


def filterTheDict(dictObj, callback):
    newDict = dict()
    # Iterate over all the items in dictionary
    for (key, value) in dictObj.items():
        # Check if item satisfies the given condition then add to new dict
        if callback((key, value)):
            newDict[key] = value
    return newDict

def words_frequency_one(words):
    great_string = []
    for word in words:
        great_string.append(word['wordForm'])
    str2 = [] 
    for i in great_string:              
        # checking for the duplicacy 
        if i not in str2: 
            # insert value in str2 
            str2.append(i)
            
    result = 0
    for i in range(0, len(str2)): 
        if great_string.count(str2[i]) == 1:
            result += 1
    return result

        
