from constructs import Construct
from cdktf import TerraformStack, S3Backend
from imports.aws import AwsProvider, vpc

class Helper(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        # set constants for project
        self.AWS_PROFILE= 'ENTER PROFILE NAME'
        self.APP_NAME = 'ENTER APP NAME'

        # https://aws.amazon.com/ec2/pricing/on-demand/
        self.EC2_INSTANCE_SIZE = 'ENTER INSTANCE SIZE'
        self.REGION = 'ENTER AWS REGION'
        self.KEY_PAIR = ''
        self.DOMAIN_NAME='ENTER AWS HOSTED ZONE NAME'
        self.STATE_BACKEND = 'cdktf-state'
        
        # VPC CONFIG
        self.VPC_SUBNET = "10.0.0.0/22"
        self.AZ1_PUBLIC_SB = "10.0.0.0/25"
        self.AZ1_PRIVATE_SB = "10.0.0.128/25"
        self.AZ2_PUBLIC_SB = "10.0.1.0/25"
        self.AZ2_PRIVATE_SB = "10.0.1.128/25"
        self.AZ = ['ENTER AWS AVAILABILITY ZONE A', 'ENTER AWS AVAILABILITY ZONE B']
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
          
