from airflow.hooks.postgres_hook import PostgresHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="redshift",
                 aws_credentials_id="aws_credentials",
                 table="staging_events",
                 s3_bucket="ricscar2570",
                 s3_key="log_json_path.json",
                 json_format="s3://ricscar2570/log_json_path.json",
                 *args, **kwargs):

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.aws_credentials_id = aws_credentials_id
        self.table = table
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.json_format = json_format

    def execute(self, context):
        self.log.info(f"Staging {self.table} from S3 to Redshift")

        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        # S3 path
        s3_path = f"s3://{self.s3_bucket}/{self.s3_key}"

        # Delete existing data (idempotenza)
        self.log.info(f"Clearing data from Redshift staging table {self.table}")
        redshift.run(f"DELETE FROM {self.table}")

        # COPY command
        copy_sql = f"""
            COPY {self.table}
            FROM '{s3_path}'
            ACCESS_KEY_ID '{{ AWS_ACCESS_KEY_ID }}'
            SECRET_ACCESS_KEY '{{ AWS_SECRET_ACCESS_KEY }}'
            FORMAT AS JSON '{self.json_format}';
        """

        self.log.info(f"Executing COPY command: {copy_sql}")
        redshift.run(copy_sql)
        self.log.info(f"Staging {self.table} completed successfully")
