"""Script to get mongodb data"""
import sys
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
    app.run()
    pass


# Get all user data
@app.route("/api/data/")
def getData():
    client = MongoClient()
    db = client.recodb
    coll = db.training_data
    cursorObject = coll.find()
    data_array = []

    for document in cursorObject:
        data_array.append(document)
        print(document)

    return str(data_array)


# Get a single user
@app.route("/api/data/<userId>")
def getUserData(userId):
    pass


# Use KMeans clustering on my dataset
@app.route("/api/clustered/")
def performClustering():
    testClustering()
    return 'done'


# Test the SVM clustering library on example data
# This is an example of supervised learning, using the sklearn
# test dataset
def testClustering():
    iris = datasets.load_iris()
    print(iris.data)   

    print(iris.target)

    # Use Support Vector Machine library method to apply
    # clustering algorithm
    clf = svm.LinearSVC()
    # Choose data to fit to model
    clf.fit(iris.data, iris.target)

    # Give a piece of sample data to predict which cluster group it fits into
    print(clf.predict([[6.0, 3.6, 5.2, 1.9]]))
    # Fits into group 2!

    pass

# This will be an example of the k-means clustering algorithm,
# which is an unsupervised learning algorithm
def testKmeans():
    pass




# Pull in new data and store it in a database collection
def pullNewData():
    pass

# Delete old database collection
def deleteOldData():
    pass


if __name__ == '__main__':
    sys.exit(main())
 
