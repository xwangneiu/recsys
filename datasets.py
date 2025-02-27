# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 18:38:50 2019

@author: jonathan
"""

'''
Dataset Class
I created this class because each dataset can be represented as an object.
Each dataset has a source csv file,
and will have a utility matrix, a similarity matrix, and a 
Objects are an easy way to bundle them together.
'''

import pandas as pd
import json
import sys
import os
sys.path.insert(0, 'datasets/yelp_dataset/utility-matrix/')

class Dataset:
    #INSTANCE VARIABLES
    #text description of dataset
    name = None
    
    #dataframe processed directly from original data file
    og_df = None
    
    #utility matrix dataframe
    um_df = None
    
    #similarity matrix dataframe
    sm_df = None    
    
    #WNMF u/v decomposed prediction matrix
    u_df = None
    v_df = None
    
    #Log data from WNMF predictor to output actual number of iterations and final change in norm
    predictor_log = None
    
    #CONSTRUCTOR
    #og - original data; um - utility matrix; sm - similarity matrix
    #Keyword Arguments: data=ml,yelp; algo=item,user,wnmf; sim=pearson,cosine,wnmf
    #latent_factors and iterations are for wnmf
    #rebuild refers to whether csv/json files for the various matrices are automatically rebuilt, or previously existing files are re-used (False)
    #elwise refers to our own elementwise WNMF algorithm, fall 2019
    def __init__(self, name, og_file, um_file, sm_file, data, algo, sim, latent_factors = 1, iterations = 7, rebuild_files = False, sklearn = False, elwise = False):
        self.name = name
        print(name + ' is being prepared...')
        if data == 'ml':
            self.og_df = self.build_ml_og_df(og_file) #function returns df
            if algo == 'item':
                self.um_df = self.build_ml_item_um(um_file, rebuild=rebuild_files) #function returns um df
            elif algo == 'user':
                self.um_df = self.build_ml_user_um(um_file, rebuild=rebuild_files) #function returns um df
                print(self.um_df)
            elif algo == 'wnmf':
                self.um_df = self.build_ml_item_um(um_file, rebuild=rebuild_files)
                
            if sim == 'pearson':
                    self.sm_df = self.build_ml_pearson_sm(sm_file, rebuild=rebuild_files) #function returns sim df
            elif sim == 'cosine':
                    self.sm_df = self.build_ml_cosine_sm(sm_file, rebuild=rebuild_files)
            elif sim == 'wnmf' and not sklearn:
                    self.u_df, self.v_df = self.build_ml_wnmf_prediction_matrix(sm_file, latent_factors, iterations, elementwise=elwise)
        elif data == 'yelp':
            self.og_df = self.build_yelp_og_df(og_file)
            if algo == 'item':
                self.um_df = self.build_yelp_item_um(um_file, rebuild=rebuild_files) #function returns um df
            elif algo == 'user':
                self.um_df = self.build_yelp_user_um(um_file, rebuild=rebuild_files) #function returns um df
            elif algo == 'wnmf':
                self.um_df = self.build_yelp_wnmf_um(um_file, rebuild=rebuild_files)
            if sim == 'pearson':
                self.sm_df = self.build_yelp_pearson_sm(sm_file, rebuild=rebuild_files) #function returns sim df
            elif sim == 'cosine':
                self.sm_df = self.build_yelp_cosine_sm(sm_file, rebuild=rebuild_files)
            elif sim == 'wnmf':
                self.u_df, self.v_df, self.predictor_log = self.build_yelp_wnmf_prediction_matrix(sm_file, latent_factors, iterations)
        
    #METHODS
    #MOVIELENS
    #build a dataframe from the source csv file #GOOD 6/25
    def build_ml_og_df(self, og_file):
        try:
            og_df = pd.read_csv(og_file, sep='\t', names=['user', 'movie', 'rating', 'timestamp'])
            del og_df['timestamp']
            print("Original MovieLens data file ready (og_df)")
            return og_df
        except FileNotFoundError:
            print("build_ml_og_df error: Original data file not at location given")
        
    
    #builds item-based utility matrix for data file at specified filename #GOOD 6/25
    #results in an item-based utility matrix with columns denoted '1', '2', '3' (strings) and rows 1, 2, 3 (integers)
    def build_ml_item_um(self, um_file, rebuild = False):
        um_df = None
        if rebuild:
            try:
                os.remove(um_file)
                print('ml_item_um file removed to rebuild')
            except FileNotFoundError:
                print('no ml_item_um file to remove, building')
        try:
            um_df = pd.read_csv(um_file, index_col = 0)
        except FileNotFoundError:
            print('Building MovieLens item-based utility matrix for the \'' + self.name + '\' dataset')
            from item_similarity import ml_item_um_builder
            um_df = ml_item_um_builder.build(self.og_df, um_file)
        print('MovieLens item-based utility matrix ready (um_df)')
        #print(um_df)
        return um_df
    
    def build_ml_user_um(self, um_file, rebuild = False):
        um_df = None
        if rebuild:
            try:
                os.remove(um_file)
                print('ml_user_um file removed to rebuild')
            except FileNotFoundError:
                print('no ml_user_um file to remove, continuing')
        try:
            um_df = pd.read_csv(um_file, index_col = 0)
        except FileNotFoundError:
            print('Building MovieLens user-based utility matrix for the \'' + self.name + '\' dataset')
            from item_similarity import ml_item_um_builder
            um_df = ml_item_um_builder.build(self.og_df, um_file)
        print('MovieLens user-based utility matrix ready')
        um_df = um_df.T
        return um_df
            
    def build_ml_pearson_sm(self, sm_file, rebuild = False):
        sm_df = None
        if rebuild:
            try:
                os.remove(sm_file)
                print('ml_pearson_sm file removed to rebuild')
            except FileNotFoundError:
                print('no ml_pearson_sm file to remove, continuing')
        try:
            sm_df = pd.read_csv(sm_file, index_col = 0)
        except FileNotFoundError:
            print('Building MovieLens Pearson correlation similarity matrix for the \'' + self.name + '\' dataset')
            import ml_pearson_sm_builder
            sm_df = ml_pearson_sm_builder.build(self.um_df, sm_file)
        print('MovieLens Pearson correlation-based similarity matrix ready (sm_df)')
        return sm_df
    
    def build_ml_cosine_sm(self, sm_file, rebuild = False):
        sm_df = None
        if rebuild:
            try:
                os.remove(sm_file)
                print('ml_cosine_sm file removed to rebuild')
            except FileNotFoundError:
                print('no ml_cosine_sm file to remove, continuing')
        try:
            sm_df = pd.read_csv(sm_file, index_col = 0)
        except FileNotFoundError:
            print('Building MovieLens cosine similarity matrix for the \'' + self.name + '\' dataset')
            import ml_cosine_sm_builder
            sm_df = ml_cosine_sm_builder.build(self.um_df, sm_file)
        print('MovieLens cosine similarity matrix ready (sm_df)')
        #print(sm_df)
        return sm_df
    
    def build_ml_wnmf_prediction_matrix(self, prediction_matrix_file, latent_factors, iterations, elementwise=False):
        u_df = None
        v_df = None
        print('Building MovieLens WMNF prediction matrix for the \'' + self.name + '\' dataset')
        if elementwise:
            from wnmf import ml_wnmf_prediction_matrix_builder_elementwise as pmbe
            u_df, v_df, log = pmbe.build(self.um_df, prediction_matrix_file, latent_factors, iterations)
        else:
            from wnmf import ml_wnmf_prediction_matrix_builder as pmb
            u_df, v_df, log = pmb.build(self.um_df, prediction_matrix_file, latent_factors, iterations)
        print('WNMF prediction matrix ready')
        self.predictor_log = log
        return u_df, v_df
    
    #YELP
    
    def build_yelp_og_df(self, og_file):
        try:
            og_df = pd.read_csv(og_file)
            print("Yelp training set loaded (og_df)")
            return og_df #this is a Pandas DataFrame
        except FileNotFoundError:
            print("build_ml_og_df error: Yelp training set file not at location given")
            
    def build_yelp_item_um(self, um_file, rebuild = False):
        um_df = None
        if rebuild:
            try:
                os.remove(um_file)
                print('yelp_item_um file removed to rebuild')
            except FileNotFoundError:
                print('no yelp_item_um file to remove, continuing')
        try:
            with open(um_file, 'r') as f:
                um_df = json.load(f)
        except FileNotFoundError:
            print('Building Yelp user-based utility matrix for the \'' + self.name + '\' dataset')
            import yelp_utility_matrix_builder_item as yumi
            um_df = yumi.build(self.og_df, um_file)
        print('Yelp item-based utility matrix ready')
        return um_df #this is a dictionary
            
    def build_yelp_user_um(self, um_file, rebuild = False):
        um_df = None
        if rebuild:
            try:
                os.remove(um_file)
                print('yelp_user_um file removed to rebuild')
            except FileNotFoundError:
                print('no yelp_user_um file to remove, continuing')
        try:
            with open(um_file, 'r') as f:
                um_df = json.load(f)
        except FileNotFoundError:
            print('Building Yelp user-based utility matrix for the \'' + self.name + '\' dataset')
            import yelp_utility_matrix_builder_user as yumu
            um_df = yumu.build(self.og_df, um_file)
        print('Yelp user-based utility matrix ready')
        return um_df #this is a dictionary
    
    def build_yelp_wnmf_um(self, um_file, rebuild = False):
        print("trying to load WNMF UM from location: " + um_file)
        um_df = None
        if rebuild:
            try:
                os.remove(um_file)
                print('yelp_wnmf_um file removed to rebuild')
            except FileNotFoundError:
                print('no yelp_wnmf_um file to remove, continuing')
        try:
            um_df = pd.read_csv(um_file, index_col = 0)
            print('Yelp WNMF utility matrix ready')
            return um_df #this is a dictionary
        except FileNotFoundError:
            print('''This Yelp WNMF UM function is not equipped to build a UM, just to load it. 
            Please build your UMs manually and point the test driver to them instead.
            Until then, you will be unable to proceed with Yelp WNMF.''')
        

    def build_yelp_pearson_sm(self, sm_file, rebuild = False):
        sm_df = None
        if rebuild:
            try:
                os.remove(sm_file)
                print('yelp_pearson_sm file removed to rebuild')
            except FileNotFoundError:
                print('no yelp_pearson_sm file to remove, continuing')
        try:
            with open(sm_file, 'r') as f:
                sm_df = json.load(f)
        except FileNotFoundError:
            import yelp_sm_builder as ysb
            print('Building Yelp Pearson similarity matrix for the \'' + self.name + '\' dataset') 
            sm_df = ysb.similarity_pearson(self.um_df, sm_file)
        return sm_df
    
    def build_yelp_cosine_sm(self, sm_file, rebuild = False):
        sm_df = None
        if rebuild:
            try:
                os.remove(sm_file)
                print('yelp_cosine_sm file removed to rebuild')
            except FileNotFoundError:
                print('no file to remove, continuing')
        try:
            with open(sm_file, 'r') as f:
                sm_df = json.load(f)
        except FileNotFoundError:
            import yelp_sm_builder as ysb
            print('Building Yelp cosine similarity matrix for the \'' + self.name + '\' dataset') 
            sm_df = ysb.similarity_cosine(self.um_df, sm_file)
        return sm_df
    
    def build_yelp_wnmf_prediction_matrix(self, prediction_matrix_file, latent_factors, iterations):
        u_df = None
        v_df = None
        print('Building MovieLens WMNF prediction matrix for the \'' + self.name + '\' dataset')
        '''
        from wnmf import yelp_prediction_matrix_builder as pmb
        u_df, v_df, log = pmb.build(self.um_df, prediction_matrix_file, latent_factors, iterations, 'datasets/yelp_dataset/utility-matrix/yelp_uc_user_id.json', 'datasets/yelp_dataset/utility-matrix/yelp_uc_item_id.json')
        '''
        from wnmf import ml_wnmf_prediction_matrix_builder as pmb
        u_df, v_df, log = pmb.build(self.um_df, prediction_matrix_file, latent_factors, iterations)
        
        print('WNMF prediction matrix ready')
        return u_df, v_df, log

#Class for training/test set pairs
#TestSet subclass inherits from Dataset superclass
class TestSet(Dataset):
    user_item_pairs_df = None
    predictions_df = None
    error_df = None
    mae = None
    rmse = None

    def build_ml_og_df(self, og_file):
        try:
            og_df = pd.read_csv(og_file, sep='\t', header=None)
            og_df.columns = ['user', 'item', 'observed', 'timestamp']
            del og_df['timestamp']
            print("Original MovieLens test set file ready (test.og_df)")
            return og_df
        except FileNotFoundError:
            print("TestSet.build_ml_og_df error: Original test set file not at location given") 
    
    def build_user_item_pairs_df(self, og_file):
        try:
            df = pd.read_csv(og_file, sep='\t', header=None)
            df.columns = ['user', 'item', 'observed', 'timestamp']
            del df['observed']
            del df['timestamp']
            print("MovieLens test user-item pairs ready (test.user_item_pairs_df)")
            return df
        except FileNotFoundError:
            print("TestSet.build_ml_og_df error: Original test set file not at location given when trying to build user_item_pairs_df") 
            
            
    def build_yelp_og_df(self, og_file):
        try:
            og_df = pd.read_csv(og_file)
            print("Yelp test set ready (test.og_df)")
            return og_df
        except FileNotFoundError:
            print("TestSet.build_ml_og_df error: Yelp test set file not at location given") 
    
    
    #NON-CONSTRUCTOR-BASED METHODS
    #takes a CSV
    #conventions do not apply to this    
    def calculate_ml_mae(self):
        from item_similarity import prediction_error_mae as mae
        self.mae = mae.calculate_mae(self.predictions_df)
        return self.mae

    def calculate_ml_rmse(self):
        from item_similarity import prediction_error_rmse as rmse
        self.rmse = rmse.calculate_rmse(self.predictions_df)
        return self.rmse
    
    def calculate_yelp_mae(self):
        from item_similarity import yelp_prediction_error_mae as ymae
        self.mae = ymae.calculate_mae(self.predictions_df)
        return self.mae

    def calculate_yelp_rmse(self):
        from item_similarity import yelp_prediction_error_rmse as yrmse
        self.rmse = yrmse.calculate_rmse(self.predictions_df)
        return self.rmse
    
    #TestSet CONSTRUCTOR
    def __init__(self, name, og_file, data, prediction_file=None):
        self.name = name
        print(name + ' is being prepared...')
        if data == "ml":
            self.og_df = self.build_ml_og_df(og_file)
            self.user_item_pairs_df = self.build_user_item_pairs_df(og_file)
        elif data == "yelp":
            self.og_df = self.build_yelp_og_df(og_file)
            self.user_item_pairs_df = self.og_df
        if prediction_file is not None:
            self.predictions_df = self.build_predictions_df(csv=prediction_file)

#this class is to bundle together a training set and a test set
class TrainingAndTest:
    name = None
    algorithm = None
    training = None
    test = None
    latent_factors = 1
    iterations = 1
    
    def build_ml_item_predictions_df(self, predictions_file, rebuild = False):
        predictions_df = None
        if rebuild:
            try:
                os.remove(predictions_file)
            except FileNotFoundError:
                print('no file to remove, continuing')
        try:
            predictions_df = pd.read_csv(predictions_file, index_col = 0)
            print('Prediction results from test set loaded from file (test.predictions_df)')
        except FileNotFoundError:
            print('Running predictor on given training set')
            from item_similarity import ml_item_predictor as mip
            predictions_df = mip.predict(self, predictions_file)
            print('Predictions saved at ' + predictions_file)
        self.test.predictions_df = predictions_df
        print('Prediction results ready (test.predictions_df)')
        print(predictions_df)
        return predictions_df
    
    def build_ml_user_predictions_df(self, predictions_file, rebuild = False):
        predictions_df = None
        if rebuild:
            try:
                os.remove(predictions_file)
            except FileNotFoundError:
                print('no file to remove, continuing')
        try:
            predictions_df = pd.read_csv(predictions_file, index_col = 0)
            print('Prediction results from test set loaded from file (test.predictions_df)')
        except FileNotFoundError:
            print('Running predictor on given training set')
            from user_similarity import ml_user_predictor as mup
            predictions_df = mup.predict(self, predictions_file)
            print('Predictions saved at ' + predictions_file)
        self.test.predictions_df = predictions_df
        print('Prediction results ready (test.predictions_df)')
        return predictions_df
    
    def build_ml_wnmf_predictions_df(self, predictions_file, cap = True, sklearn = False):
        print('Running WNMF predictor on given training set')
        from wnmf import ml_wnmf_predictor as mwp
        if sklearn:
            predictions_df = mwp.predict_sklearn(self, predictions_file, cap_at_5=cap, latent_factors=self.latent_factors, iterations=self.iterations)
        else:
            predictions_df = mwp.predict(self, predictions_file, cap_at_5=cap)
        print('Predictions saved at ' + predictions_file)
        self.test.predictions_df = predictions_df
        print('Prediction results ready (test.predictions_df)')
        return predictions_df
    
    def build_yelp_item_predictions_df(self, predictions_file, rebuild = False):
        predictions_df = None
        if rebuild:
            try:
                os.remove(predictions_file)
            except FileNotFoundError:
                print('no file to remove, continuing')
        try:
            predictions_df = pd.read_csv(predictions_file, index_col = 0)
            print('Prediction results from Yelp test set loaded from file (test.predictions_df)')
        except FileNotFoundError:
            print('Running Yelp predictor on given training set')
            from item_similarity import yelp_item_predictor as yip
            #note that the below um_df and sm_df are really dictionaries
            predictions_df = yip.predict(self.training.um_df, self.training.sm_df, self.test.og_df, predictions_file)
            print('Predictions saved at ' + predictions_file)
        self.test.predictions_df = predictions_df
        print('Prediction results ready (test.predictions_df)')
        return predictions_df

    def build_yelp_user_predictions_df(self, predictions_file, rebuild = False):
        predictions_df = None
        if rebuild:
            try:
                os.remove(predictions_file)
            except FileNotFoundError:
                print('no file to remove, continuing')
        try:
            predictions_df = pd.read_csv(predictions_file, index_col=0)
            print('Prediction results from Yelp test set loaded from file (test.predictions_df)')
        except FileNotFoundError:
            print('Running Yelp predictor on given training set')
            from user_similarity import yelp_user_predictor as yup
            #note that the below um_df and sm_df are really dictionaries
            predictions_df = yup.predict(self.training.um_df, self.training.sm_df, self.test.og_df, predictions_file)
            print('Predictions saved at ' + predictions_file)
        self.test.predictions_df = predictions_df
        print('Prediction results ready (test.predictions_df)')
        return predictions_df
    
    def build_yelp_wnmf_predictions_df(self, predictions_file):
        predictions_df = None
        print('Running ML predictor on Yelp training set')
        '''
        from wnmf import yelp_wnmf_predictor as ywp
        #note that the below um_df and sm_df are really dictionaries
        predictions_df = ywp.predict(self.training.u_df, self.training.v_df, self.test.og_df, predictions_file, 'datasets/yelp_dataset/utility-matrix/yelp_uc_user_id.json', 'datasets/yelp_dataset/utility-matrix/yelp_uc_item_id.json')
        '''
        from wnmf import ml_wnmf_predictor as mwp
        predictions_df = mwp.predict(self, predictions_file)
        print('Predictions saved at ' + predictions_file)
        self.test.predictions_df = predictions_df
        print('Prediction results ready (test.predictions_df)')
        return predictions_df
    
    #CONSTRUCTOR
    def __init__(self, name, latent_factors=1, iterations=1):
        self.name = name
        self.latent_factors = latent_factors
        self.iterations = iterations
        print("FYI: If all you are seeing is this message, you may need to initialize the .training and .test instance variable objects using their own constructors. Otherwise, disregard this.")
    
def main():
    print("Nothing here right now")
    #use this area for testing if needed

if __name__ == '__main__':
    main()
        
        



