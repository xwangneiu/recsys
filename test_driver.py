# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 15:33:23 2019

@author: jonathan
"""

import sys
#WHENEVER WE ADD A NEW ALGORITHM, WE NEED TO ADD PATH OF ANY PYTHON FILES WITH FUNCTIONS WE ARE USING TO THIS LIST OF PATHS
sys.path.insert(0, '/item_similarity')

import item_similarity.movielens_predictor_item as mlp_item

#just asks for a user and an item to input to an algorithm
def query_user_item():
    user = int(input("Enter user: "))
    item = int(input("Enter item: "))
    return user, item

def main():
    
    #main Test Driver loop: select a dataset
    run = True
    sorry = 'Sorry, test driver not implemented yet for this algorithm\n'
    print('RECOMMENDER SYSTEMS TEST DRIVER')
    print('Get a prediction for a given user and item, using a choice of algorithms')
    while (run):
        print('\nChoose Dataset:\n')
        print('1--MovieLens 100k 2--Yelp (sample) 0--Quit')
        response_dataset = int(input(": "))
        
        #Quit
        if response_dataset == 0:
            run = False
        
        #MovieLens Dataset test driver loop
        if response_dataset == 1:
            run_ml = True
            
            #loading item-based matrices only once
            utility, similarity = mlp_item.load_matrices_for_prediction('item_similarity/test_only_similarity_matrix.csv', 'datasets/ml-100k/utility-matrix/movielens_utility_matrix.csv')
            
            while(run_ml):
                print('MovieLens 100k Data Set:\n1--Get Actual (Observed) Rating of Film 2--Get Item-Based Prediction 3--Get User-Based Prediction 4--Get WNMF-Based Prediction 0--Back')
                response_ml = int(input(": "))
                #query actual rating of film 
                if response_ml == 1:
                    print(sorry)
                #query item-based MovieLens predictor
                elif response_ml == 2:
                        user, item = query_user_item()
                        print("PREDICTION for USER " + str(user) + " on ITEM " + str(item) + ": " + str(mlp_item.predict(utility, similarity, user, item)))
                        print('\n')
                elif response_ml == 3:
                    print(sorry)
                elif response_ml == 4:
                    print(sorry)
                #quit
                elif response_ml == 0:
                    run_ml = False
        
        #Yelp Dataset test driver loop
        elif response_dataset == 2:
            run_yelp = True
            while(run_yelp):
                print('\nYelp (sample):\n 1--Get Actual (Observed) Rating of Business 2--Get Item-Based Prediction 3--Get User-Based Prediction 4--Get WNMF-Based Prediction 0--Back')
                response_yelp = int(input(": "))
                
                #Query actual (observed) rating of business
                if response_yelp == 1:
                    print(sorry)
                elif response_yelp == 2:
                    print(sorry) 
                elif response_yelp == 3:
                    print(sorry)
                elif response_yelp == 4:
                    print(sorry)
                    
                #quit
                elif response_yelp == 0:
                    run_yelp = False
    
if __name__ == '__main__':
    main()