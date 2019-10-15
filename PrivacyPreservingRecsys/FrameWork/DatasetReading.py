import os
import csv
import sys

from surprise import Dataset
from surprise import Reader
from collections import defaultdict

class data_reading:

    #ID_to_name = {}
    #name_to_ID = {}
    #ratingsPath = '../datasets_storage/ID_scaled_google_rating.csv'
    
    ratingsPath = '../datasets_storage/ratings.csv'
    itemsPath = '../datasets_storage/movies.csv'
    #files_dir = '../datasets_storage/ml-20m/100folds/'
    itemsPath = '../datasets_storage/movies.csv'
    #NOFI = 91 #number of files
    
    def creatFilePath(self, root = files_dir , quantity = NOFI):
        trainFiles   = root + 'u%d.base'
        testFiles    = root + 'u%d.test'
        TOI = tuple(range(1, quantity + 1)) #tuple of indices
        folds_files = [(trainFiles % i, testFiles % i) for i in TOI]
        return folds_files        
        
    def loadGeneralData(self):

        # Look for files relative to the directory we are running from
        # it change the relative directory to the current directory.
        os.chdir(os.path.dirname(sys.argv[0]))

        ratingsDataset = 0
        self.itemID_to_name = {}
        self.name_to_itemID = {}

        reader = Reader(line_format='user item rating timestamp', sep=',', skip_lines=1)
        #This dataset object is a surprise object.
        ratingsDataset = Dataset.load_from_file(self.ratingsPath, reader=reader)
        # Open the file using the path from itemsPath, newline is '', encoding is Latin, the file is represented as csvfile.
        with open(self.itemsPath, newline='', encoding='ISO-8859-1') as csvfile:
            itemReader = csv.reader(csvfile)
            next(itemReader)  #Skip header line 
            for row in itemReader:
                itemID = int(row[0]) # first item is the ID 
                itemName = row[1]    # second item is the name
                self.itemID_to_name[itemID] = itemName #this is a classical dictionary item ID is the key and corresponds to a name
                self.name_to_itemID[itemName] = itemID #this is also a dictoinary, ID and name is reversed.

        return ratingsDataset 
        

    def loadAllIDs(self):
        itemIDs = []
        userIDs  = []
        with open(self.ratingsPath, newline='') as csvfile: # this is where the rating file path is...
            ratingReader = csv.reader(csvfile) # this how you save the csv reader
            next(ratingReader) # this is how you skip the first line...
            for row in ratingReader: # this is one row in the rating file.
                userIDs.append(int(row[0]))
                IDs.append(int(row[1]))
        userIDs.sort()
        itemIDs.sort()
        seen = set()
        seen_add = seen.add
        userIDs = [x for x in userIDs if not (x in seen or seen_add(x))]
        itemIDs = [x for x in itemIDs if not (x in seen or seen_add(x))]
        return userIDs, itemIDs

    def load20mMovieLen(self):
        os.chdir(os.path.dirname(sys.argv[0]))
        ratingsDataset = 0
        reader = Reader(line_format='user item rating timestamp', sep=',', skip_lines=0)
        filesToBeRead = self.creatFilePath()
        ratingsDataset = Dataset.load_from_folds(filesToBeRead, reader=reader)
        return ratingsDataset
        
    def getPopularityRanks(self):
        ratings = defaultdict(int) 
        rankings = defaultdict(int)
        with open(self.ratingsPath, newline='') as csvfile: # open the rating file.
            ratingReader = csv.reader(csvfile)
            next(ratingReader)
            for row in ratingReader:
                itemID = int(row[1])
                ratings[itemID] += 1 #every time a item shows up, you increment 1 in the ratings dictionary.
        rank = 1
        # This one is a bit complicated. so in the ratings. it is a dictionary. The key is itemID and the
        # the value is how many times it has been rated. Now, here the ratings are sorted using the lambda
        # function. It is using the value instead of the key to sort. Note that each line is like a tuple
        # (itemID, integer). Since it is sorted reversely, the order is from the most rated to the least 
        # rated.
        for itemID, ratingCount in sorted(ratings.items(), key=lambda x: x[1], reverse=True):
            #Then from top to bottom, you can tell what the ranking is for each item.
            rankings[itemID] = rank
            rank += 1
        #So, the rankings is also called the popularity.
        return rankings
        
    def getItemName(self, itemID): # simply get what is the item ID
        if itemID in selfitemID_to_name: # translating from ID to name.
            return self.itemID_to_name[itemID]
        else:
            return ""
        
    def getItemID(self, itemName): # rtranslate from name to ID.
        if itemName in self.name_to_itemID:
            return self.name_to_itemID[itemName]
        else:
            return 0
