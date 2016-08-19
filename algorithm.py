import numpy


def countTagOccurances(cursorObject):
    curs = cursorObject

    # Get our data into a list (for 5 users)
    prefsList = cursorToList(curs)
    prefsArray = listToMatrix(prefsList)

    tagsList = tagsToBinary(curs)
    tagsArray = listToMatrix(tagsList)

    print(prefsArray)
    print(tagsArray)

    print 'multiply arrays'
    print(numpy.dot(tagsArray * prefsArray))


    print 'hello'
    print prefsArray
    return prefsArray


def cursorToList(cursorObject):
    data_array = []

    # Keep track of current observation
    i = 0
    for observation in cursorObject:
        print(observation)
        print(observation['u1'])
        data_array.append([observation['Id'], observation['u1'], observation['u2'], observation['u3'], observation['u4'], observation['u5']])
        i += 1

    return data_array


def listToMatrix(list):
    arr = numpy.array(list)
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
        tags = observation['Tags'].split(", ")

        # print(observation)

        # For each item in data_tags pool of tags
        for i in range(len(data_tags)):
            # For each item in our returned set of tags
            for j in range(len(tags)):
                # When one of our tags matches
                if str(tags[j]) == data_tags[i]:
                    print('==equal==')
                    # Set the last list at position that matches data_tags array, inside the data_array
                    data_array[-1][i] = 1
                    # print(tags)
                    # print(tags[j])
            


    print(data_array)
    print(type(data_array))
    return data_array

