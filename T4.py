import json
import csv
import os
import sys
from random import randint
from pprint import pprint
import math

args = sys.argv

beforePath = args[1]
afterPath = args[2]

def getTokens(fileName):

    file = open(fileName, 'r')

    #create a list containing all lines from a file
    lines = file.readlines()
    allTokens = []

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

        for z in range(0, len(lines[x])):
            allTokens.append(lines[x][z])
        #

    #

    return allTokens

#

#if files do not exist, run T3 to get files needed for T4
if((os.path.isfile('probsInBeforeTrain.txt') == False) & (os.path.isfile('probsInAfterTrain.txt') == False) & (os.path.isfile('vocab.txt') == False)):
    print('\n')
    print('T3 IS BEING RUN TO GET NECESSARY FILES')
    print('--------------------------------')
    os.system('python T3.py before after')
    print('--------------------------------')
    print('GOT NECESSARY FILES NEEDED FOR T4')
    print('\n')
#

#open necessary files for T4
file1 = open('probsInBeforeTrain.txt', 'r')
file2 = open('probsInAfterTrain.txt', 'r')
file3 = open('vocab.txt', 'r')

#store file contents into variables
vocab = file3.readlines()
probsInBefore = file1.readlines()
probsInAfter = file2.readlines()

#delete all files that we used so far
os.remove('probsInBeforeTrain.txt')
os.remove('probsInAfterTrain.txt')
os.remove('vocab.txt')

for x in range(0, len(probsInAfter)):
    probsInAfter[x] = probsInAfter[x][0: probsInAfter[x].rfind('\n')]
    probsInAfter[x] = float(probsInAfter[x])
#

for x in range(0, len(probsInBefore)):
    probsInBefore[x] = probsInBefore[x][0: probsInBefore[x].rfind('\n')]
    probsInBefore[x] = float(probsInBefore[x])
#

for x in range(0, len(vocab)):
    vocab[x] = vocab[x][0: vocab[x].rfind('\n')]
#

#will store the names of all files in the before test set
beforeTestSet = None

paths = os.walk(beforePath)

for r in paths:
    if(r[0].find("/test") != -1):
       pathToSet = r[0]
       allFiles = []
       for k in range(0, len(r[2])):
           allFiles.append(pathToSet + '/' + r[2][k])
       #
       beforeTestSet = allFiles
    #
#

#will store the names of all files in the after test set
afterTestSet = None

paths = os.walk(afterPath)

for r in paths:
    if(r[0].find("/test") != -1):
       pathToSet = r[0]
       allFiles = []
       for k in range(0, len(r[2])):
           allFiles.append(pathToSet + '/' + r[2][k])
       #
       afterTestSet = allFiles
    #
#

for x in range(0, len(beforeTestSet)):
    setOfTokens = getTokens(beforeTestSet[x])
    for y in setOfTokens:
        #look up index for y in vocab using binary search
        #look up probsInAfter[index]
        #look up probsInBefore[index]
        pass
    #
#

for x in range(0, len(afterTestSet)):
    setOfTokens = getTokens(afterTestSet[x])
    for y in setOfTokens:
        #look up index for y in vocab using binary search
        #look up probsInAfter[index]
        #look up probsInBefore[index]
        pass
    #
#