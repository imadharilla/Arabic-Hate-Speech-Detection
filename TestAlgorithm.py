import csv
from nltk.corpus import stopwords

DELIMITERS = stopwords.words('arabic')
def removeStopWords(stopwords, list):
    result = []
    for word in list:
        if word not in stopwords: result.append(word)
    return result


def getNormalDictionary():
    with open('classified/wordsInNormalTweet.csv', encoding="utf-8") as normalFile:
        file = csv.reader(normalFile, delimiter=',')
        dictionary = dict()
        for row in file:
            try:
                dictionary[row[0]] = row[1]
            except :
                continue

        return  dictionary

def getHateDictionary():
    with open('classified/wordsInHateTweet.csv', encoding="utf-8") as normalFile:
        file = csv.reader(normalFile, delimiter=',')
        dictionary = dict()
        for row in file:
            try:
                dictionary[row[0]] = row[1]
            except:
                continue
        return dictionary

def getPriorProba():
    with open('classified/PriorProbability.csv', encoding="utf-8") as normalFile:
        file = csv.reader(normalFile, delimiter=',')
        dictionary = dict()
        for row in file:
            dictionary[row[0]] = row[1]
        return  dictionary




def getNormalProbaOfWord(word, normalWords, priorProba):
    if word in normalWords:
        pnormal = float(normalWords[word])
    else:
        pnormal = float(priorProba['normal-non-exist'])
    return pnormal

def getHateProbaOfWord(word, hateWords, priorProba):
    if word in hateWords:
        phate = float(hateWords[word])
    else:
        phate = float(priorProba['hate-non-exist'])
    return phate


def isHate(wordlist, normalWords, hateWords, priorProba):
    pnormal = float(priorProba['normal'])
    phate = float(priorProba['hate'])
    for word in wordlist:
        if word == '':
            continue
        pnormal *= getNormalProbaOfWord(word, normalWords, priorProba)
        phate *= getHateProbaOfWord(word, hateWords, priorProba)

    return phate > pnormal

normalWords = getNormalDictionary()
hateWords = getHateDictionary()
priorProba = getPriorProba()
with open('test.csv', encoding="utf-8") as test_file, open('results/failures.csv', 'w', encoding="utf-8") as failureFile , open('results/success.csv', 'w', encoding="utf-8") as successFile:
    file = csv.reader(test_file, delimiter=',')
    nbrTests = 0
    nbrSuccess = 0
    nbrFail = 0
    for row in file:
        nbrTests += 1
        words = removeStopWords(DELIMITERS, row[0].split(' '))
        isnormal = row[1] == 'normal'
        if isnormal != isHate(words, normalWords, hateWords, priorProba):
            nbrSuccess += 1
            successFile.write(row[0] + ',' + row[1] + '\n')
        else:
            failureFile.write(row[0] + ',' + row[1] + '\n')
            nbrFail += 1

    print("Total tests: ", nbrTests)
    print("Total success: ", nbrSuccess)
    print("Total fails: ", nbrFail)

    print("Success rate: ", (nbrSuccess/nbrTests)*100, "%")


