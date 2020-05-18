import json
import csv
import os
import sys
import math
from random import randint
from pprint import pprint

args = sys.argv

#argument to folder containing train and test sets for works published before a median date
beforePath = args[1]

#argument to folder containing train and test sets for works published on or after a median date
afterPath = args[2]

#will contain all distinct unigrams in the entire dataset
vocab = set()

#we will need to explore all the files in the train and test sets for works published before a median date
paths = os.walk(beforePath)

#will contain every token that is present in the train set for works published before a median date
tokensInBeforeTrain = []

print("Processing Training Data for works published before median date ...")

for r in paths:

    if(r[0].find('/') != -1):

        #we will need to look at all files in a train or test set
        for f in r[2]:

            pathToFile = r[0] + '/' + f

            #open a file
            file = open(pathToFile, 'r')

            #create a list containing all lines from a file
            lines = file.readlines()

            for x in range(0, len(lines)):
                
                if(lines[x].rfind('\n') == len(lines[x]) - 1):

                   #delete '\n' at the end of lines[x] if it is present
                   lines[x] = lines[x][0: lines[x].rfind('\n')]

                   #as far as punctuation marks are concerned, we need to space them out appropriately
                   lines[x] = lines[x].replace("(", " ( ")
                   lines[x] = lines[x].replace(")", " ) ")
                   lines[x] = lines[x].replace(",", " , ")
                   lines[x] = lines[x].replace("?", " ? ")
                   lines[x] = lines[x].replace(";", " ; ")
                   lines[x] = lines[x].replace("!", " ! ")
                   lines[x] = lines[x].replace("[", " [ ")
                   lines[x] = lines[x].replace("]", " ] ")
                   
                   #convert lines[x] into series of tokens contained in lines[x]
                   lines[x] = lines[x].split()

                   #counts number of times a period has to be spaced out appropriately
                   countForPeriods = 0

                   #counts number of times a colon has to be spaced out appropriately
                   countForColons = 0
                   
                   #find out number of times colons and periods have to be spaced out appropriately
                   for y in range(0, len(lines[x])):
                       if(len(lines[x][y]) > 1):
                          if(lines[x][y][len(lines[x][y]) - 1] == '.'):
                            lines[x][y] = lines[x][y][0: len(lines[x][y]) - 1]
                            countForPeriods = countForPeriods + 1
                          elif(lines[x][y][len(lines[x][y]) - 1] == ':'):
                            lines[x][y] = lines[x][y][0: len(lines[x][y]) - 1]
                            countForColons = countForColons + 1
                          #
                       #
                   #

                   #append a period at the end of lines[x] for countForPeriod times
                   for z in range(0, countForPeriods):
                       lines[x].append('.')
                   #

                   #append a colon at the end of lines[x] for countForColons times
                   for z in range(0, countForColons):
                       lines[x].append(':')
                   #

                #
            #
            
            for x in range(0, len(lines)):
                #add tokens contained in lines[x] to vocab set
                for y in range(0, len(lines[x])):
                    vocab.add(lines[x][y])
                #
            #

            if(pathToFile.find("/train") != -1):
                #if file is part of a train set, then add all tokens to tokensInBeforeTrain list
                for x in range(0, len(lines)):
                    for y in range(0, len(lines[x])):
                        tokensInBeforeTrain.append(lines[x][y])
                    #
                #
            #

        #
    #
#

print("Processing Training Data for works published on or after median date ...")

#we will need to explore all the files in the train and test sets for works published on or after a median date
paths = os.walk(afterPath)

#will contain every token that is present in the test set for works published before a median date
tokensInAfterTrain = []

