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
import correlation
import sys
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
    def __init__(self, name, og_file, um_file, sm_file, data, algo, sim, latent_factors = 3, iterations = 25):
        self.name = name
        print(name + ' is being prepared...')
        if data == 'ml':
            self.og_df = self.build_ml_og_df(og_file) #function returns df
            if algo == 'item':
                self.um_df = self.build_ml_item_um(um_file) #function returns um df
            elif algo == 'user':
                self.um_df = self.build_ml_user_um(um_file) #function returns um df
                print(self.um_df)
            elif algo == 'wnmf':
                self.um_df = self.build_ml_item_um(um_file)
            if sim == 'pearson':
                    self.sm_df = self.build_ml_pearson_sm(sm_file) #function returns sim df
            elif sim == 'cosine':
                    self.sm_df = self.build_ml_cosine_sm(sm_file)
            elif sim == 'wnmf':
                    self.u_df, self.v_df = self.build_ml_wnmf_prediction_matrix(sm_file, latent_factors, iterations)
        elif data == 'yelp':
            self.og_df = self.build_yelp_og_df(og_file)
            if algo == 'item':
                self.um_df = self.build_yelp_item_um(um_file) #function returns um df
            elif algo == 'user':
                self.um_df = self.build_yelp_user_um(um_file) #function returns um df
            elif algo == 'wnmf':
                self.um_df = self.build_yelp_wnmf_um(um_file)
            if sim == 'pearson':
                self.sm_df = self.build_yelp_pearson_sm(sm_file) #function returns sim df
            elif sim == 'cosine':
                self.sm_df = self.build_yelp_cosine_sm(sm_file)
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
            print("og_df")
            print(og_df)
            return og_df
        except FileNotFoundError:
            print("build_ml_og_df error: Original data file not at location given")
        
    
    #builds item-based utility matrix for data file at specified filename #GOOD 6/25
    #results in an item-based utility matrix with columns denoted '1', '2', '3' (strings) and rows 1, 2, 3 (integers)
    def build_ml_item_um(self, um_file):
        um_df = None
        try:
            um_df = pd.read_csv(um_file, index_col = 0)
        except FileNotFoundError:
            print('Building MovieLens item-based utility matrix for the \'' + self.name + '\' dataset')
            from item_similarity import ml_item_um_builder
            um_df = ml_item_um_builder.build(self.og_df, um_file)
        print('MovieLens item-based utility matrix ready (um_df)')
        #print(um_df)
        return um_df
    
    def build_ml_user_um(self, um_file):
        um_df = None
        try:
            um_df = pd.read_csv(um_file, index_col = 0)
        except FileNotFoundError:
            print('Building MovieLens user-based utility matrix for the \'' + self.name + '\' dataset')
            from item_similarity import ml_item_um_builder
            um_df = ml_item_um_builder.build(self.og_df, um_file)
        print('MovieLens user-based utility matrix ready')
        um_df = um_df.T
        return um_df
            
    def build_ml_pearson_sm(self, sm_file):
        sm_df = None
        try:
            sm_df = pd.read_csv(sm_file, index_col = 0)
        except FileNotFoundError:
            print('Building MovieLens Pearson correlation similarity matrix for the \'' + self.name + '\' dataset')
            import ml_pearson_sm_builder
            sm_df = ml_pearson_sm_builder.build(self.um_df, sm_file)
        print('MovieLens Pearson correlation-based similarity matrix ready (sm_df)')
        return sm_df
    
    def build_ml_cosine_sm(self, sm_file):
        sm_df = None
        try:
            sm_df = pd.read_csv(sm_file, index_col = 0)
        except FileNotFoundError:
            print('Building MovieLens cosine similarity matrix for the \'' + self.name + '\' dataset')
            import ml_cosine_sm_builder
            sm_df = ml_cosine_sm_builder.build(self.um_df, sm_file)
        print('MovieLens cosine similarity matrix ready (sm_df)')
        #print(sm_df)
        return sm_df
    
    def build_ml_wnmf_prediction_matrix(self, prediction_matrix_file, latent_factors, iterations):
        u_df = None
        v_df = None
        print('Building MovieLens WMNF prediction matrix for the \'' + self.name + '\' dataset')
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
            print(og_df)
            return og_df #this is a Pandas DataFrame
        except FileNotFoundError:
            print("build_ml_og_df error: Yelp training set file not at location given")
            
    def build_yelp_item_um(self, um_file):
        um_df = None
        try:
            with open(um_file, 'r') as f:
                um_df = json.load(f)
        except FileNotFoundError:
            print('Building Yelp user-based utility matrix for the \'' + self.name + '\' dataset')
            import yelp_utility_matrix_builder_item as yumi
            um_df = yumi.build(self.og_df, um_file)
        print('Yelp item-based utility matrix ready')
        return um_df #this is a dictionary
            
    def build_yelp_user_um(self, um_file):
        um_df = None
        try:
            with open(um_file, 'r') as f:
                um_df = json.load(f)
        except FileNotFoundError:
            print('Building Yelp user-based utility matrix for the \'' + self.name + '\' dataset')
            import yelp_utility_matrix_builder_user as yumu
            um_df = yumu.build(self.og_df, um_file)
        print('Yelp user-based utility matrix ready')
        return um_df #this is a dictionary
    
    def build_yelp_wnmf_um(self, um_file):
        print("trying to load WNMF UM from location: " + um_file)
        um_df = None
        try:
            um_df = pd.read_csv(um_file, index_col = 0)
            print(um_df)
            print('Yelp WNMF utility matrix ready')
            return um_df #this is a dictionary
        except FileNotFoundError:
            print('''This Yelp WNMF UM function is not equipped to build a UM, just to load it. 
            Please build your UMs manually and point the test driver to them instead.
            Until then, you will be unable to proceed with Yelp WNMF.''')
        

    def build_yelp_pearson_sm(self, sm_file):
        sm_df = None
        try:
            with open(sm_file, 'r') as f:
                sm_df = json.load(f)
        except FileNotFoundError:
            import yelp_sm_builder as ysb
            print('Building Yelp Pearson similarity matrix for the \'' + self.name + '\' dataset') 
            sm_df = ysb.similarity_pearson(self.um_df, sm_file)
        return sm_df
    
    def build_yelp_cosine_sm(self, sm_file):
        sm_df = None
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
    
    def build_ml_item_predictions_df(self, predictions_file):
        predictions_df = None
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
    
    def build_ml_user_predictions_df(self, predictions_file):
        predictions_df = None
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
        print(predictions_df)
        return predictions_df
    
    def build_ml_wnmf_predictions_df(self, predictions_file):
        print('Running WNMF predictor on given training set')
        from wnmf import ml_wnmf_predictor as mwp
        predictions_df = mwp.predict(self, predictions_file)
        print('Predictions saved at ' + predictions_file)
        self.test.predictions_df = predictions_df
        print('Prediction results ready (test.predictions_df)')
        print(predictions_df)
        return predictions_df
    
    def build_yelp_item_predictions_df(self, predictions_file):
        predictions_df = None
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
        print(predictions_df)
        return predictions_df

    def build_yelp_user_predictions_df(self, predictions_file):
        predictions_df = None
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
        print(predictions_df)
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
        print(predictions_df)
        return predictions_df
    
    #CONSTRUCTOR
    def __init__(self, name):
        self.name = name
        print("FYI: If all you are seeing is this message, you may need to initialize the .training and .test instance variable objects using their own constructors. Otherwise, disregard this.")

