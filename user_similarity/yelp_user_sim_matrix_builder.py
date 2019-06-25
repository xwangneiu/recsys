# SCSE RecSys Group
# Minh N. and Chen T.
# 19.06.18
# This module builds two user similarity matrices from a Yelp utility matrix
# The similiarities are cosine distance and Pearson Correlation

import pandas as pd
import numpy as np
import math

def transpose_matrix(data_csv):
	df = pd.read_csv(data_csv, header=0, index_col=0)
	df = df.transpose()
	return df

def user_similarity_cosine(data_csv, output_csv):
	input_df = transpose_matrix(data_csv)
	output_series = []
	for column_i in input_df:
		
		cos_corr_list = []
		for column_j in input_df:
			
			dot_product = input_df[column_i].multiply(input_df[column_j])
			cos_corr = dot_product.sum() / (math.sqrt(input_df[column_i].multiply(input_df[column_i]).sum()) * math.sqrt(input_df[column_j].multiply(input_df[column_j]).sum()))
			
			cos_corr_list.append(cos_corr)

		output_series.append(pd.Series(cos_corr_list))
	output_df = pd.concat(output_series, axis = 1)
	output_df.index = input_df.columns
	output_df.columns = input_df.columns
	output_df.to_csv(output_csv)

def user_similarity_pearson(data_csv, output_csv):
	input_df = transpose_matrix(data_csv)
	output_series = []

	for column_i in input_df:
		pearson_corr_list = []
		for column_j in input_df:

			corated_i = (input_df[column_j] / input_df[column_j]) * input_df[column_i]
			corated_j = (input_df[column_i] / input_df[column_i]) * input_df[column_j]

			mean_i = corated_i.mean()
			mean_j = corated_j.mean()

			calculated_i = corated_i - mean_i
			calculated_j = corated_j - mean_j

			numerator = (calculated_i*calculated_j).sum()
			denumerator = math.sqrt((calculated_i * calculated_i).sum()) * math.sqrt((calculated_j * calculated_j).sum())

			pearson_corr = numerator / denumerator

			pearson_corr_list.append(pearson_corr)
		output_series.append(pd.Series(pearson_corr_list))
	output_df = pd.concat(output_series, axis = 1)
	output_df.index = input_df.columns
	output_df.columns = input_df.columns
	output_df.to_csv(output_csv)

def main():
	user_similarity_cosine('../datasets/yelp_dataset/utility-matrix/yelp_utility_matrix_stuttgart.csv', 'yelp_user_sim_matrix_cosine.csv')
	# user_similarity_pearson('../datasets/yelp_dataset/utility-matrix/yelp_utility_matrix_stuttgart.csv', 'yelp_user_sim_matrix_pearson.csv')

if __name__ == '__main__':
	main()