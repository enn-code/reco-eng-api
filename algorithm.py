import numpy


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
    print(weightedPrefs(prefsArray, tagsArray))

    print 'hello'
    print prefsArray
    return prefsArray


def cursorToList(cursorObject):
    data_array = []

    for observation in cursorObject:
        print(observation)
        print(observation['u1'])
        print(type(str(observation['Tags'])))
        # data_array.append(observation)
        data_array.append([str(observation['Tags']), str(observation['Id']), int(observation['u1']), int(observation['u2']), int(observation['u3']), int(observation['u4']), int(observation['u5'])])

    return data_array


def listToMatrix(list):
    arr = numpy.array(list)
    return arr

def listToIntMatrix(list):
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
        print 'observation'
        print observation

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
                    print('==equal==')
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

            print('user art rating')
            print(art_id, u_id)
            print(prefs_array[art_id, u_id])
            print(tags_array[art_id])
            # Perform multiplication tags vector * user prefs
            multiplyVector = numpy.dot(tags_array[art_id], prefs_array[art_id, u_id])
            userTagsArrayList[u_id].append(multiplyVector)

    # Need to cut the list down
    print('userTagsArrayList')
    print(userTagsArrayList)
    print('userTagsArrayList[1][1:]')
    print(userTagsArrayList[1][1:])
    
    totalTagsArray = []

    # Add the tags for each user and return array of totals
    for i in range(5):
        userAllTags = listToMatrix(userTagsArrayList[i][1:])
        sumUserTags = numpy.sum(userAllTags, axis=0)
        totalTagsArray.append(sumUserTags)

    print('totals')    
    print(totalTagsArray)

    return totalTagsArray
