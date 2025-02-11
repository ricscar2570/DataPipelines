from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):
    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 table="",
                 sql_query="",
                 truncate_insert=False,
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.sql_query = sql_query
        self.truncate_insert = truncate_insert

    def execute(self, context):
        self.log.info(f"Loading data into Dimension Table {self.table}")

        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        if self.truncate_insert:
            self.log.info(f"Truncating table {self.table} before insert")
            redshift.run(f"DELETE FROM {self.table}")

        self.log.info(f"Executing SQL: {self.sql_query}")
        redshift.run(self.sql_query)

        self.log.info(f"Dimension Table {self.table} loaded successfully")
