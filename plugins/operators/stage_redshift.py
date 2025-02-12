from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id='',
                 aws_credentials_id='',
                 table='',
                 s3_bucket='',
                 s3_key='',
                 json_format='auto',
                 *args, **kwargs):
        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.aws_credentials_id = aws_credentials_id
        self.table = table
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.json_format = json_format

    def execute(self, context):
        self.log.info(f'Staging data from S3 {self.s3_bucket}/{self.s3_key} to Redshift table {self.table}')
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        s3_path = f's3://{self.s3_bucket}/{self.s3_key}'
        copy_sql = f'''
            COPY {self.table}
            FROM '{s3_path}'
            IAM_ROLE 'your-iam-role'
            FORMAT AS JSON '{self.json_format}';
        '''
        self.log.info(f'Executing COPY command: {copy_sql}')
        redshift.run(copy_sql)
        self.log.info(f'Successfully staged data into {self.table}')