for r in paths:
    if(r[0].find('/') != -1):
        for f in r[2]:
            pathToFile = r[0] + '/' + f
            file = open(pathToFile, 'r')
            lines = file.readlines()
            for x in range(0, len(lines)):
                if(lines[x].rfind('\n') == len(lines[x]) - 1):
                   lines[x] = lines[x][0: lines[x].rfind('\n')]
                   lines[x] = lines[x].replace("(", " ( ")
                   lines[x] = lines[x].replace(")", " ) ")
                   lines[x] = lines[x].replace(",", " , ")
                   lines[x] = lines[x].replace("?", " ? ")
                   lines[x] = lines[x].replace(";", " ; ")
                   lines[x] = lines[x].replace("!", " ! ")
                   lines[x] = lines[x].replace("[", " [ ")
                   lines[x] = lines[x].replace("]", " ] ")

                   lines[x] = lines[x].split()

                   countForPeriods = 0
                   countForColons = 0

                   for y in range(0, len(lines[x])):
                       if(len(lines[x][y]) > 1):
                          if(lines[x][y][len(lines[x][y]) - 1] == '.'):
                            lines[x][y] = lines[x][y][0: len(lines[x][y]) - 1]
                            countForPeriods = countForPeriods + 1
                          elif(lines[x][y][len(lines[x][y]) - 1] == ':'):
                            lines[x][y] = lines[x][y][0: len(lines[x][y]) - 1]
                            countForColons = countForColons + 1
                          #
                       #
                   #

                   for z in range(0, countForPeriods):
                       lines[x].append('.')
                   #

                   for z in range(0, countForColons):
                       lines[x].append(':')
                   #

                #
            #
            
            for x in range(0, len(lines)):
                for y in range(0, len(lines[x])):
                    vocab.add(lines[x][y])
                #
            #

            if(pathToFile.find("/train") != -1):
                for x in range(0, len(lines)):
                    for y in range(0, len(lines[x])):
                        tokensInAfterTrain.append(lines[x][y])
                    #
                #
            #

        #
    #
#

print("Add 1 Smoothing being done right now...")

#convert vocab set into a list
vocab = list(vocab)

#sort all tokens in vocab
vocab.sort()

#used to keep track of # of occurrences of each token in all train sets for works published before median date
countsInBeforeTrain = []

#used to keep track of # of occurrences of each token in all train sets for works published on or after median date
countsInAfterTrain = []

#has all add-1 smoothing estimates needed for tokens contained in train sets for works published before median date
probsInBefore = []

#has all add-1 smoothing estimates needed for tokens contained in train sets for works published on or after median date
probsInAfter = []

for x in range(0, len(vocab)):
    countsInAfterTrain.append(0)
    countsInBeforeTrain.append(0)
    probsInBefore.append(0)
    probsInAfter.append(0)
#

#contains the maximum number of times to search for something within vocab using binary search
times = math.ceil(math.log(len(vocab), 2))
times = int(times)

for x in tokensInBeforeTrain:
    index = -1
    first = 0
    last = len(vocab) - 1
    if(x == vocab[len(vocab) - 1]):
       index = len(vocab) - 1
    else:
       for c in range(0, times):
           middle = int((first + last)/2)
           if(vocab[middle] == x):
              index = middle
              break
           elif(vocab[middle] > x):
              last = middle
           elif(vocab[middle] < x):
              first = middle
           #
       #
    #

    if(index != -1):
       countsInBeforeTrain[index] = countsInBeforeTrain[index] + 1
    #
#

for x in tokensInAfterTrain:
    index = -1
    first = 0
    last = len(vocab) - 1
    if(x == vocab[len(vocab) - 1]):
       index = len(vocab) - 1
    else:
       for c in range(0, times):
           middle = int((first + last)/2)
           if(vocab[middle] == x):
              index = middle
              break
           elif(vocab[middle] > x):
              last = middle
           elif(vocab[middle] < x):
              first = middle
           #
       #
    #

    if(index != -1):
       countsInAfterTrain[index] = countsInAfterTrain[index] + 1
    #
#

#sum of all counts in countsInBeforeTrain
sumForBefore = sum(countsInBeforeTrain)

#sum of all counts in countsInAfterTrain
sumForAfter = sum(countsInAfterTrain)

#compute add-1 smoothing for train sets containing works published before median date
for x in range(0, len(probsInBefore)):
    probsInBefore[x] = (countsInBeforeTrain[x] + 1) / (1.0 * (sumForBefore + len(vocab)))
#

#compute add-1 smoothing for train sets containing works published on or after median date
for x in range(0, len(probsInAfter)):
    probsInAfter[x] = (countsInAfterTrain[x] + 1) / (1.0 * (sumForAfter + len(vocab)))
#

print("Performing tests right now...")

paths = os.walk(beforePath)

#used to keep track of all the times model gives correct classification
correct = 0

#used to keep track of all the times model gives wrong classification
wrong = 0

