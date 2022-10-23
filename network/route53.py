from constructs import Construct
from helper.project_helper import Helper
from imports.aws import route53

class DNS(Helper):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        self.host_zone = route53.Route53Zone(
            self,
            self.APP_NAME + '_dns',
            name='codywicker.com', 
        )
        