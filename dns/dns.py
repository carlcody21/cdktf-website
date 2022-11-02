from constructs import Construct
from helper.project_helper import Helper
from imports.aws import route53
from cdktf import TerraformOutput, TerraformLocal, Fn, Token, TerraformIterator
#from cert.cert import HTTPS_Cert

class Domain(Helper):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)
        
        self.dns_sub_zone = route53.Route53Zone(
            self,
            'website_zone',
            name=self.DOMAIN_NAME,   
        )
        
        
        #count = cert.validation_count
        
        TerraformOutput(
            self,
            'name_servers',
            value=self.dns_sub_zone.name_servers
        )
        
        #cert_validation = []
        #for c in range(2):
        #    obj = Fn.element(cert.https_cert_validation, c)
        #    cert_validation.append(obj.resource_record_name)
            
            #cert_validation.append(route53.Route53Record(
            #self,
            #'cert_validation_records', #+ cert_validation.count,
            #type=obj.resource_record_type,
            #name=obj.resource_record_name,
            #zone_id=self.dns_sub_zone.zone_id,
            #ttl=60,
            #records=[obj.resource_record_value]
        #)#)
        #TerraformOutput(
        #    self,
        #    'test1',
        #    value=cert_validation
        #)
        
        #validation_itr = TerraformIterator.from_list(Token().as_list(cert.https_cert_validation))
        #validation_itr = TerraformIterator.from_map(cert.https_cert_validation)
        
        
        
        #validation_itr = TerraformIterator.from_map(Token.as_map(cert.https_cert_validation))
        #cert_validation = route53.Route53Record(
        #    self,
        #    'cert_validation_records',
        #    for_each=validation_itr,
        #    type=validation_itr.get_string('resource_record_type'),
        #    name=validation_itr.get_string('resource_record_name'),
        #    zone_id=self.dns_sub_zone.zone_id,
        #    ttl=60,
        #    records=[validation_itr.get_string('resource_record_value')]
        #)
        
            #type=cert.https_cert_validation.resource_record_type,
            #name=cert.https_cert_validation.resource_record_name,
            #zone_id=self.dns_sub_zone.zone_id,
            #ttl='60',
            #records=[cert.https_cert_validation.resource_record_value]