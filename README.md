# Recommender Systems (SCSE Summer Research 2019)

This repository is for the recommender system project that includes the implementations for multiple collaborative filtering algorithms, including neighborhood based models and matrix factorization based models.

# Structure of Folders

Each folder contains several Python source files and a document that includes all functions implemented in each file with their specifications. A couple of sample sections are shown below:

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
