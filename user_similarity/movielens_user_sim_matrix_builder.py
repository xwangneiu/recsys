# SCSE RecSys Group
# Minh N. and Chen T.
# 19.06.18
import pandas as pd
import numpy as np

# Read the utility matrix file (derived from u.data) and 
# transpose so the users are columns and items are rows.
# Returns to the matrix building callers
def transpose_matrix(data_csv):
	df = pd.read_csv(data_csv, header=0, index_col=0)
	df.transpose()
	return df

# Builds a sim. matrix with cosine distance
def user_similarity_cosine(data_csv, output_csv):
	df = transpose_matrix(data_csv)
	# Dot product of vector of two users over the magnitude 
	# (root of the squares of vector components, multiplied with each other)


# Builds a sim. matrix with Pearson correlation
def user_similarity_pearson(data_csv, output_csv):
	df = transpose_matrix(data_csv)

def main():
    user_similarity_cosine('../datasets/ml-100k/utility-matrix/movielens_utility_matrix.csv', 'movielens_user_sim_matrix_cosine.csv')
    user_similarity_pearson('../datasets/ml-100k/utility-matrix/movielens_utility_matrix.csv', 'movielens_user_sim_matrix_pearson.csv')

if __name__ == '__main__':
    main()