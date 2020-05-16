import json
import csv
import os
import sys
from random import randint
from pprint import pprint

args = sys.argv

jsonPath = args[1]
beforePath = args[2]
afterPath = args[3]
csvPath = args[4]

#Generate 1/10 of len(numbers) from numbers
#PARAMATERS
    #setLength = length of set we would like to generate numbers for
def generate_Numbers(setLength):
    nums = {}
    while len(nums) < (setLength/10):
        val = randint(0, setLength)
        if val not in nums:
            nums[val] = 0
    return nums

#Take the paths given as input, and make our directories
#Format is:
#python T2.py /path/to/json_folder /path/to/beforeSet /path/to/afterSet
#We then populate beforeSet and Afterset with their training and test data
def make_paths():
    #Make our two base directories
    try:
        os.mkdir(beforePath)
    except OSError:
        print(f"Creation of the directory {beforePath} failed")
    else:
        print(f"Succesfully created the directory {beforePath}")
    try:
        os.mkdir(afterPath)
    except OSError:
        print(f"Creation of the directory {afterPath} failed")
    else:
        print(f"Succesfully created the directory {afterPath}")
    
    
    #make our four subdirectories
    beforePathTrain = beforePath+"/train"
    beforePathTest = beforePath+"/test"
    afterPathTrain = afterPath+"/train"
    afterPathTest = afterPath+"/test"
    try:
        os.mkdir(beforePathTrain)
    except OSError:
        print(f"Creation of the directory {beforePathTrain} failed")
    else:
        print(f"Succesfully created the directory {beforePathTrain}")
        
    try:
        os.mkdir(beforePathTest)
    except OSError:
        print(f"Creation of the directory {beforePathTest} failed")
    else:
        print(f"Succesfully created the directory {beforePathTest}")
    
    try:
        os.mkdir(afterPathTrain)
    except OSError:
        print(f"Creation of the directory {afterPathTrain} failed")
    else:
        print(f"Succesfully created the directory {afterPathTrain}")
    
    try:
        os.mkdir(afterPathTest)
    except OSError:
        print(f"Creation of the directory {afterPathTest} failed")
    else:
        print(f"Succesfully created the directory {afterPathTest}")

    return beforePathTrain, beforePathTest, afterPathTrain, afterPathTest


#Create two lists: one, the list of file ids made before the median (sorted by date), and two, the list of file ids made after the median date (sorted by date)
def build_DateSets():
    idDict ={}
    dateDict = {}
    finalList = []
    jsonDirectory = os.fsencode(jsonPath)
    
    #Make a list of all author ids, taken from the json files
    for file in os.listdir(jsonDirectory):
        filename = jsonPath + "/"+os.fsdecode(file)
        with open(filename) as json_file:
            data = json.load(json_file)
            idDict[data.get("paper_id")] = 1
            #print("Appended"+data.get("paper_id"))
    
    
    #we now have the list of id's - we now need to build a list of the dates. Make a dictionary of key value pairs where key is id, and value is date.
    with open(csvPath) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if row[1] in idDict:
                dateDict[row[1]] = row[9]
    
    #We now sort the list by date. Python's sort handles this easily, thankfully (we do convert to list first)
    DateList = [(k, v) for k, v in dateDict.items()]
    DateList.sort(key=lambda x:x[1])
    
    #This is our sorted list of ids
    idList = [x[0] for x in DateList]
    
    #We define the median literally as the halfway point (i.e. #of dates/2). This means that for odd number sets (like sets of length 7) the after set will have 1 more data point.
    median = int((len(idList)/2))
    beforeList = idList[:median]
    afterList = idList[median:]
    
    return beforeList, afterList


#This function is just a clean way to write the data we want from the source file to the correct destination file
#PARAMATERS
    #sourceFile = file we want to read from
    #writeFile = file we want to write to
def write_Data(sourceFile, destFile):
    
    #First open and read all data into our list
    with open(sourceFile) as source_file:
        wholeData = json.load(source_file)
        textList = []
        
        #Go through the entire file, find each instance of text in abstract and body_text and add to our final list
        for item in wholeData:
            if item == "abstract":
                index = 0
                for dict in wholeData["abstract"]:
                    for subitem in dict:
                        if subitem == "text":
                            textList.append(wholeData["abstract"][index]["text"])
                    index+=1
            
            if item == "body_text":
                index = 0
                for dict in wholeData["body_text"]:
                    for subitem in dict:
                        if subitem == "text":
                            textList.append(wholeData["body_text"][index]["text"])
                    index+=1
    #We give permission to write to this file
    with open(destFile, "w+") as dest_file:
        for text in textList:
            dest_file.write(text+"\n")




#Make files in the four given paths, with the two given lists of file ids
#PARAMATERS
    #beforePathTrain = path for our directory of training files from our beforeList
    #beforePathTest = path of our directory of test files from our beforeList
    #afterPathTrain = path for our directory of training files from our afterList
    #afterPathTest = path for our directory of test files from our afterList
    #beforeList = list of file ids before median, sorted by date
    #afterList = list of file ids after median, sorted by date
def create_Files(beforePathTrain, beforePathTest, afterPathTrain, afterPathTest, beforeList, afterList, beforeNumbers, afterNumbers):
    #Go through the list. Open the json file of each id, then write the text the appropriate folder to the appropriate file.
    #We keep x as a way to track the index
    x = 0
    for id in beforeList:
        idSource = jsonPath+"/"+id+".json"
        if x not in beforeNumbers:
            trainDest = beforePathTrain+"/"+id+".txt"
            write_Data(idSource, trainDest)
        else:
            testDest = beforePathTest+"/"+id+".txt"
            write_Data(idSource, testDest)
        x+=1
        
    x = 0
    for id in afterList:
        idSource = jsonPath+"/"+id+".json"
        if x not in afterNumbers:
            trainDest = afterPathTrain+"/"+id+".txt"
            write_Data(idSource, trainDest)
        else:
            testDest = afterPathTest+"/"+id+".txt"
            write_Data(idSource, testDest)
        x+=1

#    id = beforeList[0]
#    idSource = jsonPath+"/"+id+".json"
#    trainDest = beforePathTrain+"/"+id+".txt"
#    write_Data(idSource, trainDest)

# This function creates a bag of words from the files in a certain directory
def bag_of_words(articlePath):
    all_words = []
    bag = dict()
    
    articleDirectory = os.fsencode(articlePath)

    #print(os.listdir(articleDirectory))
    for article in os.listdir(articleDirectory):
        filename = articlePath + "/"+os.fsdecode(article)
        print(filename)

        with open(filename) as article_file:
            for line in article_file:
                for word in line.split():
                    all_words.append(word)

    for token in all_words:
        if token in bag:
            bag[word] + = 1
        else:
            bag[word] = 1

    return bag

def naive_bayes_add1(bag_of_words, data):
    

def runner():
    #create our file paths and our lists
    beforePathTrain, beforePathTest, afterPathTrain, afterPathTest = make_paths()
    beforeList, afterList = build_DateSets()
    
    #generate the indices of our test sets
    beforeNumbers = generate_Numbers(len(beforeList))
    afterNumbers = generate_Numbers(len(afterList))
    
    #Now, create the files
    create_Files(beforePathTrain, beforePathTest, afterPathTrain, afterPathTest, beforeList, afterList, beforeNumbers, afterNumbers)

    bow_before = bag_of_words(beforePathTrain)
    bow_after = bag_of_words(afterPathTrain)
    
runner()

