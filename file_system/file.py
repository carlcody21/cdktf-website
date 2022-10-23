from cgi import print_arguments
from constructs import Construct
from helper.project_helper import Helper
from imports.aws import efs, vpc
from network.network import Network
from cdktf import TerraformOutput, Token

class Elastic_File(Helper):
    #def __init__(self, scope: Construct, ns: str, network: Network):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        self.efile = efs.EfsFileSystem(
            self,
            'efs_' + self.APP_NAME,
            creation_token='efs_' + self.APP_NAME,
        )

        #private_sub = vpc.DataAwsSubnetIds(
        #    self,
        #    'private_sub_efs',
        #    vpc_id=network.my_vpc.vpc_id_output,
        #    tags={
            #    "Tier": "Private"
        #        "name": "website_vpc-private-us-east-2b"
        #       }
        #)
        
        #TerraformOutput(
        #    self,
        #    'private_sub',
        #    value= network.my_vpc.private_subnets_output
        #)
        #count = 1
        #self.mount_point = []
        #for sub in private_sub.ids: #network.my_vpc.private_subnets:
        #    
        #    efile_mount = efs.EfsMountTarget(
        #        self,
        #        'efs_' + self.APP_NAME + '_mount_az_' + str(count),
        #        file_system_id = self.efile.id,
        #        subnet_id = sub,
        #        security_groups = [str(network.efs_sg.id)],
        #    )
        #    count+=1
        #    self.mount_point.append(efile_mount)
            