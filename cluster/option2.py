from constructs import Construct
from network.network import Network
from  helper.project_helper import Helper
from imports.eks import Eks, EksOptions
from imports.aws import eks
from iam.role import Roles

class Cluster(Helper):
    def __init__(self, scope: Construct, ns: str, network: Network, role: Roles):
        super().__init__(scope, ns)

        self.cluster = Eks(
            self,
            self.APP_NAME + '-cluster',
            cluster_name = self.APP_NAME + '-cluster',
            vpc_id = network.my_vpc.vpc_id_output,
            #subnet_ids= network.my_vpc.private_subnets,
            subnet_ids= network.private_sb_ids,
            cluster_endpoint_private_access=False,
            cluster_endpoint_public_access=True,
            #cluster_addons= {'coredns': {'resolve_conflicts': "OVERWRITE"}, 'kube-proxy':{}, 'vpc-cni':{ 'resolve_conflicts': 'OVERWRITE'} }, 
            cluster_addons= {'vpc-cni':{ 'resolve_conflicts': 'OVERWRITE'} }, 
            #eks_managed_node_groups=
            #self_managed_node_group_defaults= {
            self_managed_node_groups= { 
                'ng_one': {
                    'name': 'ng_one',
                    'instace_type': self.EC2_INSTANCE_SIZE,
                    'max_size': 1,
                    'desired_size': 1,
                    'min_size': 1,
                    'additional_security_group_ids': [network.eks_sg.id]
                    }
                }
            )
        