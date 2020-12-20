import csv
from nltk.corpus import stopwords

DELIMITERS = stopwords.words('arabic')
nbrOfrows = 0
nbrOfNormal = 0
nbrOfHate = 0

def removeStopWords(stopwords, list):
    result = []
    for word in list:
        if word not in stopwords: result.append(word)
    return result


def loadAllwords(filePath):
    with open(filePath, encoding='UTF-8') as csv_file :
        file = csv.reader(csv_file, delimiter=',')
        normalWords = []
        hateWords = []
        nbrOfrows = 0
        nbrOfNormal = 0
        nbrOfHate = 0

        for row in file:
            nbrOfrows +=1
            if row[1] == 'normal' :
                nbrOfNormal += 1
                normalWords += removeStopWords(DELIMITERS, row[0].split(' '))
            else:
                nbrOfHate +=1
                hateWords += removeStopWords(DELIMITERS, row[0].split(' '))
        return normalWords, hateWords, nbrOfNormal/nbrOfrows , nbrOfHate/nbrOfrows

def classifier(normalWords, hateWords):
    hateWords.sort()
    normalWords.sort()
    distinctHateWords = dict()
    distinctNormalWords = dict()
    for i in range(len(hateWords) ):
        if hateWords[i] in distinctHateWords:
            distinctHateWords[hateWords[i]] += 1
        else:
            distinctHateWords[hateWords[i]] = 1

    for i in range(len(normalWords) ):
        if normalWords[i] in distinctNormalWords:
            distinctNormalWords[normalWords[i]] += 1
        else:
            distinctNormalWords[normalWords[i]] = 1
    return distinctNormalWords, distinctHateWords



if __name__ == '__main__':
    normal, hate , normalPriorProba , hatePriorProba = loadAllwords('train.csv')
    normalDict, hateDict= classifier(normal, hate)

    with open('classified/wordsInNormalTweet.csv','w',  encoding='UTF-8' ) as file:
        for word in normalDict :
            file.write(word + ',' + str(normalDict[word]/ len(normal)) + '\n')

    with open('classified/wordsInHateTweet.csv', 'w', encoding='UTF-8') as file:
        for word in hateDict:
            file.write(word + ' , ' + str(hateDict[word] / len(hate)) + ' \n')

    with open('classified/PriorProbability.csv','w',  encoding='UTF-8' ) as file:
        file.write('normal' + ',' + str(normalPriorProba) + '\n')
        file.write('hate' + ',' + str(hatePriorProba) + '\n')
        file.write('normal-non-exist' + ',' + str(1 / (len(normal) + len(normalDict))) + '\n')
        file.write('hate-non-exist' + ',' + str(1 / (len(hate) + len(hateDict))) + '\n')


