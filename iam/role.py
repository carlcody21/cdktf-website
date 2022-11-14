from constructs import Construct
from helper.project_helper import Helper
from imports.aws import iam
from pathlib import Path
from cdktf import TerraformOutput, S3Backend

class Roles(Helper):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        cluster_trust = '{"Version": "2012-10-17","Statement": [{"Effect": "Allow","Principal": {"Service": ["eks.amazonaws.com","ec2.amazonaws.com"]},"Action": "sts:AssumeRole"}]}'
        node_perm = '{"Version": "2012-10-17","Statement": [{"Action": ["sts:AssumeRole"],"Effect": "Allow","Principal": {"Service": ["eks-nodegroup.amazonaws.com", "ec2.amazonaws.com" ]}}]}'
        
############ Provision Role for EKS Cluster ############
        self.eks_cluster_role = iam.IamRole(
            self,
            'eks_cluster' + self.APP_NAME + '_role',
            name='eks_' + self.APP_NAME + '_role',
            assume_role_policy=cluster_trust,
        )

        cluster_policy = iam.DataAwsIamPolicy(
            self,
            'get_cluster_policy',
            name = 'AmazonEKSClusterPolicy',
        )

        attach_cluster = iam.IamPolicyAttachment(
            self,
            'attach_eks_cluster_policy',
            name='attach_eks_cluster_policy',
            policy_arn=cluster_policy.arn,
            roles=[str(self.eks_cluster_role.name)],
        )

############ Provision Role for EKS Node Groups ############
        self.eks_node_role = iam.IamRole(
            self,
            'eks_node' + self.APP_NAME + '_role',
            name='eks_node_' + self.APP_NAME + '_role',
            assume_role_policy= node_perm,
        )

        node_policy = iam.DataAwsIamPolicy(
            self,
            'get_node_policy',
            name = 'AmazonEKSWorkerNodePolicy',
        )

        cni_policy = iam.DataAwsIamPolicy(
            self,
            'get_cni',
            name = 'AmazonEKS_CNI_Policy',
        )

        attach_node = iam.IamPolicyAttachment(
            self,
            'attach_eks_node_policy',
            name='attach_eks_node_policy',
            policy_arn=node_policy.arn,
            roles=[str(self.eks_node_role.name)],
        )

        reg_policy = iam.DataAwsIamPolicy(
            self,
            'get_no_policy',
            name = 'AmazonEC2ContainerRegistryReadOnly',
        )

        attach_reg = iam.IamPolicyAttachment(
            self,
            'attach_reg_policy',
            name='attach_reg_policy',
            policy_arn=reg_policy.arn,
            roles=[str(self.eks_node_role.name)],
        )

        attach_cni = iam.IamPolicyAttachment(
            self,
            'attach_cni_policy',
            name='attach_cni_policy',
            policy_arn=cni_policy.arn,
            roles=[str(self.eks_node_role.name)],
        )
        
############ Provision Policy EKS access to EFS ############
        #with open('./iam/eks_efs_policy.json', 'r') as f:
        eks_efs_policy_data = Path('./iam/eks_efs_policy.json').read_text()
            
        eks_efs_policy = iam.IamPolicy(
            self,
            'efs_eks_policy',
            name='EFSCSIControllerIAMPolicy',
            policy=eks_efs_policy_data,
            description='eks_efs_policy',
        )

############ Provision Policy EKS access to ELB ############
        eks_elb_policy_data = Path('./iam/eks_elb_policy.json').read_text()
            
        eks_elb_policy = iam.IamPolicy(
            self,
            'efs_elb_policy',
            name='ALBIngressControllerIAMPolicy',
            policy=eks_elb_policy_data,
            description='efs_elb_policy',
        )

        #self.eks_role = iam.IamRole(
         #   self,
         #   self.APP_NAME + '_eks_role',
         #   name=self.APP_NAME + '_eks_role',
         #   managed_policy_arns=
        #)
        
        S3Backend(
            self,
            profile=self.AWS_PROFILE,
            bucket=self.STATE_BACKEND,
            key='website_roles',
            region=self.REGION,
            encrypt=True,
            kms_key_id='alias/' + self.STATE_BACKEND,
            dynamodb_table=self.STATE_BACKEND,
        )