for r in paths:
    if(r[0].find("/test") != -1):
        for f in r[2]:
            pathToFile = r[0] + '/' + f
            file = open(pathToFile, 'r')
            lines = file.readlines()
            for x in range(0, len(lines)):
                if(lines[x].rfind('\n') == len(lines[x]) - 1):
                    lines[x] = lines[x][0: lines[x].rfind('\n')]
                    lines[x] = lines[x].replace("(", " ( ")
                    lines[x] = lines[x].replace(")", " ) ")
                    lines[x] = lines[x].replace(",", " , ")
                    lines[x] = lines[x].replace("?", " ? ")
                    lines[x] = lines[x].replace(";", " ; ")
                    lines[x] = lines[x].replace("!", " ! ")
                    lines[x] = lines[x].replace("[", " [ ")
                    lines[x] = lines[x].replace("]", " ] ")
                   
                    lines[x] = lines[x].split()
                    countForPeriods = 0
                    countForColons = 0
                   
                    for y in range(0, len(lines[x])):
                       if(len(lines[x][y]) > 1):
                          if(lines[x][y][len(lines[x][y]) - 1] == '.'):
                            lines[x][y] = lines[x][y][0: len(lines[x][y]) - 1]
                            countForPeriods = countForPeriods + 1
                          elif(lines[x][y][len(lines[x][y]) - 1] == ':'):
                            lines[x][y] = lines[x][y][0: len(lines[x][y]) - 1]
                            countForColons = countForColons + 1
                          #
                       #
                    # 

                    for z in range(0, countForPeriods):
                       lines[x].append('.')
                    #

                    for z in range(0, countForColons):
                       lines[x].append(':')
                    #
                #
            #

            classType = pathToFile[0: pathToFile.find('/')]

            #instead of multiplying probabilities, adopt alternative method as underflow is bound to happen whether log space is used or not
            #Example of alternative method being used is shown below

            '''
            Example:
            Let's say we have two numbers, productOfProbs1 and productOfProbs2
            We want to see which one of the two numbers is the highest

            productOfProbs1 = 0.6 * 0.8 * 0.7 
            productOfProbs2 = 0.3 * 0.2 * 0.4  

            The best way to see which one of the two numbers is the highest is to compute log10(0.6/0.3) + log10(0.8/0.2) + log10(0.7/0.4)

            if log10(0.6/0.3) + log10(0.8/0.2) + log10(0.7/0.4) is less than 0 --> productOfProbs1 is less than productOfProbs2
            -> (productOfProbs1 / productOfProbs2) = 10^(some negative #)

            if log10(0.6/0.3) + log10(0.8/0.2) + log10(0.7/0.4) is greater than 0 --> productOfProbs1 is greater than productOfProbs2
            -> (productOfProbs1 / productOfProbs2) = 10^(some positive #)

            if log10(0.6/0.3) + log10(0.8/0.2) + log10(0.7/0.4) is equal to 0 --> productOfProbs1 is equal to productOfProbs2
            -> (productOfProbs1 / productOfProbs2) = 10^(0)

            '''

            powers = 0

            for x in range(0, len(lines)):
                for y in range(0, len(lines[x])):
                    target = lines[x][y]
                    index = -1
                    first = 0
                    last = len(vocab) - 1
                    if(target == vocab[len(vocab) - 1]):
                        index = len(vocab) - 1
                    else:
                        for c in range(0, times):
                            middle = int((first + last)/2)
                            if(vocab[middle] == target):
                                index = middle
                                break
                            elif(vocab[middle] > target):
                                last = middle
                            elif(vocab[middle] < target):
                                first = middle
                            #
                        #
                    #
                    
                    num = probsInAfter[index] / (1.0 * probsInBefore[index])
                    powers = powers + math.log(num, 10)

                #
            #

            classInstance = ''

            if(powers >= 0):
               classInstance = 'after'
            elif(powers < 0):
               classInstance = 'before'
            #

            if(classInstance == classType):
                correct = correct + 1
            else:
                wrong = wrong + 1
            #

        #
    #
#

#used to keep track of all times when model gave correct classification for test set files for works published before medianDate
beforeTestCorrect = correct

#used to keep track of all times when model gave wrong classification for test set files for works published before medianDate
beforeTestWrong = wrong

#used to keep track of all times when model gave correct classification for test set files for works published on or after medianDate
afterTestCorrect = 0

#used to keep track of all times when model gave wrong classification for test set files for works published on or after medianDate
afterTestWrong = 0


