import json
from typing import Sequence
from constructs import Construct
import requests
from helper.project_helper import Helper
from imports.vpc import Vpc
from imports.aws import vpc, efs
from cdktf import TerraformOutput, S3Backend, Token, Fn, TerraformIterator, ITerraformDependable
from file_system.file import Elastic_File

class Network(Helper):
    def __init__(self, scope: Construct, ns: str, efile_share: Elastic_File):
        super().__init__(scope, ns)

        # info on module 
        # https://registry.terraform.io/modules/terraform-aws-modules/vpc/aws/latest
        self.my_vpc = Vpc(
            self,
            self.APP_NAME + '_vpc',
            name=self.APP_NAME + '_vpc',
            cidr=self.VPC_SUBNET,
            azs=self.AZ,
            private_subnets=[self.AZ1_PRIVATE_SB, self.AZ2_PRIVATE_SB],
            public_subnets=[self.AZ1_PUBLIC_SB, self.AZ2_PUBLIC_SB],
            enable_nat_gateway= True,
            single_nat_gateway= True,
            enable_dns_hostnames= True,
            enable_dns_support= True,
            tags={
                "name": self.APP_NAME + "_vpc",
                'kubernetes.io/cluster/' + self.APP_NAME + '-cluster': "shared"
                },
            public_subnet_tags={
                'kubernetes.io/cluster/' + self.APP_NAME + '-cluster': "shared",
                'kubernetes.io/role/elb': '1'
            },
            private_subnet_tags={
                'kubernetes.io/cluster/' + self.APP_NAME + '-cluster': "shared",
                'kubernetes.io/role/internal-elb': '1',
                'type': 'private'
            },
            #depends_on=self.eks_sg,
        )

        open_all_egress = vpc.SecurityGroupEgress(
            cidr_blocks = ["0.0.0.0/0"],
            from_port= 0,
            protocol = "-1",
            to_port = 0,
        )

#################### EFS Security Group ####################

        efs_sg_ingress = vpc.SecurityGroupIngress(
            from_port = 2049,
            to_port = 2049,
            protocol = 'tcp',
            cidr_blocks= [self.my_vpc.cidr],
        )

        self.efs_sg = vpc.SecurityGroup(
            self,
            'efs_' + self.APP_NAME + '_sg',
            vpc_id= self.my_vpc.vpc_id_output,
            ingress = [efs_sg_ingress],
            egress = [open_all_egress],
            #depends_on=self.my_vpc,
        )

#################### ELB Security Group ####################

        elb_egress = vpc.SecurityGroupEgress(
            cidr_blocks = [str(self.my_vpc.vpc_cidr_block_output)],
            from_port = 31225,
            to_port = 31225,
            protocol = 'tcp',
        )

        elb_80_ingress = vpc.SecurityGroupIngress(
            cidr_blocks = ['0.0.0.0/0'],
            from_port = 80,
            to_port = 80,
            protocol = 'tcp'
        )
        elb_443_ingress = vpc.SecurityGroupIngress(
            cidr_blocks = ['0.0.0.0/0'],
            from_port = 443,
            to_port = 443,
            protocol = 'tcp'
        )

        self.elb_sg = vpc.SecurityGroup(
            self,
            'elb_' + self.APP_NAME + '_sg',
            name= 'elb_' + self.APP_NAME + '_sg',
            vpc_id= self.my_vpc.vpc_id_output,
            ingress=[elb_80_ingress, elb_443_ingress],
            egress=[elb_egress],
            #depends_on=self.my_vpc,
        )

#################### EKS Security Group ####################

        eks_db_egress = vpc.SecurityGroupEgress(
            cidr_blocks = [str(self.my_vpc.vpc_cidr_block_output)],
            from_port = self.DB_MASTER_PORT,
            to_port = self.DB_MASTER_PORT,
            protocol = 'tcp',
        )

        eks_22_ingress = vpc.SecurityGroupIngress(
            cidr_blocks = [self.my_vpc.vpc_cidr_block_output],
            from_port = 22,
            to_port = 22,
            protocol = 'tcp'
        )

        eks_31225_ingress = vpc.SecurityGroupIngress(
            security_groups=[self.elb_sg.id],
            from_port = 31225,
            to_port = 31225,
            protocol = 'tcp'
        )
        
        self.eks_sg = vpc.SecurityGroup(
            self,
            'eks_' + self.APP_NAME + '_sg',
            name= 'eks_' + self.APP_NAME + '_sg',
            vpc_id= self.my_vpc.vpc_id_output,
            ingress=[eks_22_ingress, eks_31225_ingress],
            egress=[eks_db_egress],
        )

#################### EFS Mount Points ####################
        self.private_sb_ids = Token().as_list(self.my_vpc.private_subnets_output)
        
        # https://developer.hashicorp.com/terraform/cdktf/concepts/iterators
        #l = TerraformIterator.from_list(Token().as_list(self.my_vpc.private_subnets_output))
        #efile_mount = efs.EfsMountTarget(
        #    self,
        #    'efs_' + self.APP_NAME + '_mount_az',
        #    for_each=l,
        #    file_system_id = efile_share.efile.id,
        #    subnet_id = Token.as_string(l.value),
        #    security_groups = [str(self.efs_sg.id)],
        #    depends_on=ITerraformDependable()
        #   )
        
        S3Backend(
            self,
            profile=self.AWS_PROFILE,
            bucket=self.STATE_BACKEND,
            key='website_network',
            region=self.REGION,
            encrypt=True,
            kms_key_id='alias/' + self.STATE_BACKEND,
            dynamodb_table=self.STATE_BACKEND,
        )
        
        TerraformOutput(
            self,
            'subnet_ids_output',
            value= Fn.tolist(self.private_sb_ids)
        )

def get_my_ip():
    call = requests.get('https://api.ipify.org?format=json')
    response = call.json()
    return response["ip"]