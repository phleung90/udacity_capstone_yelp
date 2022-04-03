# Udacity_capstone_yelp

## Project introduction 
In this project, it is assumed that we are working in the data engineering department, and we need to provide data to BI analysts to create dashboards and answer the business questions i.e how's the performance of yelp from time to time. 

To achieve the goal, we will need to know 2 key questions:
- How's the change of no.of users from time to time?
- How's the user engagement behvaiour?

To answer the key questions, below are some of the example business that we need to answer: 
- What is the user growth from time to time?
- How many checkins/reviews are given from users from time to time?
- What are the most popular restaurant from time to time?
- What are the ratings from time to time?

With these information, YELP can then optimize the display sequence of business partner, so that more user will come and increase the website traffic

## Data scope
Most of the source files are from the YELP dataset, which is available here: https://www.yelp.com/dataset

In this project, the following files from the dataset are used:

- business.json -- Contains business data including location data, attributes, and categories
- review.json -- Contains full review text data including the user_id that wrote the review and the business_id the review is written for
- user.json -- User data including the user's friend mapping and all the metadata associated with the user.
- checkin.json -- Checkins on a business.
- tip.json -- Tips written by a user on a business. Tips are shorter than reviews and tend to convey quick suggestions

And to extend the information of location, we also use the csv file here: https://public.opendatasoft.com/explore/dataset/us-cities-demographics/export/

In this case, we have 2 different forms of data source.

## Steps involved
- Step 1: Scope the Project and Gather Data
- Step 2: Explore and Assess the Data
- Step 3: Define the Data Model
- Step 4: Run ETL to Model the Data
- Step 5: Complete Project Write Up

## Process 
For step 1-3, the data cleaning process recorded in the jupyter notebook. In the notebook, we use spark to read the source data, select the information that we need and prepare for the ETL process 

For step 4, the exct ETL process is run in airflow. The main DAG (yelp-project.py), the SQL queries (sql_queries.py) and the operators (csv_redshift.py, load_dimension.py, load_fact.py and data_quality.py) are included in this file. 

The data dictionary is also includede in the jupyter notebook

## Final write up 
**Situation 1: The data was increased by 100x.**
- For the data cleaning process, we will need to set up EMR cluster in AWS, and to load spark there to process the data.
- For ETL process, it would not be affected as it is scalable in redshift

**Situation 2: The pipelines would be run on a daily basis by 7 am every day**
- This would be easy as we can set the schedule in airflow and run it at 7pm every day

**The database needed to be accessed by 100+ people.**
- There would be no problem as the AWS redshift is scalable
