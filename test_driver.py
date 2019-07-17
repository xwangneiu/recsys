# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 15:33:23 2019

@author: jonathan
"""

import sys
sys.path.insert(0, '/item_similarity')
import datasets
import time

def run_test(data_source, test_source, name, data, algo, sim, latent_factors, iterations):
    t1 = time.time()
    results_folder = str(algo)
    data_utility_dir = None
    filetype = None
    if data == 'ml':
        data_utility_dir = 'datasets/ml-100k/utility-matrix/'
        filetype = 'csv'
        ds = datasets.TrainingAndTest(data + ' training/test sets')
        ds.training = datasets.Dataset(
            name,                                             #name
            data_source,                                      #original source
            data_utility_dir + str(name) + '_' + str(algo) + '_um.' + filetype,    #utility matrix
            results_folder + str(name) + '_' + str(algo) + '_' + str(sim) + '_sm.' + filetype,            #similarity matrix (or u and v matrices filename after u_ and v_ respectively)
            data,                                             #data source
            algo,                                             #algorithm
            sim,
            latent_factors,
            iterations)
        ds.test = datasets.TestSet(
            str(name) + ' test set',                                          #name
            test_source, data)
    elif data == 'yelp':
        data_utility_dir = None
        filetype = None
        um_location = None
        if algo == 'wnmf':
            data_utility_dir = 'datasets/yelp_dataset/'
            filetype = 'csv'
            um_location = data_source
        else:
            data_utility_dir = 'datasets/yelp_dataset/utility-matrix/'
            filetype = 'json'
            um_location = data_utility_dir + 'yelp_review_uc_training_um' + str(algo) + '_um.' + filetype
        ds = datasets.TrainingAndTest(data + ' training/test sets')
        ds.training = datasets.Dataset(
            name,                                             #name
            data_source,                                      #original source
            um_location,    #utility matrix
            results_folder + str(name) + '_' + str(algo) + '_' + str(sim) + '_sm.' + filetype,            #similarity matrix (or u and v matrices filename after u_ and v_ respectively)
            data,                                             #data source
            algo,                                             #algorithm
            sim,
            latent_factors,
            iterations)
        ds.test = datasets.TestSet(
            str(name) + ' test set',                                          #name
            test_source, data)
            
    if algo == 'user' or algo == 'item':
        results_folder += '_similarity/'
    elif algo == 'wnmf':
        results_folder += '/'
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
    if data == 'ml':
        ds.test.calculate_ml_mae()
        ds.test.calculate_ml_rmse()
    elif data == 'yelp':
        ds.test.calculate_yelp_mae()
        ds.test.calculate_yelp_rmse()
    print("MAE: " + str(ds.test.mae))
    print("RMSE: " + str(ds.test.rmse))
    print('Run time: ' + str(time.time() - t1) + ' sec')
    log_entry = str(t1) + ',' + name + ',' + data + ',' + algo + ',' + sim + ',' + str(latent_factors) + ',' + str(ds.training.predictor_log) + ',' + str(time.time() - t1) + ',' + str(ds.test.mae) + ',' + str(ds.test.rmse) + ',\n'
    return ds, log_entry

def record_in_log_file(data, algo, sim, log_entry, log_name=''):
    filename = ''
    if algo == 'item' or algo == 'user':
        filename += algo + '_similarity/'
    elif algo == 'wnmf':
        filename += 'wnmf/'
    header = 'Timestamp,Data Set,Data Source,Algorithm,Similarity Measure,Latent Factors,Iterations,Final Change,Runtime,MAE,RMSE,\n'
    print("about to add to logs: " + log_entry)
    
    date = time.strftime('%Y_%d_%b')
    filename += data + '_' + date + '_test_logs_' + log_name + '.csv'
    try:
        f = open(filename, 'r')
        f.close()
        f = open(filename, 'a')
        f.write(log_entry)
        f.close()
    except FileNotFoundError:
        f = open(filename, 'w')
        f.write(header + log_entry)
        f.close()    
    print (filename)

def automated_wnmf_test_ml():
    datasets = [1, 2, 3, 4, 5]
    latent_factors = [1, 2, 3, 4, 5, 7, 10, 12, 15, 20, 25, 30, 40, 50]
    for d in datasets:
        for f in latent_factors:
            for i in range(1, 31):
                ds, log_entry = run_test('datasets/ml-100k/u' + str(d) + '.base',  #training set source
                                    'datasets/ml-100k/u' + str(d) + '.test',       #test set source
                                    'ml_u' + str(d),                               #dataset name
                                    'ml',                                                       #type of data
                                    'wnmf', #algo                                                #algorithm
                                    'wnmf', #sim                                                #similarity measure
                                    f,  #latent factors
                                    i)  #iterations
                data_source = 'ml'
                record_in_log_file(data_source, 'wnmf', 'wnmf', log_entry)

def automated_wnmf_test_yelp():
    datasets = [1, 2, 3, 4, 5]
    latent_factors = [1, 2, 3, 4, 5, 7, 10, 12, 15, 20, 25, 30, 40, 50]
    dataset_choice = 'yelp'
    algo_choice = 'wnmf'
    sim_choice = 'wnmf'
    for d in datasets:
        for f in latent_factors:
            for i in range(1, 31):
                ds, log_entry = run_test('datasets/yelp_dataset/yelp_review_uc_training_um_' + str(d) + '.csv',  #training set source
                                'datasets/yelp_dataset/yelp_review_uc_testing_' + str(d) + '.csv',       #test set source
                                'yelp_set' + str(d),                               #dataset name
                                'yelp',                                                       #type of data
                                algo_choice,                                                #algorithm
                                sim_choice,
                                f,
                                i)
                record_in_log_file('yelp', algo_choice, sim_choice, log_entry)
                


def test_driver():
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
            #only relevant to WNMF
            latent_factors = 3
            iterations = 25
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
                    algo_choice = 'wnmf'
                    sim_choice = 'wnmf'  
                    change_params = input('Would you like to change the current setting for the number of latent factors (' + str(latent_factors) + ') or iterations (' + str(iterations) + '), y/n? ')
                    if change_params == 'y':
                        latent_factors = int(input('Latent factors: '))
                        iterations = int(input('Iterations: '))
                if response_ml <= 5:
                    ds, log_entry = run_test('datasets/ml-100k/u' + str(dataset_choice) + '.base',  #training set source
                                'datasets/ml-100k/u' + str(dataset_choice) + '.test',       #test set source
                                'ml_u' + str(dataset_choice),                               #dataset name
                                'ml',                                                       #type of data
                                algo_choice,                                                #algorithm
                                sim_choice,                                                 #similarity measure
                                latent_factors,
                                iterations)
                    data_source = 'ml'
                    record_in_log_file(data_source, algo_choice, sim_choice, log_entry)
        #Yelp Dataset test driver loop
        elif response_dataset == 2:
            run_yelp = True
            latent_factors = 3
            iterations = 25
            while(run_yelp):
                print('Select Algorithm for Yelp Champaign-Urbana Data Sets:\n1--Item-Based Pearson 2--Item-Based Cosine 3--User-Based Pearson 4--User-Based Cosine 5--WNMF')
                algo_choice = None
                sim_choice = None
                response_yelp = int(input(": "))
                if response_yelp == 0:
                    run_yelp = False
                    break
                print('Select Yelp Test Set 1-5 for Prediction')
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
                    algo_choice = 'wnmf'
                    sim_choice = 'wnmf'  
                    change_params = input('Would you like to change the current setting for the number of latent factors (' + str(latent_factors) + ') or iterations (' + str(iterations) + '), y/n? ')
                    if change_params == 'y':
                        latent_factors = int(input('Latent factors: '))
                        iterations = int(input('Iterations: '))
                if response_yelp <= 5:
                    if response_yelp <= 4:
                        ds, log_entry = run_test('datasets/yelp_dataset/yelp_review_uc_training_' + str(dataset_choice) + '.csv',  #training set source
                                    'datasets/yelp_dataset/yelp_review_uc_testing_' + str(dataset_choice) + '.csv',       #test set source
                                    'yelp_set' + str(dataset_choice),                               #dataset name
                                    'yelp',                                                       #type of data
                                    algo_choice,                                                #algorithm
                                    sim_choice,
                                    latent_factors,
                                    iterations)
                    elif response_yelp == 5:
                        ds, log_entry = run_test('datasets/yelp_dataset/yelp_review_uc_training_um_' + str(dataset_choice) + '.csv',  #training set source
                                    'datasets/yelp_dataset/yelp_review_uc_testing_' + str(dataset_choice) + '.csv',       #test set source
                                    'yelp_set' + str(dataset_choice),                               #dataset name
                                    'yelp',                                                       #type of data
                                    algo_choice,                                                #algorithm
                                    sim_choice,
                                    latent_factors,
                                    iterations)
                    data_source = 'yelp'
                    record_in_log_file(data_source, algo_choice, sim_choice, log_entry)
                    
    
def main():
    #test_driver()
    automated_wnmf_test_yelp()
    #create_log_file('ml_u1', 'ml', 'wnmf', 'wnmf', 'test')

if __name__ == '__main__':
    main()