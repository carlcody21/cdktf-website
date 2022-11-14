#!/usr/bin/env python
from constructs import Construct
from cdktf import App, TerraformStack, S3Backend
from network.network import Network
from file_system.file import Elastic_File
from load_balancer.load_balancer import Load_Balancer
from cluster.cluster import Cluster
from iam.role import Roles
from kube.kube import K8WordPress
from cert.cert import HTTPS_Cert
from dns.dns import Domain
from backend.backend import Terrafrom_Backend

app = App()

# https://technology.doximity.com/articles/terraform-s3-backend-best-practices
#Defines Terraform Backend Infra
s3_backend = Terrafrom_Backend(app, 's3_backend')

#Defines route53 config for codywicker.com
domain = Domain(app, 'domain')

#Defines ACM certficate used to terminate HTTPS traffic at load balancer
cert = HTTPS_Cert(app, 'https_cert', domain)

#Defines EFS store, Kube pods are able to write to the same file system
file = Elastic_File(app, 'website_efs')

#Defines VPC config
net = Network(app, "website_network", file)

#Defines AWS roles Used by cluster
roles = Roles(app, 'website_roles')

#defines EKS cluster
cluster = Cluster(app, 'website_cluster', net, roles, file)

app.synth()
