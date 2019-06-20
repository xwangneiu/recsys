# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 13:01:30 2019

@author: jonathan
"""
import numpy as np
import pandas as pd

#ITEM-BASED MOVIELENS PREDICTOR
#Not the ultimate code we will be using, since we are coding Pearson correlation / cosine distance ourselves: just a test to see if the predictor works with a similarity matrix
#this just uses .corrwith so we can test the predictor
#it also takes about 20 minutes to run.
def build_test_similarity_matrix(utility_matrix_csv, similarity_matrix_csv_output):
    utility = pd.read_csv(utility_matrix_csv)

    #create first column/dataframe
    row = utility.corrwith(utility['1'])
    row = pd.DataFrame(row, columns=['1'])
    similarity = row.drop('user')
                       
    def get_item_corrs(item):
        item = str(item)
        row = utility.corrwith(utility[item])
        row = row.drop('user')
        return row
    
    for i in range(2, len(utility.columns)):
        if i % 10 == 0:
            print('Correlating item ' + str(i) + '...')
        similarity[str(i)] = get_item_corrs(i)
        
    print(similarity)
    similarity.to_csv(similarity_matrix_csv_output)
    
def predictor(similarity_matrix_csv, utility_matrix_csv, user, item):

    #import item-item similarity matrix. INDICES OK
    similarity = pd.read_csv(similarity_matrix_csv, index_col=0)
    
    #import utility matrix. INDICES OK
    utility = pd.read_csv(utility_matrix_csv)
    utility = utility.set_index('user')
    #correct data type of item parameter to string as required to query dataframe below
    item = str(item)

    #similarity of all items to active item. INDICES OK
    item_similarity = pd.DataFrame(similarity[item])
    
    #all ratings on items given by active user. SELECTS CORRECT USER ROW
    user_ratings = pd.DataFrame(utility.iloc[user - 1])
    
    #print(user_ratings.iat[int(item) - 1, 0]) #THIS IS HOW TO CORRECTLY SELECT THE RATING FOR A FILM item

    #print(user_ratings.shape[0])  #THIS IS HOW TO CORRECTLY GET THE NUMBER OF ROWS IN A DATAFRAME

    #get weighted ratings (each item rating by the active user * that item's correlation with the active item). INDICES OK
    
    weighted_ratings = np.zeros(user_ratings.shape[0], dtype=float)
    
    for i in range(len(weighted_ratings)):
        weighted_ratings[i] = float(item_similarity.iat[i, 0] * user_ratings.iat[i, 0])
    
    weighted_ratings = pd.DataFrame(weighted_ratings, columns=['weighted_rating'])

    weighted_ratings.index = user_ratings.index #replace weighted_ratings labels (which were off by one) INDICES OK
    
#    print('user ratings: ')
#    print(user_ratings)
#    print('Weighted Ratings: ')
#    print(weighted_ratings)
    
    #take absolute value for denominator of Simple Weighted Average function
    item_similarity_abs = item_similarity.apply(abs) #WORKS CORRECTLY
    
#    print('similarity absolute values before: ')
#    print(item_similarity_abs.head(20))
#    
#    print('user ratings: ')
#    print(user_ratings.head(20))
    
    #remove items not reviewed by user from item row of similarity matrix. WORKS CORRECTLY
    
    for i in range(user_ratings.shape[0]):
        if not user_ratings.iat[i, 0] > 0:
           item_similarity_abs.iat[i, 0] = 0
           
#    print('similarity absolute values after: ')
#    print(item_similarity_abs.head(20))
#    
#    print('weighted ratings:')
#    print(weighted_ratings.head(20))
    
    weighted_ratings_sum = float(weighted_ratings.sum()[0])
    
    item_correlations_abs_sum = float(item_similarity_abs.sum()[0])
    
    prediction = weighted_ratings_sum / item_correlations_abs_sum
    
    print('RATING PREDICTION for USER ' + str(user) + ' on ITEM ' + item + ': ' + str(prediction))
#    #print(item_similarity_abs.sum()[0])
#    print("User Ratings:")
#    print(user_ratings.head(100))
#    print("Item Similarity:")
#    print(item_similarity_abs.head(100))
#    print(weighted_ratings)
#    print("user rat: ")
#    print(user_ratings.iloc[1][0])

    
        
    #CREATE LIST OF USER RATINGS ON K MOST SIMILAR ITEMS
        
    #CREATE LIST CONTAINING USER RATINGS * CORRELATION

def main():
    user = int(input("Please enter the User ID of the active user: "))
    item = int(input("Please enter the Film ID of the desired film: "))
    
    #build_test_similarity_matrix('../datasets/ml-100k/utility-matrix/movielens_utility_matrix.csv', 'test_only_similarity_matrix.csv')
    
    #build test driver that takes in lists and 
    predictor('test_only_similarity_matrix.csv', '../datasets/ml-100k/utility-matrix/movielens_utility_matrix.csv', user, item)
    
if __name__ == '__main__':
    main()
    
    
        
        
        