#DATASET LOADING FUNCTIONS
def load_ml_100k():
    ml_100k = Dataset("MovieLens 100k main file")
    ml_100k.algorithm = 'neighborhood-based collaborative filtering'
    ml_100k.source = 'datasets/ml-100k/u.data'
    ml_100k.build_ml_og_df() #build dataframe from the source
    ml_100k.item_utility_source = 'datasets/ml-100k/utility-matrix/ml_100k_item_utility.csv'
    #ml_100k.build_item_utility('datasets/ml-100k/utility-matrix/ml_100k_item_utility.csv') #build item-based utility matrix dataframe
    ml_100k.build_item_utility_df()
    ml_100k.item_pearson_sim_source = 'item_similarity/ml_100k_item_pearson_sim.csv'
    #ml_100k.build_item_pearson_sim('item_similarity/ml_100k_item_pearson_sim.csv')
    ml_100k.build_item_pearson_sim_df() #build item-based utility matrix dataframe
    #returns Dataset object to calling function
    return ml_100k


    #MovieLens 100k u1 test/training set
def load_ml_u1():
    return load_ml_u1_item_pearson()
    
def load_ml_u1_for_wnmf():
    ml_u1 = TrainingAndTest('MovieLens u1 training/test sets')
    ml_u1.training = Dataset(
        'u1 training set',                                          #name
        'datasets/ml-100k/u1.base',                                 #original source
        'datasets/ml-100k/utility-matrix/ml_u1_item_utility.csv',   #utility matrix
        'item_similarity/ml_u1_item_pearson_sim.csv',               #similarity matrix
        'ml',                                                   #data source
        'item',                                                 #algorithm
        'pearson')                                              #correlation
    ml_u1.test = TestSet(
        'u1 test set',                                              #name
        'datasets/ml-100k/u1.test')
    return ml_u1

    #MovieLens 100k u1 test/training set
