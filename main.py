#!/usr/bin/env python
from constructs import Construct
from cdktf import App, TerraformStack
from network.network import Network
from file_system.file import Elastic_File
from load_balancer.load_balancer import Load_Balancer
from cluster.cluster import Cluster
#from cluster.option2 import Cluster
from iam.role import Roles
from kube.kube import K8WordPress



app = App()

f = Elastic_File(app, 'website_efs')

#net = Network(app, "website_network", f)
net = Network(app, "website_network")
#el = Load_Balancer(app, 'website_elb', net)
r = Roles(app, 'website_roles')
c = Cluster(app, 'website_cluster', net, r)
#print(dir(c.cluster.certificate_authority))
#print(vars(c.cluster.certificate_authority))

#kube = K8WordPress(app, 'kube', c)
app.synth()
