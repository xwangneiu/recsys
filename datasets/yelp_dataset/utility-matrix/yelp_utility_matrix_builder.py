# Builds the utility matrix from the yelp_review.csv file
# specifically for Stuttgart, BW, Germany for testing.
# Can be modified to build the matrix for the entirety of the file for all 11 metropolitan areas
# Minh N. and Chen T.
# 2019.06.19

import pandas as pd
import numpy as np
import json

def yelp_utility_matrix()


def main():
	# utility_matrix('../yelp_review.csv', 'yelp_utility_matrix_stuttgart.csv')
	# aggregate_rewrite_matrix('yelp_utility_matrix_stuttgart.csv')

if __name__ == '__main__' :
	main()

# def aggregate_rewrite_matrix(data_csv):
# 	# Take a csv, groupby users, aggregate, and fix elements
# 	df = pd.read_csv(data_csv)
# 	df = df.groupby(['user_id'])
# 	df = df.agg(['sum'])
# 	df = df.replace(to_replace = 0, value = np.nan)	
# 	df.columns = df.columns.get_level_values(0)
# 	df.to_csv('yelp_utility_matrix_mesa.csv')

# def utility_matrix(data_csv, output_csv):
	
# 	# this reader was used to test the algorithm on limited chunks
# 	# reader = pd.read_csv(data_csv, iterator = True)
# 	# for i in range(700):
# 		# chunk = reader.get_chunk(300)

# 	# reads yelp_business.csv to join with chunks
# 	df_business = pd.read_csv('../yelp_business.csv')
# 	df_business = df_business[['business_id','city']]

# 	df_list = []
# 	df = pd.DataFrame()

# 	for chunk in pd.read_csv(data_csv, chunksize = 500):
# 		chunk = pd.merge(chunk, df_business, on = 'business_id')
# 		chunk = chunk[chunk.city == 'Stuttgart']
# 		chunk = pd.pivot_table(chunk, values = 'stars', index = 'user_id', columns = 'business_id')
# 		df_list.append(chunk)
# 	# The following commented code can replace the uncommented code
# 	# The while loop concats one chunk at a time, which can save on a little memory but requires more computational time
# 	# del df_business
# 	# while df_list:
# 		# df = pd.concat([df, df_list.pop()], sort = False)
# 	df.to_csv(output_csv)
# 	df = pd.concat(df_list, sort = False)
