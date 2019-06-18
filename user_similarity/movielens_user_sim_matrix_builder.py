# SCSE RecSys Group
# Minh N. and Chen T.
# 19.06.18
import pandas as pd
import numpy as np


# Read the utility matrix file (derived from u.data) and 
# transpose so the users are columns and items are rows.
def user_similarity(data_csv, output_csv):
	df = pd.read_csv(data_csv, header=0, index_col=0)
	df = df.transpose()

	print(df)

def main():
    user_similarity('../datasets/ml-100k/utility-matrix/movielens_utility_matrix.csv', 'movielens_user_sim_matrix.csv')

if __name__ == '__main__':
    main()