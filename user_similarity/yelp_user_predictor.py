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
	
	# give non-predictable rows math.nan
	# drop columns so the format is user, item, observced rating, predicted.
	return

def main():
	training_um, training_sm, test_set = load_files('../datasets/yelp_dataset/utility-matrix/yelp_utility_matrix_uc_user_tr1','','')
	predict(training_um, training_sm, test_set, 'yelp_user_prediction_cosine.csv')

if __name__ == '__main__':
	main()