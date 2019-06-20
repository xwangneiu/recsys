# Builds the utility matrix from the yelp_review.csv file
# specifically for Stuttgart, BW, Germany for testing.
# Can be modified to build the matrix for the entirety of the file for all 11 metropolitan areas
# Minh N. and Chen T.
# 2019.06.19

import pandas as pd
import numpy as np

def utility_matrix(data_csv, output_csv):
	
	df_list = []
	df = pd.DataFrame()
	
	# this reader was used to test the algorithm on 4 chunks
	# reader = pd.read_csv(data_csv, iterator = True)
	# for i in range(100):

	# reads yelp_business.csv to join with chunks
	# possibly needs to be restructured to include in parameters?
	df_business = pd.read_csv('../yelp_business.csv')

	for chunk in pd.read_csv(data_csv, chunksize = 500):
		# note that review.csv and business.csv both has 'stars' columns, which are relabeled as 'stars_x' and 'stars_y' respectively
		chunk = pd.merge(chunk, df_business, on = 'business_id')
		chunk = chunk[chunk.city == 'Mesa']
		temp_df = pd.pivot_table(chunk, values = 'stars_x', index = 'user_id', columns = 'business_id')
		df_list.append(temp_df)
	while df_list:
		df = pd.concat([df, df_list.pop(0)], sort = False)
	df.to_csv(output_csv)

def main():
	utility_matrix('../yelp_review.csv', 'yelp_utility_matrix_mesa.csv')

if __name__ == '__main__' :
	main()