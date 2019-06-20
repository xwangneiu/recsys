# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 11:09:01 2019

@author: jonathan
"""
#Given a data csv in the format given by MovieLens (tab-delimited columns containing user, item, rating, and timestamp, respectively), return a pandas utility_matrix, or export a csv, if export_csv_or_not is set to True
def utility_matrix(data_csv, output_csv_filename, exporting_csv):
    import pandas as pd
    
    #import u.data file
    df = pd.read_csv(data_csv, sep='\t', names=['user', 'movie', 'rating', 'timestamp'])
    
    #remove timestamp -- not needed
    del df['timestamp']
    
    #create utility matrix using pivot table
    utility_matrix = df.pivot_table(index='user', columns='movie', values='rating')
    
    #export as csv
    if exporting_csv:
        utility_matrix.to_csv(output_csv_filename)
    return utility_matrix
    
def main():
    utility_matrix('../u.data', 'movielens_utility_matrix.csv')

if __name__ == '__main__':
    main()