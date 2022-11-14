from constructs import Construct
from network.network import Network
from file_system.file import Elastic_File
from  helper.project_helper import Helper
from cdktf import TerraformOutput, S3Backend, TerraformLocal, Fn, TerraformIterator, Token
from imports.aws import eks, efs, vpc
from iam.role import Roles

class Cluster(Helper):
    def __init__(self, scope: Construct, ns: str, network: Network, role: Roles, efile_share: Elastic_File):
        super().__init__(scope, ns)

        # https://developer.hashicorp.com/terraform/cdktf/concepts/iterators
        l = TerraformIterator.from_list(Token().as_list(network.my_vpc.private_subnets_output))
        efile_mount = efs.EfsMountTarget(
            self,
            'efs_' + self.APP_NAME + '_mount_az',
            for_each=l,
            file_system_id = efile_share.efile.id,
            subnet_id = Token.as_string(l.value),
            security_groups = [str(network.efs_sg.id)],
            )
        
        # Info for VPC config from
        #  https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/eks_cluster#vpc_config
        vpc_config = eks.EksClusterVpcConfig(
            subnet_ids=network.private_sb_ids,
            endpoint_private_access=True,
            endpoint_public_access=True,
       ) 

        #info - https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/eks_cluster
        self.cluster = eks.EksCluster(
            self,
            self.APP_NAME + "-cluster",
            name= self.APP_NAME + "-cluster",
            vpc_config = vpc_config,
            role_arn= role.eks_cluster_role.arn,
        )
            

        scaling = eks.EksNodeGroupScalingConfig(
            desired_size=1,
            max_size=1,
            min_size=1
        )
        
        group_az1 = eks.EksNodeGroup(
            self,
            'group_az1',
            cluster_name=self.cluster.name,
            node_group_name= self.APP_NAME + 'wg_az1',
            subnet_ids=network.private_sb_ids,
            scaling_config=scaling,
            node_role_arn= role.eks_node_role.arn,
            instance_types=[self.EC2_INSTANCE_SIZE],
        )

        group_az2 = eks.EksNodeGroup(
            self,
            'group_az2',
            cluster_name=self.cluster.name,
            node_group_name= self.APP_NAME + 'wg_az2',
            subnet_ids=network.private_sb_ids,
            scaling_config=scaling,
            node_role_arn= role.eks_node_role.arn,
            instance_types=[self.EC2_INSTANCE_SIZE],

        )
        
        self.token = eks.DataAwsEksClusterAuth(
            self,
            self.APP_NAME + '_cluster_token',
            #id=self.cluster.id,
            name=self.cluster.name,
        )
        
        S3Backend(
            self,
            profile=self.AWS_PROFILE,
            bucket=self.STATE_BACKEND,
            key='website_cluster',
            region=self.REGION,
            encrypt=True,
            kms_key_id='alias/' + self.STATE_BACKEND,
            dynamodb_table=self.STATE_BACKEND,
        )
        
        #eks.DataAwsEksClusterCertificateAuthority
       # self.cert = eks.DataAwsEksClusterCertificateAuthorityList(
        #    terraform_resource=self.cluster
        #    terraform_attribute=
        #    wraps_set=True
        #)
        
        #self.cert = eks.DataAwsEksClusterCertificateAuthority(
        #    self,
        #    self.APP_NAME + '_cluster_cert',
        #    #id=self.cluster.id,
        #    #name=self.cluster.name,
        #)
        
        #TerraformOutput(
        #    self,
        #    'cluster_cert',
            #value= self.cluster.certificate_authority
        #    value= self.cluster.certificate_authority.get(0).data,
            #value= json.loads(str(self.cluster.certificate_authority))
            #value= type(self.cluster.certificate_authority)
            #value= str(self.cluster.certificate_authority),
        #)
        
        #self.cluster_cert = TerraformLocal(
         #   self,
         #   'cluster_cert_var',
         #   value = self.cluster.certificate_authority,
        #)