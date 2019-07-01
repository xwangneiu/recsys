# Builds the utility matrix from the yelp_review.csv file
# This takes a zipcode list (.json) and builds UM with only reviews from those businesses there
# The resulting .json is a dictionary of dictionaries
# This one has items as the main key to a dictionary that has users as the keys to the rating
# Minh N. and Chen T.
# 2019.06.19, updated 06.25

import pandas as pd
import numpy as np
import json

def yelp_utility_matrix(df, output_json, json_file_path = 'urbana_zip.json'):
	output_dict = {}

	for j in range(len(df.index)):
		curr = df.iloc[j]
		if curr.business_id in output_dict.keys():
			output_dict[curr.business_id][curr.user_id] = int(curr.stars)
		else:
			output_dict[curr.business_id] = {curr.user_id: int(curr.stars)}
	with open(output_json, 'w') as f:
		json_dump = json.dumps(output_dict)
		f.write(json_dump)
		f.close()
	return output_dict

def main():
	df = pd.read_csv('../yelp_review_uc_training_1.csv')
	yelp_utility_matrix(df, 'yelp_utility_matrix_uc_item_tr1.json')

if __name__ == '__main__' :
	main()

# def yelp_utility_matrix(df, output_json, json_file_path = 'urbana_zip.json'):
# 	with open(json_file_path, 'r') as f:
# 		try:
# 			zip_list = json.load(f)
# 		except:
# 			print('Zip file for building UM possibly empty. Returning to caller.')
# 			return
# 	# businesses = pd.read_csv('../yelp_business.csv')
# 	output_dict = {}
# 	for chunk in df:
# 		# chunk = chunk.merge(businesses[['business_id', 'postal_code']], on = 'business_id')
# 		# chunk = chunk[chunk.postal_code.isin(zip_list)]
# 		for j in range(len(chunk.index)):
# 			# Could optmize accessing each row? iterrow() was not working at the time
# 			curr = chunk.iloc[j]
# 			if curr.business_id in output_dict.keys():
# 				output_dict[curr.business_id][curr.user_id] = int(curr.stars)
# 			else:
# 				output_dict[curr.business_id] = {curr.user_id: int(curr.stars)}
# 	with open(output_json, 'w') as f:
# 		json_dump = json.dumps(output_dict)
# 		f.write(json_dump)
# 		f.close()
# 	return output_dict

# def main():
# 	df = pd.read_csv('../yelp_review.csv', chunksize = 500)
# 	yelp_utility_matrix(df, 'yelp_utility_matrix_uc_item.json')