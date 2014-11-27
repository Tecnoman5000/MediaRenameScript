#!/usr/bin/python
from os import rename, path, listdir

# Global varibles
filePlace = []  #Holds locations of files in the fileName varible
fileDir = input("File rename directory? ")
try: # Try the user submitted directory
    fileInput = str(listdir(fileDir)) #find all the files in submited director
except WindowsError: #If user submition fails, user default directories
    fileDir = 'D:\Documents\Programming\Python\Media Rename Project' #find all the files in selected director (Windows)
    #fileDir = '/run/media/nick/ORANGE2/python/Media Rename Project/'  #find all the files in selected director (Linux - USB)
    #fileDir = 'E:\python\Media Rename Project' #find all the files in selected director (Windows - USB)
    print("Invalid directory, reverting to deafualt: " + fileDir)
    fileInput = str(listdir(fileDir)) #find all the files in submited director
fileList = [] #stores file names
numFiles = 0  #Holds the number of files in the directory based on the # of " ' " found in the list
currentFile = 0  #currentfile in the list (starts at 0)
fileName = "tmpFileName"  #holds the original file name
fileExt = ".mp4"  #holds file extension during renaming process

#proper file extensions
proExt = ['.mp4', '.mkv', '.avi', '.AAC']

#Formate check dictionary
checkChars = ['[720p]', '[1080p]','(2013)', '(2014)']

#Repair Dictionary
repChars = {'.': ' ', '1080p': '[1080p]', '720p': '[720p]', '2013': '(2013)', '2014': '(2014)'}

#Remove Dictionary
rmChars = {} #Create rmChars dictionary
with open("rmDict.txt", 'r') as rmDict: #Open rmDict.txt file
    for line in rmDict.read().splitlines(): #For lines in rmDict.txt file pull string data
        rmChars[line] = '' #Add data from each line in rmDict.txt to rmChars dictionary as a key with emmty value

#find each " ' " in fileInput
def initFilePlace():
    #print(fileInput)
    index = 0
    while index < len(fileInput):
        index = fileInput.find("'", index)
        if index == -1:
            break
        #print("' found at ", index)
        filePlace.append(index)
        index += 1
    return int(len(filePlace) / 2)
    
#Creates the fileList, form the fileInput    
def initFileList(text): #Makes file List, Input is the number of files
    fileStart = 0 #Begining of the fileName in FileInput
    fileFinish = fileStart + 1

    print(numFiles)
    for n in range(numFiles):
        #print(fileStart, fileFinish)
        fileList.append(fileInput[filePlace[fileStart] + 1:filePlace[fileFinish]]) #Grabs file name from the fileInput  & puts it in fileList
        fileStart += 2 #Moves the splice position
        fileFinish = fileStart + 1 #Moves to end of fileName in fileInput
    print("Files Found: " + str(fileList))

#pick out a single file name out of "filePlace"
def splicefileInput(placement):
    fileName = fileList[placement]
    return fileName

#finds and removes the extension from the file name and places it in a variable
def findExt():
    index = 0
    global extIndex  #Declare extIndex as a global variable so that it can be reference
    extIndex = 0
    
    while index < len(fileName):
        index = fileName.find(".", index)
        if index == -1:
            break
        #print(". found at ", index)
        extIndex = index
        index += 1
    return extIndex

#Initail check for previous formatting 
def initCheck(text):
    global badText
    global formating
    badText = False
    formating = False

    for key in rmChars: #For the amount of keys in remove dict
        if text.find(key) > 0: #if bad text found, stop loop
            #print("Bad naming found")
            badText = True
            break

    for key in checkChars:
        if text.find(key) > 0: #if formating found, stop loop
            #print("Formating found")
            formating = True
            break
    if badText == False or formating == True: #No Bad text, and formating found
        return True #Is it formated?
    return False #Else, ethier bad text found, or no formating found = not formated
        
