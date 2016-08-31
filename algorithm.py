import numpy
from sklearn.cluster import KMeans

import collections # Handle unordered dictionaries
import re # For extracting digits from string


def countTagOccurances(cursorObject):
    curs = cursorObject

    # Get our data into a list (for 5 users)
    dataList = cursorToList(curs)
    dataArray = listToMatrix(dataList)
    
    print(dataArray)
    print(dataArray[:, 2:])

    # Put preferences into array
    prefsArray = listToIntMatrix(dataArray[:, 2:])

    # Get only tags
    tags = dataArray[:,:2]
    # Get tags as a binary array
    tagsList = tagsToBinary(tags)
    tagsArray = listToMatrix(tagsList)

    print(type(prefsArray[0,0]))
    print(type(tagsArray[0,0]))

    # Get tag totals for each user and then weight them
    weightedPrefsDict = weightedPrefs(prefsArray, tagsArray)
    print(weightedPrefsDict)

    weightedPrefsArray = dictionaryToMatrix(weightedPrefsDict)
    print(weightedPrefsArray)
    kmeans = clusterData(weightedPrefsArray)
    kmeansClusters = kmeans.labels_
    print(kmeansClusters)

    articleClustersList = groupArticles(kmeans, tagsArray)
    print(articleClustersList)

    # Recommend the top article in the cluster
    topClusterRecommendation = recommendTopArticle(prefsArray, kmeansClusters, articleClustersList)

    message = ''
    for key, value in topClusterRecommendation.iteritems():
        print(value)
        recArticle = dataArray[value, 1]
        print(dataArray[value, 1])
        mess = 'For a user in cluster {0}, we recommend '.format(key) + recArticle
        message = message + ' --- ' + mess

    print 'Final result'
    return message


def get_key(key):
    ''' Used to help sort unordered dictionaries '''
    try:
        key = re.sub("\D", "", key) # Strip out non-digits
        return int(key)
    except ValueError:
        return str(key)


def cursorToList(cursorObject):   # add to library
    data_list = []

    # print('cursorObject')
    # print(cursorObject)
    # print('SORTED cursorObject')
    # print(sorted(cursorObject))

    for observation in cursorObject:
        print('observation')
        print(observation)
        # print(collections.OrderedDict(observation))
        # print(sorted(observation))
        obsOrdered = collections.OrderedDict(sorted(observation.items(), key=lambda t: get_key(t[0])))
        print(obsOrdered)
        # data_array.append(observation)
        data_list.append([str(obsOrdered['Tags']), str(obsOrdered['Id']), int(obsOrdered['u1']), int(obsOrdered['u2']), int(obsOrdered['u3']), int(obsOrdered['u4']), int(obsOrdered['u5'])])
# http://stackoverflow.com/questions/17376700/sort-alphanumeric-strings-in-numpy-matrix

# def get_key(key):
#     try:
#         return int(key)
#     except ValueError:
#         return key
# a = {'100':12,'6':5,'88':3,'test':34, '67':7,'1':64 }
# b = collections.OrderedDict(sorted(a.items(), key=lambda t: get_key(t[0])))

    return data_list


def listToMatrix(list):     # add to library
    arr = numpy.array(list)
    return arr

def dictionaryToMatrix(dict):     # add to library
    # arr = numpy.array(dict.items())
    arr = numpy.array([val for (key,val) in dict.iteritems()])
    return arr

def listToIntMatrix(list):    # add to library
    arr = numpy.array(list, dtype=numpy.int16)
    return arr


# Get tag data from cursor object and register as binary array
def tagsToBinary(cursorObject):
    print('tags to binary start')
    print cursorObject
    data_array = []
    data_tags = ['animals', 'cats', 'cute', 'funny', 'fruit', 'food', 'vegetables', 'feminism', 'sport', 'women', 'men', 'sexy', 'hot', 'football', 'athletics', 'hockey', 'training', 'routines', 'healthy', 'workout', 'tv', 'celebrity', 'movies', 'comedy', 'drama', 'youtube']

    # For each observation
    for observation in cursorObject:
        # print 'observation'
        # print observation

        # Initialise a row of zeroes
        data_array.append([0] * len(data_tags))
        # Get tags for current observation
        tags = observation[0].split(", ")

        # print(observation)

        # For each item in data_tags pool of tags
        for i in range(len(data_tags)):
            # For each item in our returned set of tags
            for j in range(len(tags)):
                # When one of our tags match
                if str(tags[j]) == data_tags[i]:
                    # print('==equal==')
                    # Set the last list at position that matches data_tags array, inside the data_array
                    data_array[-1][i] = 1
                    # print(tags)
                    # print(tags[j])
            
    # print(data_array)
    # print(type(data_array))
    return data_array