def load_ml_u1_item_pearson():
    #NEED ONLY FUNCTIONS TO BE BUILD FUNCTIONS THAT TAKE A CSV
    ml_u1 = TrainingAndTest('MovieLens u1 training/test sets')
    ml_u1.training = Dataset(
        'u1 training set',                                      #name
        'datasets/ml-100k/u1.base',                             #original source
        'datasets/ml-100k/utility-matrix/ml_u1_item_um.csv',    #utility matrix
        'item_similarity/ml_u1_item_corr_sm.csv',               #similarity matrix
        'ml',                                                   #data source
        'item',                                                 #algorithm
        'pearson')                                              #correlation
    print("ml_u1.training UM")
    print(ml_u1.training.um_df)
    print("ml_u1.training SM")
    print(ml_u1.training.sm_df)
    ml_u1.test = TestSet(
        'u1 test set',                                          #name
        'datasets/ml-100k/u1.test')
    ml_u1.build_ml_item_predictions_df('item_similarity/filename')
    print("ml_u1.test.og_df")
    print(ml_u1.test.og_df)
    print("ml_u1.test.predictions_df")
    print(ml_u1.test.predictions_df)
    ml_u1.test.calculate_mae()
    ml_u1.test.calculate_rmse()
    print("MAE: " + str(ml_u1.test.mae))
    print("RMSE: " + str(ml_u1.test.rmse))
    return ml_u1

def load_ml_u1_user_pearson():
    #NEED ONLY FUNCTIONS TO BE BUILD FUNCTIONS THAT TAKE A CSV
    ml_u1 = TrainingAndTest('MovieLens u1 training/test sets')
    ml_u1.training = Dataset(
        'u1 training set',                                      #name
        'datasets/ml-100k/u1.base',                             #original source
        'datasets/ml-100k/utility-matrix/ml_u1_user_um.csv',    #utility matrix
        'user_similarity/ml_u1_user_pearson_sm.csv',            #similarity matrix
        'ml',                                                   #data source
        'user',                                                 #algorithm
        'pearson')                                              #correlation
    print("ml_u1.training UM")
    print(ml_u1.training.um_df)
    print("ml_u1.training SM")
    print(ml_u1.training.sm_df)
    ml_u1.test = TestSet(
        'u1 test set',                                          #name
        'datasets/ml-100k/u1.test')

    ml_u1.build_ml_user_predictions_df('user_similarity/ml_u1_user_pearson_predictions.csv')
    #print("ml_u1.test.og_df")
    print(ml_u1.test.og_df)
    
    print("ml_u1.test.predictions_df")
    print(ml_u1.test.predictions_df)
    
    ml_u1.test.calculate_mae()
    ml_u1.test.calculate_rmse()
    print("MAE: " + str(ml_u1.test.mae))
    print("RMSE: " + str(ml_u1.test.rmse))
    return ml_u1

def load_yelp_stut():
    yelp_stut = Dataset("Yelp Stuttgart, Germany Reviews")
    yelp_stut.item_utility_source = 'datasets/yelp_dataset/utility-matrix/yelp_utility_matrix_stuttgart.csv'
    yelp_stut.build_item_utility_df()
    yelp_stut.item_pearson_sim_source = 'item_similarity/yelp_stut_item_pearson_sim.csv'
    yelp_stut.build_user_pearson_sim('user_similarity/yelp_stut_user_pearson_sim.csv')
    print(yelp_stut.user_pearson_sim_df)
    
def main():
    ml_u1 = load_ml_u1_item_pearson()
    #print("Correlation between observed values and predictions")
    #print(ml_u1.test.predictions_df['observed'].corr(ml_u1.test.predictions_df['prediction']))
    

if __name__ == '__main__':
    main()
    
        
        
        



