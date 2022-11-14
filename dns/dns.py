from constructs import Construct
from helper.project_helper import Helper
from imports.aws import route53
from cdktf import TerraformOutput, S3Backend

class Domain(Helper):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)
        
        self.dns_sub_zone = route53.Route53Zone(
            self,
            'website_zone',
            name=self.DOMAIN_NAME,   
        )
        
        S3Backend(
            self,
            profile=self.AWS_PROFILE,
            bucket=self.STATE_BACKEND,
            key='domain',
            region=self.REGION,
            encrypt=True,
            kms_key_id='alias/' + self.STATE_BACKEND,
            dynamodb_table=self.STATE_BACKEND,
        )
        
        TerraformOutput(
            self,
            'name_servers',
            value=self.dns_sub_zone.name_servers
        )
        
        TerraformOutput(
            self,
            'hosted_zone_id',
            value=self.dns_sub_zone.id
        )