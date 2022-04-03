from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.contrib.hooks.aws_hook import AwsHook

class CsvToRedshiftOperator(BaseOperator): 
    drop_table = "DROP TABLE IF EXISTS {}"

    copy_csv_to_redshift = """
        COPY {} 
        FROM '{}'
        CREDENTIALS 'aws_access_key_id={};aws_secret_access_key={}' 
        CSV QUOTE '\"'
        DELIMITER '{}'
        REGION '{}'
        IGNOREHEADER 1;
    """

    @apply_defaults
    def __init__(self, 
                 redshift_conn_id, 
                 aws_credentials_id,  
                 s3_bucket, 
                 s3_key,
                 input_csv_file,
                 table_creation_sql,
                 redshift_table_name, 
                 delimiter,    
                 region, 
                 *args, **kwargs): 

        super(CsvToRedshiftOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.aws_credentials_id = aws_credentials_id
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.input_csv_file = input_csv_file
        self.table_creation_sql = table_creation_sql
        self.redshift_table_name = redshift_table_name
        self.delimiter = delimiter
        self.region = region 
    
    def execute(self, context): 
        # Connect to S3 
        self.log.info('Connect to S3')
        aws_hook = AwsHook(self.aws_credentials_id)
        aws_credentials = aws_hook.get_credentials()

        self.log.info('Successfully connect to S3')

        redshift_hook = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        # Loop through the input file 
        for i in range(len(self.input_csv_file)):
            input_file = self.input_csv_file[i]
            self.log.info(input_file)
            query = self.table_creation_sql[i]
            output_table = self.redshift_table_name[i]
            self.log.info(output_table)


            s3_path = "s3://{}/{}/{}".format(self.s3_bucket, self.s3_key, input_file)
            self.log.info('Now processing the file {}'.format(input_file))

            
            # Copy the data from S3 to redshift

            drop_table = "DROP TABLE IF EXISTS {} ;".format(output_table)
            create_table = query

            csv_to_redshift = CsvToRedshiftOperator.copy_csv_to_redshift.format(
                output_table,
                s3_path,
                aws_credentials.access_key,
                aws_credentials.secret_key,
                self.delimiter,
                self.region
            )

            redshift_hook.run(drop_table)
            redshift_hook.run(create_table)
            redshift_hook.run(csv_to_redshift)


