From SCSE RecSys group

As of 06.20, the yelp_data was too large to push into the GitHub Repository. Instead, anyone using this repository should download the dataset from Kaggle, and organize the directory as follows:

datasets/
|--datasets.txt
|--ml-100k data description.txt
|--README.txt
|--yelp_dataset data description.txt
|--ml-100k/
|--yelp_dataset/
|  |--utility-matrix/
|  |--yelp_business.csv
|  |--yelp_business_attributes.csv
|  |--yelp_business_hours.csv
|  |--yelp_checkin.csv
|  |--yelp_review.csv
|  |--yelp_tip.csv
|  |--yelp_user.csv

The last 7 .csv files are the datasets we retrieved our data from. It may be absent from the repository but it should be used and maintained in this way for the project.