#Removes the crap from the fileName, based on the rmDict
def autoRemove(text, rmDict):
    for i, j in rmDict.items():
        text = text.replace(i, j)
    return text

#function for fixing "file" names
def autoFormat(text, repairDict):
    for i, j in repairDict.items():
        text = text.replace(i, j)
    return text

def finalCheck(text):
    spaceLoc = []
    #print (len(text) - 1)
    while text.find(" ", len(text) - 1) != -1:
        spaceLoc.append(text.find(" ", len(text) - 1))
        #print("Space location = " + str(spaceLoc))
        if len(text) - 1 in spaceLoc:
            spaceLoc.remove(len(text) -1)
            #print("'" + text + "'")
            text = text[:len(text) - 1]
            #print("'" + text + "'")
    return text

#Add extension to the fomated fileName
def addExt(text):
    text += fileExt
    return text

#Debug prints
def debugPrints():
    #print("Number of Chars in fileInput: " + str(len(fileInput)))
    #print("Start and finsh to each file name " + str(filePlace))
    #print("Number of positions sotred in filePlace: " + str(len(filePlace)))
    #print("Number of files in current directory: " + str(numFiles))
    print("")
    print("File Choosen: " + fileName)
    print("Found file extension: " + str(fileExt))

#Create / file filePlace variable
numFiles = initFilePlace()  #Declare number of files in folder

if numFiles < 1: #if less than 1 file in directory skip rename process
    print("Not enough files in directory")
else:
    #Create the fileList
    initFileList(numFiles)
    
    while currentFile < numFiles:
        #Call splicefileInput 
        fileName = splicefileInput(currentFile)
        
        #Grab file extension from fileName string
        fileExt = fileName[findExt():]
            
        #Check if the fileName has been previously formated
        
        if fileExt in proExt:  #Checks to see if given file extension is valid compared to list (proExt)
            debugPrints() #Display all debug information
            print("Valid Extension")

            #Is the file formated?
            if initCheck(fileName) == False: #Formate Check
                fileName = fileName[:findExt()]  #remove file extension from fileName string
                print("Original File Name = " + fileName)

                #Formate clean text in fileName
                if formating == False:
                    fileNameFixed = autoFormat(fileName, repChars) #Rename File via "autoFormat" function
                    print("Fixed File Name = '" + fileNameFixed + "'")

                #Clean bad text from fileName
                if badText == True:
                    fileNameFixed = autoRemove(fileNameFixed, rmChars) #Rename File via "autoRemove" function
                    print("Crap removed - '" + fileNameFixed + "'")
                
                while (initCheck(fileNameFixed)) == False: #Keep checking the fileName till fully cleaned and formatted
                    #Formate clean text in fileName
                    if formating == False:
                        fileNameFixed = autoFormat(fileName, repChars) #Rename File via "autoFormat" function
                        print("Fixed File Name = '" + fileNameFixed + "'")

                    #Clean bad text from fileName
                    if badText == True:
                        fileNameFixed = autoRemove(fileNameFixed, rmChars) #Rename File via "autoRemove" function
                        print("Crap removed - '" + fileNameFixed + "'")
                        
                    print("Repair Check")
                    initCheck(fileName) #Check fileName for clean formatted text

                fileNameFixed = finalCheck(fileNameFixed)

                    
                #rename(addExt(fileName), addExt(fileNameFixed)) #Renames file with the "fixed" name
                rename(path.join(fileDir, addExt(fileName)), path.join(fileDir, addExt(fileNameFixed)))
                print("File Renamed: " + addExt(fileNameFixed))
                   
                
            elif initCheck(fileName) == True:
                print("Already Formated")
            currentFile += 1 #Add 1 to currentFile as the currentFile has been processed
            
        else:
            debugPrints() #Display all debug information
            print("Invalid Extension or Folder")
            currentFile += 1 #Add 1 to currentFile as the currentFile has been processed
