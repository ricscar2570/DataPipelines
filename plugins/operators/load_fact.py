from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadFactOperator(BaseOperator):
    ui_color = '#F98866'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id='',
                 table='',
                 sql_query='',
                 *args, **kwargs):
        super(LoadFactOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.sql_query = sql_query

    def execute(self, context):
        self.log.info(f'Loading data into fact table {self.table}')
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        # Inserimento dati senza eliminazione (append-only)
        formatted_sql = f"""
            INSERT INTO {self.table}
            {self.sql_query}
        """
        self.log.info(f'Executing query: {formatted_sql}')
        redshift.run(formatted_sql)
        self.log.info(f'Successfully loaded data into {self.table}')
