from cgi import print_arguments
from constructs import Construct
from helper.project_helper import Helper
from imports.aws import efs, vpc
from cdktf import TerraformOutput, S3Backend, Token

class Elastic_File(Helper):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        self.efile = efs.EfsFileSystem(
            self,
            'efs_' + self.APP_NAME,
            creation_token='efs_' + self.APP_NAME,
        )
        
        S3Backend(
            self,
            profile=self.AWS_PROFILE,
            bucket=self.STATE_BACKEND,
            key='website_efs',
            region=self.REGION,
            encrypt=True,
            kms_key_id='alias/' + self.STATE_BACKEND,
            dynamodb_table=self.STATE_BACKEND,
        )
        
        TerraformOutput(
            self,
            'efs_id',
            value=self.efile.id
        )
        