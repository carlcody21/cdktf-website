from constructs import Construct
from cdktf import TerraformStack, S3Backend
from imports.aws import AwsProvider, vpc

class Helper(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        # set constants for project
        self.AWS_PROFILE= 'cwCMD'
        self.APP_NAME = 'website'
        #self.EC2_INSTANCE_SIZE = 't2.micro'
        #self.EC2_INSTANCE_SIZE = 't3.medium'
        self.EC2_INSTANCE_SIZE = 't3.small'
        self.REGION = 'us-east-2'
        self.KEY_PAIR = ''
        self.DOMAIN_NAME='codywicker.com'
        self.STATE_BACKEND = 'cdktf-state'
        
        # VPC CONFIG
        self.VPC_SUBNET = "10.0.0.0/22"
        self.AZ1_PUBLIC_SB = "10.0.0.0/25"
        self.AZ1_PRIVATE_SB = "10.0.0.128/25"
        self.AZ2_PUBLIC_SB = "10.0.1.0/25"
        self.AZ2_PRIVATE_SB = "10.0.1.128/25"
        self.AZ = ['us-east-2a', 'us-east-2b']
        # Database Config 
        self.DB_MASTER_PORT = 3306
        self.DB_ENGINE_VERSION = '5.7'
        self.DB_INSTANCE_TYPE = ""


        # create Provider to connect to AWS with
        AwsProvider(
            self,
            "AWS", 
            region=self.REGION, 
            profile=self.AWS_PROFILE
        )
          