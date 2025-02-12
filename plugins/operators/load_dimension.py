from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):
    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id='',
                 table='',
                 sql_query='',
                 truncate_insert=True,
                 *args, **kwargs):
        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.sql_query = sql_query
        self.truncate_insert = truncate_insert

    def execute(self, context):
        self.log.info(f'Loading data into dimension table {self.table}')
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        if self.truncate_insert:
            self.log.info(f'Truncating table {self.table} before insert')
            redshift.run(f'TRUNCATE TABLE {self.table}')
        
        formatted_sql = f"""
            INSERT INTO {self.table}
            {self.sql_query}
        """
        self.log.info(f'Executing query: {formatted_sql}')
        redshift.run(formatted_sql)
        self.log.info(f'Successfully loaded data into {self.table}')
