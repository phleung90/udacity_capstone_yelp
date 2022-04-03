from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import (CsvToRedshiftOperator, LoadDimensionOperator, LoadFactOperator, DataQualityOperator)
from helpers import SqlQueries


default_args = {
    'start_date': datetime(2022, 3, 21),
    'depends_on_past': False, 
    'retries': 0, 
    'retry_delay': timedelta(minutes=5), 
    'catchup': False, 
    'email_on_retry': False
}

dag = DAG('udac_yelp_project',
          default_args=default_args,
          description='Load and transform data in Redshift with Airflow',
          schedule_interval= '0 * * * *',
        )

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

# Tables and queries to copy csv from s3 to redshift
csv_file_list = ['yelp_academic_dataset_business_output.csv', 'yelp_academic_dataset_checkin_output.csv', 'yelp_academic_dataset_cities_output.csv', 'yelp_academic_dataset_review_output.csv', 'yelp_academic_dataset_tip_output.csv', 'yelp_academic_dataset_user_output.csv']
copy_to_redshift_query = [SqlQueries.staging_business_table_create, SqlQueries.staging_checkin_table_create, SqlQueries.staging_cities_table_create, SqlQueries.staging_review_table_create, SqlQueries.staging_tip_table_create, SqlQueries.staging_users_table_create]
output_table = ['public.staging_business', 'public.staging_checkin', 'public.staging_cities', 'public.staging_review', 'public.staging_tip', 'public.staging_user']

# Tables and queries to create dimension table in redshift
dimension_tables = ['public.dim_business_location', 'public.dim_business','public.dim_cities', 'public.dim_users']
dimension_tables_creation = [SqlQueries.dimension_location_table_create, SqlQueries.dimension_business_table_create, SqlQueries.dimension_cities_table_create, SqlQueries.dimension_users_table_create]
dimension_tables_insertion = [SqlQueries.dimension_location_table_insert, SqlQueries.dimension_business_table_insert, SqlQueries.dimension_cities_table_insert, SqlQueries.dimension_users_table_insert]

# Tables and queries to create fact table in redshift
fact_tables = ['public.fact_tip', 'public.fact_checkin','public.fact_review']
fact_tables_creation = [SqlQueries.fact_tip_table_create, SqlQueries.fact_checkin_table_create, SqlQueries.fact_review_table_create]
fact_tables_insertion = [SqlQueries.fact_tip_table_insert, SqlQueries.fact_checkin_table_insert, SqlQueries.fact_review_table_insert]

csv_to_redshift = CsvToRedshiftOperator(
    task_id='CsvToRedshift',
    redshift_conn_id='redshift', 
    aws_credentials_id='aws_credentials',
    s3_bucket='yelp-dataset-udacity-capstone', 
    s3_key='csv_output', 
    input_csv_file = csv_file_list,
    table_creation_sql = copy_to_redshift_query, 
    redshift_table_name = output_table, 
    delimiter = ',',
    region='us-west-2',
    dag=dag
)

staging_quality_checks = DataQualityOperator(
    task_id='Staging_data_quality_checks',
    redshift_conn_id = 'redshift',
    table_name = output_table,
    dag=dag
)

load_dimension_tables = LoadDimensionOperator(
    task_id='LoadDimensions',
    redshift_conn_id = 'redshift', 
    target_tables = dimension_tables,
    table_creation_sql = dimension_tables_creation,
    table_insert_sql = dimension_tables_insertion, 
    dag=dag
)

dimension_quality_checks = DataQualityOperator(
    task_id='Dimension_data_quality_checks',
    redshift_conn_id = 'redshift',
    table_name = dimension_tables,
    dag=dag
)

load_facts_tables = LoadFactOperator(
    task_id='LoadFacts',
    redshift_conn_id = 'redshift', 
    target_tables = fact_tables,
    table_creation_sql = fact_tables_creation,
    table_insert_sql = fact_tables_insertion, 
    dag=dag
)

fact_quality_checks = DataQualityOperator(
    task_id='Fact_data_quality_checks',
    redshift_conn_id = 'redshift',
    table_name = fact_tables,
    dag=dag
)



start_operator >> csv_to_redshift
csv_to_redshift >> staging_quality_checks
staging_quality_checks >> load_dimension_tables
load_dimension_tables >> dimension_quality_checks
staging_quality_checks >> load_facts_tables
load_facts_tables >> fact_quality_checks