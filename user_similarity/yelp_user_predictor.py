# SCSE RecSys Group
# Minh N.
# 19.07.01
# This module takes a list of user-item-ratings and predicts ratings for each row based off of 
# the similarity and utility matrix.

import pandas as pd
import numpy as np
import math
import json


def load_files(training_um_path, training_sm_path, test_set_path):
	with open(training_um_path, 'r') as f:
		training_um = json.load(f)
	with open(training_sm_path, 'r') as f:
		training_sm = json.load(f)
	test_set = pd.read_csv(test_set_path)
	return training_um, training_sm, test_set

def predict(training_um, training_sm, test_set, output_file_path):
	
	test_set = test_set.drop(['Unnamed: 0', 'postal_code', 'Unnamed: 0.1'], axis = 1)
	test_set['prediction'] = math.nan
	# For all lines in test set
	#	take the u1 in the test set
	# 	get all similarities of u1 from the sim matrix
	#	take the b1 from the test set
	#	get all ratings given by users from the UM if they've rated b1 into a list
	#	if no one in u1's similarities rated b1, return NaN
	#	if there are ratings, run it through simple weighted average ((Sum of W * R)/(sum of |W|))
	#	add result to column
	for num, (user, business) in enumerate(zip(test_set['user_id'], test_set['business_id']), start = 0):
		if user not in training_sm.keys():
			continue
		similarities = training_sm[user]

		# CURRENT ISSUES:
		# Test_set entries are being added by copy, which may cause issues?
		# The training/test sets aren't split such that there is a guarantee of a person being in the training set

		# This is a map of users' ratings for the business.
		ratings = {}
		for key in similarities.keys():
			if business in training_um[key]:
				ratings[key] = training_um[key][business]
		if len(ratings) == 0:
			continue
		else:
			numerator = 0
			denominator = 0
			for key, value in ratings.items():
				numerator += float(value * similarities[key])
				denominator += float(abs(similarities[key]) + 0.0000001)
		test_set['prediction'][num] = (numerator / denominator)
	print(test_set)
	return test_set

def main():
	training_um, training_sm, test_set = load_files('../datasets/yelp_dataset/utility-matrix/yelp_utility_matrix_uc_user_tr1.json','yelp_user_sim_matrix_cosine_tr1.json','../datasets/yelp_dataset/yelp_review_uc_testing_1.csv')
	predict(training_um, training_sm, test_set, 'yelp_user_prediction_cosine_1.csv')
	with open('yelp_user_sim_matrix_pearson_tr1.json', 'r') as f:
		training_sm = json.load(f)
	predict(training_um, training_sm, test_set, 'yelp_user_prediction_pearson_1.csv')	

if __name__ == '__main__':
	main()