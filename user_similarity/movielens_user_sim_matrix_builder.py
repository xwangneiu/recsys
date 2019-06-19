# SCSE RecSys Group
# Minh N. and Chen T.
# 19.06.18
import pandas as pd
import numpy as np
import math

# Read the utility matrix file (derived from u.data) and 
# transpose so the users are columns and items are rows.
# Returns to the matrix building callers
def transpose_matrix(data_csv):
	df = pd.read_csv(data_csv, header=0, index_col=0)
	df = df.transpose()
	return df

# Builds a sim. matrix with cosine distance
def user_similarity_cosine(data_csv, output_csv):
	input_df = transpose_matrix(data_csv)
	# Dot product of vector of two users over the magnitude 
	# (root of the squares of vector components, multiplied with each other)

	# For loop through column, comparing it with every other column
	output_df = pd.DataFrame()
	for column_i in input_df:
		cos_corr_list = []
		for column_j in input_df:
			dot_product = input_df[column_i].multiply(input_df[column_j])
			cos_corr = dot_product.sum() / (math.sqrt(input_df[column_i].multiply(input_df[column_i]).sum()) * math.sqrt(input_df[column_j].multiply(input_df[column_j]).sum()))
			cos_corr_list.append(cos_corr)
		outputdf = output_df.append(pd.Series(cos_corr_list), ignore_index=True)	
	print(output_df.head())

# Builds a sim. matrix with Pearson correlation
def user_similarity_pearson(data_csv, output_csv):
	df = transpose_matrix(data_csv)

def main():
    user_similarity_cosine('../datasets/ml-100k/utility-matrix/movielens_utility_matrix.csv', 'movielens_user_sim_matrix_cosine.csv')
    user_similarity_pearson('../datasets/ml-100k/utility-matrix/movielens_utility_matrix.csv', 'movielens_user_sim_matrix_pearson.csv')

if __name__ == '__main__':
    main()