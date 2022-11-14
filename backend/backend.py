from constructs import Construct
from helper.project_helper import Helper
from cdktf import S3Backend
from imports.aws import s3, kms, dynamodb

# https://technology.doximity.com/articles/terraform-s3-backend-best-practices

class Terrafrom_Backend(Helper):
 def __init__(self, scope: Construct, ns: str):
    super().__init__(scope, ns)
    
    s3_key = kms.KmsKey(
        self,
        's3_kms_key',
        description='used to encrypt s3 bucket objects',
        deletion_window_in_days=10,
        enable_key_rotation=True,
    )
    
    self.s3_alias = kms.KmsAlias(
        self,
        'kms_alias',
        name='alias/' + self.STATE_BACKEND,
        target_key_id= s3_key.id,
    )
    
    self.state_bucket = s3.S3Bucket(
        self,
        'state_bucket',
        bucket=self.STATE_BACKEND,
    )
    
    s3_acl = s3.S3BucketAcl(
        self,
        's3_acl',
        bucket=self.state_bucket.id,
        acl='private'
    )
    s3_ver = s3.S3BucketVersioningA(
        self,
        's3_ver',
        bucket= self.state_bucket.id,
        versioning_configuration = {'status': 'Enabled'}
    )
    
    default_encrypt_rule_config = s3.S3BucketServerSideEncryptionConfigurationRuleApplyServerSideEncryptionByDefaultA(
     kms_master_key_id= s3_key.id,
     sse_algorithm='aws:kms',
    )
   
    encrypt_rule_config = s3.S3BucketServerSideEncryptionConfigurationRuleA(
        apply_server_side_encryption_by_default=default_encrypt_rule_config
    )

    s3_encrypt = s3.S3BucketServerSideEncryptionConfigurationA(
        self,
        's3_encrypt',
        bucket=self.state_bucket.id,
        #rule=dict({'apply_server_side_encryption_by_default': {'kms_master_key_id': str(s3_key.id),'sse_algorithm': 'aws:kms'}}),
        rule=[encrypt_rule_config],
    )
    
    dyna_attribute = dynamodb.DynamodbTableAttribute(
        name='LockID',
        type='S',
    )
    self.dyna_db_table = dynamodb.DynamodbTable(
        self,
        'dyna_db_table',
        name=self.STATE_BACKEND,
        read_capacity=20,
        write_capacity=20,
        hash_key='LockID',
        #attribute={'name': 'LockID','type': 'S' }
        attribute=[dyna_attribute],
    )
    
    S3Backend(
        self,
        profile=self.AWS_PROFILE,
        bucket=self.STATE_BACKEND,
        key='s3_backend',
        region=self.REGION,
        encrypt=True,
        kms_key_id='alias/' + self.STATE_BACKEND,
        dynamodb_table=self.STATE_BACKEND,
        )