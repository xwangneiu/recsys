# SCSE RecSys Group
# Minh N. and Chen T.
# 19.06.18
import pandas as pd
import numpy as np


# Read the utility matrix file (derived from u.data) and 
# transpose so the users are columns and items are rows.
def user_similarity(data_csv, output_csv):
	df = pd.read_csv(data_csv)
	df = df.transpose()

	df.head()

def main():
    utility_matrix('../datasets/ml-100k/utility-matrix/movielens_utility_matrix', 'movielens_user_sim_matrix.csv')

if __name__ == '__main__':
    main()