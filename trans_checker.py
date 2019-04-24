#!/usr/bin/env python

#+-+-+-+-+-+ +-+-+-+-+-+-+-+
#|T|R|A|N|S| |C|H|E|C|K|E|R|
#+-+-+-+-+-+ +-+-+-+-+-+-+-+

# - Imports 
import sys
import json
import os
import string
from random import *
import re
#import pdb
#import ast

# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

# - Static definitions
FILE_DOES_NOT_EXIST_TRUE = "Source file doesn't exist"

# - Valid Keys
DEFAULT_KEYS = ['Header','Instruction','Status']

# - Valid Parameters
DEFAULT_PARAMETER_LIST_INSTRUCTION = ['Time','Tid','Fid','Uid','Sid','User','RealUser','Context']
DEFAULT_PARAMETER_LIST_STATUS = ['Code']
DEFAULT_PARAMETER_LIST_HEADER = ['Type','Ver']

# - Temporal list
DEFAULT_PARAMETER_LIST_INSTRUCTION_TEMP = ['Time','Tid','Fid','Sid','User','RealUser','Context']

# - Separator
SEPARATOR = ','

# +-+-+-+-+-+ +-+-+-+-+-+-+-+-+-+-+
# |C|L|A|S|S| |D|E|F|I|N|I|T|I|O|N|
# +-+-+-+-+-+ +-+-+-+-+-+-+-+-+-+-+

class OsAgent:
    parametersList = []
    parametersSize = 0
    myFile = ""
    #myKey = []
    #myParametersPerKey = []
    myFileExist = 0

    def argumentList(self,list):
        self.parametersList = list

    def countMyParameters(self):
        self.parametersSize = len(self.parametersList)

    def parsingParameters(self):
        self.myFile = self.parametersList[1]
	#self.myKey = self.parametersList[2]

    def checkSourceFile(self,myInt):
	self.myFileExist = myInt

    @staticmethod
    def clearScreen():
        os.system('clear')

    @staticmethod
    def elegantExit():
	sys.exit()

# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

class JSONFileBox:
    allchar = string.ascii_letters + string.digits
    minMax = (8,12)
    FILE_NAME = "JSON."
    currentQueryFileName = ""
    currentFile = None
    myJSONFileList = []
    myJSONObjects = []
    myFilterResult = []
    myFinalList = []
    myTemporalNames = []
    myTemporalValues = []
    myTemporalCleanNames = []
    myTemporalCleanValues = []
    myFinalLongStringNames = ""
    myFinalLongStringValues = ""
    myFinalStringList = []

    def dumpMyJsonToFile(self,myJSON):
        min_char, max_char = self.minMax
	randomExtension = "".join(choice(self.allchar) for x in range(randint(min_char, max_char)))
	with open(myJSON,'r') as jsonRaw:
	    for indice,jsonData in enumerate(jsonRaw):
	        self.currentQueryFileName = self.FILE_NAME + str(indice) + '.' + randomExtension + '.json'
		with open(self.currentQueryFileName,'w') as write_file:
		    write_file.write(jsonData)
		    self.myJSONFileList.append(self.currentQueryFileName)

    def loadJsons(self):
	for myfile in self.myJSONFileList:
	    myTempString = open(myfile,'r').read()
	    os.remove(myfile)
	    # - Check Json Detail
	    tempJson = json.loads(myTempString)
	    temporalTuple = ( myfile, tempJson )
	    #self.myJSONObjects.append(tempJson)
	    self.myJSONObjects.append(temporalTuple)

    def printJsonDetail(self):
	#print self.myJSONObjects
        for myFile,jsonDictionary in self.myJSONObjects:
	    # - Get the object dictionary
	    for key in jsonDictionary:
                # - Get the main keys
		for index1,subValue in enumerate(jsonDictionary[key]):
			if key == 'Instruction':
		            for index2,instructionValue in enumerate(jsonDictionary[key][subValue]):
			        if instructionValue in DEFAULT_PARAMETER_LIST_INSTRUCTION_TEMP:
				    #print jsonDictionary[key][subValue][instructionValue]
				    myValue = jsonDictionary[key][subValue][instructionValue]
				    myTuple = (myFile,instructionValue,myValue)
                                    self.myFilterResult.append(myTuple)
	
	#print self.myFilterResult
	for indice,everyTuple in enumerate(self.myFilterResult):
	    myFileName, myName, myValue = everyTuple

	    if type(myName) == unicode:
	        myRenName = myName.encode('ascii')
	    else:
		myRenName = str(myName)

	    if type(myValue) == unicode:
	        myRenValue = myValue.encode('ascii')
	    else:
		myRenValue = str(myValue)
            
            myRenTuple = (myFileName,myRenName,myRenValue)
            self.myFinalList.append(myRenTuple)

        myTemporalString = ''
	for myFile in self.myJSONFileList:
	    for myTup in self.myFinalList:
	        if myFile == myTup[0]:
	            myTemporalString = myTemporalString + myTup[2] + ','
	    if myTemporalString:
                myTemporalString = myTemporalString[:-1]
	        self.myFinalStringList.append(myTemporalString)
	    myTemporalString = ''

        #print self.myFinalList
	#print self.myFinalStringList
	#print self.myJSONFileList

# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
class FinalReport:
    myFinalReport = []

    def printFinalReport(self,myLista):
        for i in myLista:
	    print i

# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

# +-+-+-+-+-+-+-+-+-+-+ +-+-+-+-+-+
# |D|E|P|L|O|Y|M|E|N|T| |L|O|G|I|C|
# +-+-+-+-+-+-+-+-+-+-+ +-+-+-+-+-+

# - Set Trace
#pdb.set_trace()

# - Objects
os1 = OsAgent()
jsonfile1 = JSONFileBox()
finalReport1 = FinalReport()

# - Parsing values for parameters
os1.argumentList(sys.argv)
os1.countMyParameters()

if os1.parametersSize > 1:
    os1.parsingParameters()

# - Confirm directory exist
if os.path.exists( os1.myFile ):
    os1.checkSourceFile(1)
else:
    os1.checkSourceFile(0)
    OsAgent.clearScreen()
    print(FILE_DOES_NOT_EXIST_TRUE)
    OsAgent.elegantExit()

# - Separate the JSON in transactions
jsonfile1.dumpMyJsonToFile(os1.myFile)
jsonfile1.loadJsons()
jsonfile1.printJsonDetail()
#print finalReport1.myFinalReport
#print jsonfile1.myFinalLongStringNames
finalReport1.printFinalReport(jsonfile1.myFinalStringList)