# Takes two arrays with compatible type
def weightedPrefs(prefs_array, tags_array):
    print 'multiply arrays'

    n_users = prefs_array.shape[1]
    n_articles = prefs_array.shape[0]
    userTagsArrayList = []

    print(userTagsArrayList)

    # For each user
    for u_id in range(n_users):
        # Initialise list for appending later
        userTagsArrayList.append([0])
        for art_id in range(n_articles):        

            # print('user art rating')
            # print(art_id, u_id)
            # print(prefs_array[art_id, u_id])
            # print(tags_array[art_id])
            # Perform multiplication tags vector * user prefs
            multiplyVector = numpy.dot(tags_array[art_id], prefs_array[art_id, u_id])
            userTagsArrayList[u_id].append(multiplyVector)

    # Need to cut the list down
    # print('userTagsArrayList')
    # print(userTagsArrayList)
    # print('userTagsArrayList[1][1:]')
    # print(userTagsArrayList[1][1:])
    
    totalTagsArray = []
    totalTagsConsumed = []

    # Add the tags for each user and return array of totals
    for i in range(5):
        userAllTags = listToMatrix(userTagsArrayList[i][1:])
        sumUserTags = numpy.sum(userAllTags, axis=0)
        totalTagsArray.append(sumUserTags)
        print('sumUserTags')
        print(sumUserTags)
        # Turn content consumption into weighted consumption
        # TODO: Turn into a function
        totalTagsConsumed.append(numpy.sum(sumUserTags, axis=0))

        print(totalTagsConsumed)

    print('totals')    
    print(totalTagsArray)


    # Turn content consumption into weighted consumption
    # TODO: Turn into function
    weightedArray = {}
    for i in range(5):
        weightedArray["user{0}".format(i)] = []
        for j in range(len(totalTagsArray[0])):
            tagWeighting = totalTagsArray[i][j] / float(totalTagsConsumed[i])
            # print(tagWeighting)
            weightedArray["user{0}".format(i)].append(tagWeighting)

    print(weightedArray)
    return weightedArray


def clusterData(data):
    # Initialise kmeans
    kmeans = KMeans(n_clusters=3)
    kmeans.fit(data)

    cluster_centroids = kmeans.cluster_centers_
    cluster_labels = kmeans.labels_
    print(cluster_centroids)
    print(cluster_labels)

    
    return kmeans


# Use Kmeans to predict which consumer group each article fits into
def groupArticles(kmeans, binaryArticles):
    print(binaryArticles)

    numberArticles = binaryArticles.shape[0]
    articleClusters = numpy.array([])

    for i in range(numberArticles):
        # Find closest fitting cluster for an article with a given set of tags
        articleGroup = kmeans.predict(binaryArticles[i,:].reshape(1,-1))
        articleClusters = numpy.append(articleClusters, articleGroup)

        
    # TODO: Get number of articles in each group, get number of users too

    print(articleClusters)    
    return articleClusters


# For each user group, find most popular article that falls in that group
def recommendTopArticle(prefsArray, kmeansClusters, articleClusters):
    
    preferenceList = {}
    # userIndices = numpy.zeros((max(kmeansClusters)+1))
    # userPrefsByGroup = numpy.zeros(shape=())
    
    userIndices = {}
    userPrefsByGroup = []

    print(userPrefsByGroup)


    # For each user, put into cluster group whilst keeping the index
    for i in range(len(kmeansClusters)):
        cluster = kmeansClusters[i]
        print(cluster)

        groupName = "group{0}".format(cluster)
        print(groupName)

        if userIndices.get(groupName) == None:
            userIndices[groupName] = []

        userIndices[groupName].append(i)
        # userPrefsByGroup[cluster] = numpy.array(numpy.append(userPrefsByGroup[cluster], float(i)))

    print(userIndices)

    # Slice each user's full prefs into arrays, listed by group
    userPrefsByGroup = {}
    for key, value in userIndices.iteritems():
        for index in range(len(value)):
            if userPrefsByGroup.get(key) == None:
                userPrefsByGroup[key] = []

            # print(index,key,value,userPrefsByGroup[key])
            userPrefsByGroup[key].append(prefsArray[:, value[index]])

    print(userPrefsByGroup)

    sumUserPrefsByGroup = {}
    topRatedIndex = {}
    for key, value in userPrefsByGroup.iteritems():
        if sumUserPrefsByGroup.get(key) == None:
            sumUserPrefsByGroup[key] = []

        # Gives us the sum of all user prefs for each group
        sumUserPrefsByGroup[key] = numpy.sum(userPrefsByGroup[key], axis=0)

        print(sumUserPrefsByGroup[key])

        # Set each article not in group to 0
        for i in range(len(articleClusters)):
            print(sumUserPrefsByGroup[key][i])
            print(key)
            print("group{}".format(int(articleClusters[i])))
            if key != "group{}".format(int(articleClusters[i])):
                print('not equal')
                print(sumUserPrefsByGroup[key])
                print(i)
                sumUserPrefsByGroup[key][i] = 0

        print(sumUserPrefsByGroup[key])
        # Find where the maximum lies
        print 'argmax'
        print(sumUserPrefsByGroup[key].argmax(axis=0))
        topRatedIndex[key] = sumUserPrefsByGroup[key].argmax(axis=0)

    print(topRatedIndex)
    print(sumUserPrefsByGroup)
    print(userIndices)

    return topRatedIndex



# For each user group, find most popular article that falls in that group
def NOTESrecommendTopArticle(prefsArray, kmeansClusters, articleClusters):
    # Takes in an array of preferences for each user in the group
    # Takes a list of all articles in the group
    # Filters so only matching items are left
    # Finds article with highest total rating across this group

    preferenceList = {}
    
    # For each user in cluster (kmeansClusters == groupNumber). Return user ids
    #   For each article per user in cluster


    for j in range(len(kmeansClusters)):
        if preferenceList.get("group{0}".format(kmeansClusters[j])) == None:
            preferenceList["group{0}".format(kmeansClusters[j])] = []

        for i in range(len(articleClusters)):
            # If user group is equal to article group
            # if kmeansClusters[j] == articleClusters[i]:

            userPrefs = prefsArray[i,j]
            if kmeansClusters[j] == articleClusters[i]:
                preferenceList["group{0}".format(kmeansClusters[j])].append(userPrefs)
                print(userPrefs)

    print(preferenceList)
    print(len(preferenceList))
    print(max(preferenceList))
    print(preferenceList.index(max(preferenceList)))

    pass


