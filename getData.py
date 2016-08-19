"""Script to get mongodb data"""
import sys
import json
from pymongo import MongoClient

from flask import Flask, request
app = Flask(__name__)

from sklearn.cluster import KMeans
from sklearn import datasets
from sklearn import svm



print('test outside function')

def main():
    """Main entry point for the script."""
    print('testing...')
    app.run(debug=True) # debug lets us auto reload on code changes
    pass


# Root page 
@app.route("/")
def rootPage():
    return 'This is the root page'



# Get all user data
@app.route("/api/data/")
def getData():
    cursorObject = databaseData()
    prefs_array = preferencesToArray(cursorObject)
    print(prefs_array)
    print(type(prefs_array))
    
    prefs_cut_array = [item[1:] for item in prefs_array]
    print(prefs_cut_array)
    firstKmeans(prefs_cut_array)

    # Get tag data and put into a binary array for each observation
    #tags_array = str(tagsToBinary(cursorObject))
    
    displayArray(prefs_array)
    
    return str(prefs_array)


@app.route("/api/version1/")
def version1():
    cursorObject = databaseData()

    # Count times each user views an article with a given tag
    countTagOccurances()

def countTageOccurances():
    print 'hello'

def databaseData():
    client = MongoClient()
    db = client.recodb
    coll = db.training_data
    cursorObject = coll.find()
    return cursorObject

def displayArray(input_array):
    for i in range(len(input_array)):
        print(input_array[i])

    print(input_array[0][0])
    pass



# Get a single user
@app.route("/api/data/<userId>")
def getUserData(userId):
    pass


# Use KMeans clustering on my dataset
@app.route("/api/clustered/")
def performClustering():
    result = firstKmeans()
    return str(result)


# First attempt at KMeans with our main dataset
# Needs: Our data in an [n_observations, n_features] matrix
def firstKmeans(data):

    kmeans = KMeans(n_clusters=4)
    kmeans.fit(data)

    print('kmeans!')
    print(data)
    print(kmeans.cluster_centers_)
    print(kmeans.labels_)
    return kmeans


# Convert observed user behaviour (preferences) to array
def preferencesToArray(cursorObject):

    prefs_array = []

    # Keep track of current observation
    i = 0
    for observation in cursorObject:
        print(observation)
        print(observation['u1'])
        prefs_array.append([observation['Id'], observation['u1'], observation['u2'], observation['u3'], observation['u4'], observation['u5']])
        i += 1

    print(prefs_array)
    return prefs_array


# Get tag data from cursor object and register as binary array
def tagsToBinary(cursorObject):
    data_array = []
    data_full = []
    data_tags = ['animals', 'cats', 'cute', 'funny', 'fruit', 'food', 'vegetables', 'feminism', 'sport', 'women', 'men', 'sexy', 'hot', 'football', 'athletics', 'hockey', 'training', 'routines', 'healthy', 'workout', 'tv', 'celebrity', 'movies', 'comedy', 'drama', 'youtube']

    # For each observation
    for observation in cursorObject:
        # Save the observations to a complete array for test purposes
        data_full.append(observation)
        # Initialise a row of zeroes
        data_array.append([0] * len(data_tags))
        # Get tags for current observation
        tags = observation['Tags'].split(", ")

        print(observation)

        # For each item in data_tags pool of tags
        for i in range(len(data_tags)):
            # For each item in our returned set of tags
            for j in range(len(tags)):
                # When one of our tags matches
                if str(tags[j]) == data_tags[i]:
                    print('==equal==')
                    # Set the last list at position that matches data_tags array, inside the data_array
                    data_array[-1][i] = 1
                    print(tags)
                    print(tags[j])
            


    print(data_array)
    return data_array


# Test the SVM clustering library on example data
# This is an example of supervised learning, using the sklearn
# test dataset
@app.route("/api/test/svmclustering/")
def testClustering():
    iris = datasets.load_iris()
    print(iris)
    print(iris.data)   

    print(iris.target)

    # Use Support Vector Machine library method to apply
    # clustering algorithm
    clf = svm.LinearSVC()
    # Choose data to fit to model
    clf.fit(iris.data, iris.target)

    # Give a piece of sample data to predict which cluster group it fits into
    result = clf.predict([[6.0, 3.6, 5.2, 1.9]])
    # Fits into group 2!

    return result


# This will be an example of the k-means clustering algorithm,
# which is an unsupervised learning algorithm
@app.route("/api/test/kmeans")
def testKmeans():
    
    iris = datasets.load_iris()

    # We are clustering n observations into k clusters
    # Initialise the object
    kmeans_iris = KMeans(n_clusters=3, init='k-means++', n_init=5, max_iter=300)

    kmeans_iris.fit(iris.data)

    # Get attributes of the clustering operation
    print('Display kmeans_iris cluster centers')
    print(kmeans_iris.cluster_centers_)
    print('Display kmeans_iris labels')
    print(kmeans_iris.labels_)
    pass




# Pull in new data and store it in a database collection
def pullNewData():
    pass

# Delete old database collection
def deleteOldData():
    pass


if __name__ == '__main__':
    sys.exit(main())
 
