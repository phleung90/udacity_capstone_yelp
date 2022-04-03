# udacity_capstone_yelp

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
In the source data, it contains data since 2010 and there are couple of source data in different categories 
- yelp_academic_dataset_business.json
- yelp_academic_dataset_checkin.json
- yelp_academic_dataset_covid_features.json
- yelp_academic_dataset_review.json
- yelp_academic_dataset_tip.json
- yelp_academic_dataset_user.json

In this project, as we focus in reporting the business performance in general, we do not need all the data from the source files. 
At the same time, the data in earlier time e.g 2010, 2011, might not be able to bring many insights as there are drastic changes in internal environment and external environment, therefore we only extract the review data and check in data since 2020-01-01



