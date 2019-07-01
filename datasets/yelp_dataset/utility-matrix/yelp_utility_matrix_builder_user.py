# Builds the utility matrix from the yelp_review.csv file
# This takes a zipcode list (.json) and builds UM with only reviews from those businesses there
# The resulting .json is a dictionary of dictionaries
# This one has users as the main key to a dictionary that has items as the keys to the rating
# Minh N. and Chen T.
# 2019.06.19, updated 06.25

import pandas as pd
import numpy as np
import json

def yelp_utility_matrix(df, output_json, json_file_path = 'urbana_zip.json'):
	with open(json_file_path, 'r') as f:
		try:
			zip_list = json.load(f)
		except:
			print('Zip file for building UM possibly empty. Returning to caller.')
			return
	businesses = pd.read_csv('../yelp_business.csv')
	output_dict = {}
	for chunk in df:
		chunk = chunk.merge(businesses[['business_id', 'postal_code']], on = 'business_id')
		chunk = chunk[chunk.postal_code.isin(zip_list)]
		for j in range(len(chunk.index)):
			# Could optmize accessing each row? iterrow() was not working at the time
			curr = chunk.iloc[j]
			if curr.user_id in output_dict.keys():
				output_dict[curr.user_id][curr.business_id] = int(curr.stars)
			else:
				output_dict[curr.user_id] = {curr.business_id: int(curr.stars)}
	with open(output_json, 'w') as f:
		json_dump = json.dumps(output_dict)
		f.write(json_dump)
		f.close()
	return output_dict

def main():
	df = pd.read_csv('../yelp_review_uc_training_5.csv', chunksize = 500)
	yelp_utility_matrix(df, 'yelp_utility_matrix_uc_user_training_5.json')

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
