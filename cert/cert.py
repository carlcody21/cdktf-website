from constructs import Construct
from helper.project_helper import Helper
from imports.aws import acm, route53
from cdktf import TerraformOutput, S3Backend
from dns.dns import Domain

class HTTPS_Cert(Helper):
    def __init__(self, scope: Construct, ns: str, domain: Domain):
        super().__init__(scope, ns)
        
        self.https_cert = acm.AcmCertificate(
            self,
            'cluster_cert',
            domain_name=self.DOMAIN_NAME,
            validation_method='DNS',
            subject_alternative_names=['*.' + self.DOMAIN_NAME],
        )
        
        https_cert_validation_standard = self.https_cert.domain_validation_options.get(0)
        #https_cert_validation_wildcard = self.https_cert.domain_validation_options.get(1)
        
        dns_validation_record_standard = route53.Route53Record(
            self,
            'cert_validation_record_standard', #+ cert_validation.count,
            type=https_cert_validation_standard.resource_record_type,
            name=https_cert_validation_standard.resource_record_name,
            zone_id=domain.dns_sub_zone.zone_id,
            ttl=300,
            records=[https_cert_validation_standard.resource_record_value],
        )
        
        S3Backend(
            self,
            profile=self.AWS_PROFILE,
            bucket=self.STATE_BACKEND,
            key='https_cert',
            region=self.REGION,
            encrypt=True,
            kms_key_id='alias/' + self.STATE_BACKEND,
            dynamodb_table=self.STATE_BACKEND,
        )
        
        TerraformOutput(
            self,
            'cert_arn',
            value=self.https_cert.arn
        )
        