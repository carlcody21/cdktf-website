from cgi import print_arguments
from constructs import Construct
from helper.project_helper import Helper
from imports.aws import efs, vpc
from cdktf import TerraformOutput, Token

class Elastic_File(Helper):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        self.efile = efs.EfsFileSystem(
            self,
            'efs_' + self.APP_NAME,
            creation_token='efs_' + self.APP_NAME,
        )