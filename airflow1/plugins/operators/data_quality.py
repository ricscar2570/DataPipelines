from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):
    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="redshift",
                 sql_checks=[],
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.sql_checks = sql_checks

    def execute(self, context):
        self.log.info("Running data quality checks")

        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        for check in self.sql_checks:
            sql_query, expected_value = check

            self.log.info(f"Executing query: {sql_query}")
            records = redshift.get_records(sql_query)

            if len(records) < 1 or len(records[0]) < 1:
                raise ValueError(f"Data quality check failed. Query {sql_query} returned no results.")

            result = records[0][0]
            if result < expected_value:
                raise ValueError(f"Data quality check failed. Query {sql_query} expected {expected_value} but got {result}")

            self.log.info(f"Data quality check passed for query: {sql_query}")
