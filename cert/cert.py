import json
from constructs import Construct
from helper.project_helper import Helper
from imports.aws import acm, route53
from cdktf import TerraformOutput, TerraformLocal, Fn, Token
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
        https_cert_validation_wildcard = self.https_cert.domain_validation_options.get(1)
        
        #self.validation_count = Fn.length_of(self.https_cert_validation)
        #self.https_cert_validation = Fn.element(self.https_cert.domain_validation_options, 1)
        #Fn.element(Token().as_list(self.https_cert.domain_validation_options))
        
        #domain_id = route53.DataAwsRoute53Zone(
        #    self,
        #    'data_domain',
        #    private_zone=False,
        #    name=self.DOMAIN_NAME,
        #)
        
        dns_validation_record_standard = route53.Route53Record(
            self,
            'cert_validation_record_standard', #+ cert_validation.count,
            type=https_cert_validation_standard.resource_record_type,
            name=https_cert_validation_standard.resource_record_name,
            zone_id=domain.dns_sub_zone.zone_id,
            ttl=300,
            records=[https_cert_validation_standard.resource_record_value],
        )
        
        #dns_validation_record_wildcard = route53.Route53Record(
        #    self,
        #    'cert_validation_record_wildcard', #+ cert_validation.count,
        #    type=https_cert_validation_wildcard.resource_record_type,
        #    name=https_cert_validation_wildcard.resource_record_name,
        #    zone_id=domain.dns_sub_zone.zone_id,
        #    ttl=60,
        #    records=[https_cert_validation_wildcard.resource_record_value]
        #)
        
        
        #maybe use https://github.com/hashicorp/terraform-cdk/issues/430
        #cert_validation = []
        #for c in range(Fn.length_of(Token.as_number(self.https_cert_validation))):
        #    obj=Fn.element(self.https_cert.domain_validation_options, c)
        #    cert_validation.append(obj.resource_record_name)
        
        #TerraformOutput(
        #    self,
        #    'test1',
        #    value=cert_validation
        #)
            
        
        TerraformOutput(
            self,
            'cert_arn',
            value=self.https_cert.arn
        )
        