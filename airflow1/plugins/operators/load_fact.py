from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadFactOperator(BaseOperator):
    ui_color = '#F98866'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="redshift",
                 table="",
                 sql_query="",
                 *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.sql_query = sql_query

    def execute(self, context):
        self.log.info(f"Loading data into Fact Table {self.table}")

        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        self.log.info(f"Executing SQL: {self.sql_query}")
        redshift.run(self.sql_query)

        self.log.info(f"Fact Table {self.table} loaded successfully")
