# Recommender Systems (SCSE Summer Research 2019)

This repository is for the recommender system project that includes the implementations for multiple collaborative filtering algorithms, including neighborhood based models and matrix factorization based models.

# Structure of Folders

Each folder contains several Python source files and a document that includes all functions implemented in each file with their specifications. A couple of sample sections are shown below:

# recsys
## datasets.py
This file contains classes that enable us to bundle together training sets, test sets, and the results of functions and tests run on them.

### Classes
#### Dataset
Description: This class holds original data files imported into Pandas, as well as utility, similarity, and prediction matrices calculated from it.

##### Parent Classes: 
None

##### Child Classes: 
TestSet

##### Instance Variables:

``name`` name of Dataset (ml_u1 for MovieLens set 1, etc.)
``og_df`` Pandas dataframe holding results of importing original data using <function>
``um_df`` **For MovieLens**, a Pandas dataframe containing a utility matrix (UM). For item-based similarity, the UM rows represent users and the columns represent items. For user-based similarity, rows represent items, and columns users. 
**For Yelp**, this is a Python dictionary of keys representing a utility matrix. We chose this representation for the Yelp dataset UM because it is much more compact than a ~200 MB utility matrix table. For item-based similarity, each key on the first level represents an item, and each key/value pair on the second level represents a user who has rated that item, as follows:
````
um_df = {
item1: {user1: rating1, user2: rating2, ..., user_n: rating_n}, 
item2: {user1: rating1, user2: rating2, ..., user_n: rating_n},
...,
item_n: {user1: rating1, user2: rating2, ..., user_n: rating_n}}
````
``sm_df`` **For MovieLens** a Pandas dataframe containing a similarity matrix (SM), which holds the calculated Pearson correlation or cosine similarity between all pairs of items (in item-item similarity) or users (in user-user similarity) in the training set. If no similarity could be calculated for a given pair, the value for that pair in the SM is ``nan``.
**For Yelp** a Python dictionary of keys representing a similarity matrix. For item-item similarity, it would be as follows:
````
sm_df = {
item1: {item1: similarity_1_1, item2: similarity_1_2, ..., item_n: similarity_1_n}, 
item2: {item1: similarity_2_1, item2: similarity_2_2, ..., user_n: similarity_2_n}, 
...,
item_n: {item1: similarity_n_1, item2: similarity_n_2, ..., item_n: similarity_n_n}}
````
``u_df`` and ``v_df``: Pandas dataframes holding U and V factors, respectively, produced as the result of running the WNMF prediction matrix builders.








#### TrainingAndTest
Description: This class holds 

```
computePCC(userVector1, userVector2)
Description: This function computes the Pearson correlation coefficient between two user vectors.
Input: Two user vectors
Output: The value of the Pearson correlation coefficient between two user vectors

buildSimilarityMatrix()
Description: This function calls the computePCC function to compute similarity degrees between every pair of users and build an m-by-m two dimensional array that represents the user similarity matrix, where m is the total number of users.
Input: None
Output: The user similarity matrix
```
