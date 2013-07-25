from __future__ import division
import csv
import os
import random
import sys

def beginProgram():
    beginProgram = raw_input("Welcome to JG's flashcards! Press 'Enter' to begin.")
    print

def requestBoxNum():
    while True:
        boxNum = raw_input("Choose a box to practice (1-5): ")
        print
        try:
            boxNum = int(boxNum)
            if (0 < boxNum < 6):
                return str(boxNum)
            else:
                print "The number must be between '1' and '5'."
                print        
        except ValueError:
            print "Oops, that wasn't a number!"
            print

def openBoxFile(boxNum):
    try:            
        with open(inputPath, "rb") as myFile:
            myFileReader = csv.reader(myFile)
            for key, value in myFileReader: #loads two rows of words from file            
                currentDict[key] = value #add that entry to the dictionary
    except IOError:
        print ("There is a problem opening the file.  Double check that the"
        "\nbox files are in the correct folder and that they are named"
        "\ncorrectly (e.g., 'box1.csv', 'box2.csv', etc.).")      
        closeProgram()
    except ValueError:
        print ("There aren't any cards in that box.  Add some words to the box"
        "\nand try again.")
        closeProgram()          

def practiceBox(boxNum):    
    correct = 0
    incorrect = 0
    print
    print "Ok, let's practice box number {}!".format(boxNum)
    print
    print ("Type 'QUIT' at any time to exit the program."
    "\nYour progress will be saved.")
    print    
    while len(currentDict) > 0: #repeats the loop if words are still in the dict
        testWord = random.choice(currentDict.keys()) #grabs a random key 
        testAnswer = currentDict[testWord] #sets answer to corresponding value        
        print "Word to translate:", testWord
        myWord = raw_input("Enter the correct translation: ")        
        if myWord == testAnswer:
            print "Good job!"
            print
            correctDict[testWord] = testAnswer #appends correct answer to temp dict        
            del(currentDict[testWord]) #deletes word from main dict        
            correct += 1
        elif myWord == "QUIT":            
            saveAnswersOnQuit()            
            closeProgram()
        else:
            print ("You were a little off..."
            "\nThe correct answer was '{}'.").format(testAnswer)
            print
            incorrectDict[testWord] = testAnswer
            del(currentDict[testWord])            
            incorrect += 1         
        checkDictLength(currentDict)              
    else:
        calcFinalScore(correct, incorrect)

def saveCorrectAnswer():    
    outputPath = os.path.join(myPath, "box{}.csv".format(str(int(boxNum)+1)))
    with open(outputPath, "ab") as myFile:
        myFileWriter = csv.writer(myFile)
        for key, value in correctDict.items():
            myFileWriter.writerow([key, value])

def saveIncorrectToBox1():
    if boxNum == "1":        
        with open(outputPath, "wb") as myOutputFile:
            myFileWriter = csv.writer(myOutputFile)
            for key, value in incorrectDict.items():            
                myFileWriter.writerow([key, value])
    else:
        box1TempDict = {}        
        with open(box1InputPath, "rb") as myInputFile:
            myFileReader = csv.reader(myInputFile)
            for key, value in myFileReader:           
                box1TempDict[key] = value                
        for key, value in incorrectDict.iteritems():
            if key not in box1TempDict:
                box1TempDict[key] = value                        
        with open(box1OutputPath, "wb") as myOutputFile:
            myFileWriter = csv.writer(myOutputFile)
            for key, value in box1TempDict.items():            
                myFileWriter.writerow([key, value])        

def writeRemainingWordsToCurrentBox():    
    with open(outputPath, "wb") as myFile:
        myFileWriter = csv.writer(myFile)
        for key, value in currentDict.items():
            myFileWriter.writerow([key, value])

def saveAnswersOnQuit():
    saveIncorrectToBox1()
    saveCorrectAnswer()
    writeRemainingWordsToCurrentBox()        

def clearCurrentBox():
    if boxNum != "1":        
        with open(outputPath, "w+") as myFile:
            myFile.truncate()
    else:
        clearBox1()

def clearBox1():
    if len(incorrectDict) == 0:        
        with open(box1OutputPath, "w+") as myFile:
            myFile.truncate()
    else:
        None           

def checkDictLength(currentDict):
    if len(currentDict) == 0: #checks if all words have been answered correctly
        print ("You have practiced all the words in this box."  
        "\nThe correct words are in the next box, and the incorrect words are in box 1.")                       
        saveCorrectAnswer()
        saveIncorrectToBox1()
        clearCurrentBox()            
        print    

def calcFinalScore(correct, incorrect):
    try:
        score = 0        
        score = int((correct / (incorrect + correct)) * 100)    
        print ("You had {} words correct and {} words incorrect."
        "\nYour score was {}%.").format(correct, incorrect, score)
        print
    except ZeroDivisionError:
        print ("Looks like you tried to load an empty box.  Add some words"
        "\nto the box and try to load it again.") 

def closeProgram():
    print
    closeProgram = raw_input("Press 'Enter' to close the program.")
    sys.exit()


beginProgram()

currentDict = {}
incorrectDict = {}
correctDict = {}

boxNum = requestBoxNum()

myPath = "C:/Users/Justin/Desktop/flashcards"
inputPath = os.path.join(myPath, "box{}.csv".format(boxNum))
box1InputPath = os.path.join(myPath, "box1.csv")
outputPath = os.path.join(myPath, "box{}.csv".format(boxNum))
box1OutputPath = os.path.join(myPath, "box1.csv")

openBoxFile(boxNum)
practiceBox(boxNum)

closeProgram()