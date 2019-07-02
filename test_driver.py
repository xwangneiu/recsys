# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 15:33:23 2019

@author: jonathan
"""

import sys
#WHENEVER WE ADD A NEW ALGORITHM, WE NEED TO ADD PATH OF ANY PYTHON FILES WITH FUNCTIONS WE ARE USING TO THIS LIST OF PATHS
sys.path.insert(0, '/item_similarity')

import datasets


#just asks for a user and an item to input to an algorithm
def query_user_item():
    user = int(input("Enter user: "))
    item = int(input("Enter item: "))
    return user, item

#def build_results_table():
    

def run_test(data_source, test_source, name, data, algo, sim):
    results_folder = str(algo)
    data_utility_dir = None
    filetype = None
    if data == 'ml':
        data_utility_dir = 'datasets/ml-100k/utility-matrix/'
        filetype = 'csv'
    elif data == 'yelp':
        data_utility_dir = 'datasets/yelp_dataset/utility-matrix/'
        filetype = 'json'
    if algo == 'user' or algo == 'item':
        results_folder += '_similarity/'
    elif algo == 'wnmf':
        results_folder += '/'
    ds = datasets.TrainingAndTest(data + ' training/test sets')
    ds.training = datasets.Dataset(
        name,                                              #name
        data_source,                             #original source
        data_utility_dir + str(name) + '_' + str(algo) + '_um.' + filetype,    #utility matrix
        results_folder + str(name) + '_' + str(algo) + '_' + str(sim) + '_sm.' + filetype,            #similarity matrix
        data,                                             #data source
        algo,                                             #algorithm
        sim)                                              #correlation
    ds.test = datasets.TestSet(
        str(name) + ' test set',                                          #name
        test_source, data)
    if data == 'ml':
        if algo == 'item':
            ds.build_ml_item_predictions_df('item_similarity/' + str(name) + '_' + str(algo)  + '_' + str(sim) + '_predictions.csv')
        elif algo == 'user':
            ds.build_ml_user_predictions_df('user_similarity/' + str(name) + '_' + str(algo)  + '_' + str(sim) + '_predictions.csv')
        elif algo == 'wnmf':
            ds.build_ml_wnmf_predictions_df('wnmf/' + str(name) + '_' + str(algo) + '_' + str(sim) + '_predictions.csv')
    elif data == 'yelp':
        if algo == 'item':
            ds.build_yelp_item_predictions_df('item_similarity/' + str(name) + '_' + str(algo)  + '_' + str(sim) + '_predictions.csv')
        elif algo == 'user':
            ds.build_yelp_user_predictions_df('user_similarity/' + str(name) + '_' + str(algo)  + '_' + str(sim) + '_predictions.csv')
        elif algo == 'wnmf':
            ds.build_yelp_wnmf_predictions_df('wnmf/' + str(name) + '_' + str(algo) + '_' + str(sim) + '_predictions.csv')
    print('Predictions: ')
    print(ds.test.predictions_df)
    ds.test.calculate_mae()
    ds.test.calculate_rmse()
    print("MAE: " + str(ds.test.mae))
    print("RMSE: " + str(ds.test.rmse))
    return ds

def main():
    
    #main Test Driver loop: select a dataset
    run = True
    sorry = 'Sorry, test driver not implemented yet for this algorithm\n'
    print('RECOMMENDER SYSTEMS TEST DRIVER')
    print('Get a prediction for a given dataset, using a choice of algorithms')
    while (run):
        print('\nChoose Dataset Type:\n')
        print('1--MovieLens 100k 2--Yelp (Champaign-Urbana) 0--Quit')
        response_dataset = int(input(": "))
        
        #Quit
        if response_dataset == 0:
            run = False
        
        #MovieLens Dataset test driver loop
        if response_dataset == 1:
            run_ml = True
            
            #loading item-based matrices only once
            while(run_ml):
                print('Select Algorithm for MovieLens 100k Data Sets:\n1--Item-Based Pearson 2--Item-Based Cosine 3--User-Based Pearson 4--User-Based Cosine 5--WNMF')
                response_ml = int(input(": "))
                if response_ml == 0:
                    run_ml = False
                    break
                print('Select MovieLens 100k Test Set 1-5 for Prediction')
                algo_choice = None
                sim_choice = None
                dataset_choice = int(input(": "))
                if dataset_choice < 1 or dataset_choice > 5:
                    print("Invalid dataset selection")
                if response_ml == 1:
                    algo_choice = 'item'
                    sim_choice = 'pearson'
                #query item-based MovieLens predictor
                elif response_ml == 2:
                    algo_choice = 'item'
                    sim_choice = 'cosine'
                elif response_ml == 3:
                    algo_choice = 'user'
                    sim_choice = 'pearson'
                elif response_ml == 4:
                    algo_choice = 'user'
                    sim_choice = 'cosine'
                elif response_ml == 5:
                    print(sorry)
                if response_ml <= 5:
                    ds = run_ml_test('datasets/ml-100k/u' + str(dataset_choice) + '.base',  #training set source
                                'datasets/ml-100k/u' + str(dataset_choice) + '.test',       #test set source
                                'ml_u' + str(dataset_choice),                               #dataset name
                                'ml',                                                       #type of data
                                algo_choice,                                                #algorithm
                                sim_choice)                                                 #similarity measure
                    
        #Yelp Dataset test driver loop
        elif response_dataset == 2:
            run_yelp = True
            while(run_yelp):
                print('Select Algorithm for Yelp Champaign-Urbana Data Sets:\n1--Item-Based Pearson 2--Item-Based Cosine 3--User-Based Pearson 4--User-Based Cosine 5--WNMF')
                algo_choice = None
                sim_choice = None
                response_yelp = int(input(": "))
                if response_yelp == 0:
                    run_yelp = False
                    break
                print('Select MovieLens 100k Test Set 1-5 for Prediction')
                dataset_choice = int(input(": "))
                if dataset_choice < 1 or dataset_choice > 5:
                    print("Invalid dataset selection")
                if response_yelp == 1:
                    algo_choice = 'item'
                    sim_choice = 'pearson'
                #query item-based MovieLens predictor
                elif response_yelp == 2:
                    algo_choice = 'item'
                    sim_choice = 'cosine'
                elif response_yelp == 3:
                    algo_choice = 'user'
                    sim_choice = 'pearson'
                elif response_yelp == 4:
                    algo_choice = 'user'
                    sim_choice = 'cosine'
                elif response_yelp == 5:
                    print(sorry)
                if response_yelp <= 5:
                    ds = run_test('datasets/yelp_dataset/yelp_review_uc_training_' + str(dataset_choice) + '.csv',  #training set source
                                'datasets/yelp_dataset/yelp_review_uc_testing_' + str(dataset_choice) + '.csv',       #test set source
                                'yelp_set' + str(dataset_choice),                               #dataset name
                                'yelp',                                                       #type of data
                                algo_choice,                                                #algorithm
                                sim_choice)                                                 #similarity measure
    
if __name__ == '__main__':
    main()