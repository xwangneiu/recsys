# SCSE RecSys Group
# Minh N.
# 19.06.27
# This module finds the specified entries of a column and builds a new csv from rows including that
# This is written to pull Urbana-Champaign businesses out from the yelp_review.csv
# for testing against ratings on businesses with zipcodes listed in urbana_zip.json

import pandas as pd
import numpy as np
import json

def shuffle(data_csv):
	df = pd.read_csv(data_csv)
	df = df.drop(['postal_code'], axis = )
	df = df.sample(frac=1).reset_index(drop=True)
	return df

def build_test_sets(data_csv, set_name):
	
	df = shuffle(data_csv)
	partitions = []

	size = int(len(df.index))
	for i in range(0,size,(size//5)):
		partitions.append(df[i:i + (size//5)])
	for num, part in enumerate(partitions, start = 1):
		training_set = partitions.copy()
		del training_set[num-1]
		output_path = set_name + '_training_' + str(num) + '.csv'
		df = pd.concat(training_set)
		df.to_csv(output_path, index = False)
		output_path = set_name + '_testing_' + str(num) + '.csv'
		part.to_csv(output_path, index = False)

def extract_entries(data_csv, output_path):
	with open('utility-matrix/urbana_zip.json', 'r') as f:
		zip_list = json.load(f)
	businesses = pd.read_csv('yelp_business.csv')
	businesses = businesses[['business_id', 'postal_code']]
	businesses = businesses[businesses.postal_code.isin(zip_list)]
	ls = []
	for chunk in pd.read_csv(data_csv, chunksize = 500):
		chunk = chunk[['user_id', 'business_id', 'stars']]
		chunk = chunk.merge(businesses, on = 'business_id')
		chunk = chunk[chunk.postal_code.isin(zip_list)]
		ls.append(chunk)
	df = pd.concat(ls)
	df.to_csv(output_path, index = False)

def main():
	# extract_entries('yelp_review.csv','yelp_review_uc.csv')
	# build_test_sets('yelp_review_uc.csv', 'yelp_review_uc')

if __name__ == '__main__':
	main()