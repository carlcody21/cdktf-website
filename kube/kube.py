from constructs import Construct
from helper.project_helper import Helper
from cdktf import TerraformStack, TerraformOutput, Token
from imports.kubernetes import KubernetesProvider, Namespace, Deployment, Service
from cluster.cluster import Cluster
import base64
import json
#import subprocess
import os

class K8WordPress(Helper):
    def __init__(self, scope: Construct, ns: str, kube_cluster: Cluster):
        super().__init__(scope, ns)

        # https://www.codespeedy.com/encoding-and-decoding-base64-strings-in-python/
        
        
        #print(type(kube_cluster.cluster.certificate_authority))
        #cert = base64.b64decode(kube_cluster.cluster.certificate_authority)
        #cert = kube_cluster.cluster.certificate_authority['data']
        #cert = bytes(kube_cluster.cluster.certificate_authority).decode('ascii')
        #cert = str(kube_cluster.cluster.certificate_authority)
        #cert = (json.dumps(kube_cluster.cluster.certificate_authority))['data']
        #cert = base64.b64decode(kube_cluster.cluster.certificate_authority.get(0).data).decode("utf-8") 
        #data = bytes(kube_cluster.cluster.certificate_authority.get(0).data, encoding='ascii') #.isascii()
        #data = base64.b64decode(kube_cluster.cluster.certificate_authority.get(0).data + '==').decode('ascii')
        data = Token.as_string(kube_cluster.cluster.certificate_authority.get(0).data)
        #data = kube_cluster.cluster.certificate_authority.get(0).data

        #file = open('pem.txt', 'w')
        #file.write(data)
        #file.close()
        #data_by = data.encode('ascii')
        #string_by = base64.standard_b64decode(data)
        #string = string_by.decode('ascii')
        #cert = base64.unpack(kube_cluster.cluster.certificate_authority.get(0).data)
        #cert = base64.b64decode(data , validate=False)
        #cert = data.decode('ascii')
        #cert = base64.b64decode(data + bytes('==', encoding='ascii')).decode('ascii')
        #+ '=='
        #cert = base64.b64decode(Token.as_string(kube_cluster.cluster.certificate_authority.get(0).data + "=="))
        #cert = os.popen('echo ' + data + ' | base64 -d').read()
        #TerraformOutput(
        #    self,
        #    'test_data',
        #    value=data
        #)
        
        #TerraformOutput(
         #   self,
        #   'test_cert',
        #   value=
        #)
        
        #cert = subprocess.check_output('echo ' + data + ' | base64 -d', shell=True)
        #cluster_ca_lookup_string = ''.join(c for c in kube_cluster.cluster.certificate_authority.get(0).data
         #                              if c not in '{}$')
        #KubernetesProvider(
        #    self,
        #    self.APP_NAME + '_k8_provider',
            #https://discuss.hashicorp.com/t/leveraging-built-in-terraform-functions-in-cdktf/17118/6
            #https://developer.hashicorp.com/terraform/cdktf/concepts/variables-and-outputs
            #https://learn.hashicorp.com/tutorials/terraform/helm-provider?in=terraform/kubernetes&_ga=2.185485417.112652662.1666318193-494919862.1661381262
            #cluster_ca_certificate=data,
        #    cluster_ca_certificate=f'${{base64decode({cluster_ca_lookup_string})}}',
            #cluster_ca_certificate=f"${{base64decode(module.{kube_cluster.node.id}.cluster_certificate_authority_data)}}",
            #cluster_ca_certificate= Fn.base64decode(kube_cluster.certificate_authority.get(0).data),
            #cluster_ca_certificate=f'${{base64decode({kube_cluster.cert.get(0).data})}}',
            #cluster_ca_certificate=f'${{base64decode({data})}}',
        #    token=str(kube_cluster.token),
        #    host=kube_cluster.cluster.endpoint,
        #)

        #Namespace(
        #    self,
        #    self.APP_NAME + 'k8_ns',
        #    metadata= {
        #        'annotations': {
        #            'name': 'wordpress-ns'
        #           },
        #        'labels': {
        #            'name': 'wordpress'
        #        },
        #        'name': 'wordpress-ns',
        #    }
        #)

        #Service(

        #)

        #Deployment(
            
        #)

        


        