paths = os.walk(afterPath)

for r in paths:
    if(r[0].find("/test") != -1):
        for f in r[2]:
            pathToFile = r[0] + '/' + f
            file = open(pathToFile, 'r')
            lines = file.readlines()
            for x in range(0, len(lines)):
                if(lines[x].rfind('\n') == len(lines[x]) - 1):
                    lines[x] = lines[x][0: lines[x].rfind('\n')]
                    lines[x] = lines[x].replace("(", " ( ")
                    lines[x] = lines[x].replace(")", " ) ")
                    lines[x] = lines[x].replace(",", " , ")
                    lines[x] = lines[x].replace("?", " ? ")
                    lines[x] = lines[x].replace(";", " ; ")
                    lines[x] = lines[x].replace("!", " ! ")
                    lines[x] = lines[x].replace("[", " [ ")
                    lines[x] = lines[x].replace("]", " ] ")
                   
                    lines[x] = lines[x].split()
                    countForPeriods = 0
                    countForColons = 0
                   
                    for y in range(0, len(lines[x])):
                       if(len(lines[x][y]) > 1):
                          if(lines[x][y][len(lines[x][y]) - 1] == '.'):
                            lines[x][y] = lines[x][y][0: len(lines[x][y]) - 1]
                            countForPeriods = countForPeriods + 1
                          elif(lines[x][y][len(lines[x][y]) - 1] == ':'):
                            lines[x][y] = lines[x][y][0: len(lines[x][y]) - 1]
                            countForColons = countForColons + 1
                          #
                       #
                    # 

                    for z in range(0, countForPeriods):
                       lines[x].append('.')
                    #

                    for z in range(0, countForColons):
                       lines[x].append(':')
                    #
                #
            #

            classType = pathToFile[0: pathToFile.find('/')]
            powers = 0

            for x in range(0, len(lines)):
                for y in range(0, len(lines[x])):
                    target = lines[x][y]
                    index = -1
                    first = 0
                    last = len(vocab) - 1
                    if(target == vocab[len(vocab) - 1]):
                        index = len(vocab) - 1
                    else:
                        for c in range(0, times):
                            middle = int((first + last)/2)
                            if(vocab[middle] == target):
                                index = middle
                                break
                            elif(vocab[middle] > target):
                                last = middle
                            elif(vocab[middle] < target):
                                first = middle
                            #
                        #
                    #
                    
                    num = probsInAfter[index] / (1.0 * probsInBefore[index])
                    powers = powers + math.log(num, 10)

                #
            #

            classInstance = ''

            if(powers >= 0):
               classInstance = 'after'
            elif(powers < 0):
               classInstance = 'before'
            #

            if(classInstance == classType):
                correct = correct + 1
                afterTestCorrect = afterTestCorrect + 1
            else:
                wrong = wrong + 1
                afterTestWrong = afterTestWrong + 1
            #

        #
    #
#

print('\n')

#provides information about test set performance for works published on or after a median date
print("Test Set for works published ON OR AFTER medianDate")
percentCorrect = (afterTestCorrect) / (1.0 * (afterTestCorrect + afterTestWrong))
percentCorrect = percentCorrect * 100
print("% Correct Classification: " + str(percentCorrect))
percentWrong = (afterTestWrong) / (1.0 * (afterTestCorrect + afterTestWrong))
percentWrong = percentWrong * 100
print("% Wrong Classification: " + str(percentWrong))
print("\n")

#provides information about test set performance for works published before a median date
print("Test Set for works published BEFORE medianDate")
percentCorrect = (beforeTestCorrect) / (1.0 * (beforeTestCorrect + beforeTestWrong))
percentCorrect = percentCorrect * 100
print("% Correct Classification: " + str(percentCorrect))
percentWrong = (beforeTestWrong) / (1.0 * (beforeTestCorrect + beforeTestWrong))
percentWrong = percentWrong * 100
print("% Wrong Classification: " + str(percentWrong))
print("\n")

#provides information about performance of all tests
print("All Test Sets")
percentCorrect = (correct) / (1.0 * (correct + wrong))
percentCorrect = percentCorrect * 100
print("% Correct Classification: " + str(percentCorrect))
percentWrong = (wrong) / (1.0 * (correct + wrong))
percentWrong = percentWrong * 100
print("% Wrong Classification: " + str(percentWrong))
print("\n")
