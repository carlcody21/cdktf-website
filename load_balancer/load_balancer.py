from constructs import Construct
from helper.project_helper import Helper
from imports.aws import elb
from network.network import Network

class Load_Balancer(Helper):
    def __init__(self, scope: Construct, ns: str, network: Network):
        super().__init__(scope, ns)

        # provision load balancer
        
        self.cluster_elb = elb.Lb(
            self,
            'elb_' + self.APP_NAME,
            load_balancer_type= 'application', 
            internal = False,
            subnets=network.my_vpc.public_subnets,
            security_groups = [str(network.elb_sg.id)], 
        )

        hc = elb.LbTargetGroupHealthCheck(
            enabled= True,
            path= '/wp-admin/install.php',
            protocol='HTTP',
            port='31225',
            interval=30,
            healthy_threshold=2,
            unhealthy_threshold=2,
            #timeout=5,         
        )

        #info - https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lb_target_group
        eks_target = elb.LbTargetGroup(
            self,
            'eks_tg_' + self.APP_NAME,
            port= 31225,
            protocol='TCP',
            health_check= hc,
            vpc_id=network.my_vpc.vpc_id_output,
            target_type='instance',

        )
        
        elb_default_action = elb.LbListenerDefaultAction(
            type= 'forward',
            target_group_arn=str(eks_target.arn),
        )

        # provisonin listeners
        #info - https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lb_listener
        port80_listener = elb.LbListener(
            self,
            'port80_listener',
            load_balancer_arn= self.cluster_elb.arn,
            port= 80,
            protocol= 'HTTP',
            default_action= [elb_default_action],
        )

        # uncomment when we want to work on 443/SSL,
        #  will need to create ssl cert and pass
        #port443_listener = elb.LbListener(
        #    self,
        #    'port443_listener',
        #    load_balancer_arn= self.cluster_elb.arn,
        #    port= 443,
        #    protocol= 'HTTPS',
        #    default_action= elb_default_action,
        #    #ssl_policy=
        #    #certificate_arn=
        #)
