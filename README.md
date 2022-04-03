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
Most of the source files are from the YELP dataset, which is available here: https://www.yelp.com/dataset

In this project, the following files from the dataset are used:

business.json -- Contains business data including location data, attributes, and categories
review.json -- Contains full review text data including the user_id that wrote the review and the business_id the review is written for
user.json -- User data including the user's friend mapping and all the metadata associated with the user.
checkin.json -- Checkins on a business.
tip.json -- Tips written by a user on a business. Tips are shorter than reviews and tend to convey quick suggestions

And to extend the information of location, we also use the csv file here: https://public.opendatasoft.com/explore/dataset/us-cities-demographics/export/

In this case, we have 2 different forms of data source.



