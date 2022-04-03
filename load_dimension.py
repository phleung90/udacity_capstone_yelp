from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults



class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id, 
                 target_tables,
                 table_creation_sql, 
                 table_insert_sql,
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.target_tables = target_tables
        self.table_creation_sql = table_creation_sql
        self.table_insert_sql = table_insert_sql 

    def execute(self, context):
        self.log.info('LoadDimensionOperator not implemented yet')
        
        redshift_hook = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        for i in range(len(self.target_tables)):
            target_table = self.target_tables[i]
            table_creation = self.table_creation_sql[i]
            data_insert = self.table_insert_sql[i]

            drop_table = f'DROP TABLE IF EXISTS {target_table}'
            create_table = table_creation
            insert_table = data_insert

            redshift_hook.run(drop_table)
            redshift_hook.run(create_table)
            redshift_hook.run(insert_table)