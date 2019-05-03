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
DEFAULT_PARAMETER_LIST_INSTRUCTION = ['Header','Amount','Cc','From','To']
DEFAULT_PARAMETER_LIST_INSTRUCTION_HEADER = ['Time','Tid','Fid','Uid','Sid','User','RealUser','Context','Records']
DEFAULT_PARAMETER_LIST_INSTRUCTION_FROM = ['Fri','OffNet','Message','Available','RFri','Cc','FROParents','Fri','SP','FRO','Rate','OffNet','OfferIdentities','Amount','AccountHolder','Committed','Total','BankDomainName','IFee']
DEFAULT_PARAMETER_LIST_INSTRUCTION_FROM_AVAILABLE = ['After','Before']
DEFAULT_PARAMETER_LIST_INSTRUCTION_FROM_FRO = ['MSISDN','Id','UserProfile']
DEFAULT_PARAMETER_LIST_INSTRUCTION_FROM_ACCOUNTHOLDER = ['MSISDN','Id','UserProfile']
DEFAULT_PARAMETER_LIST_INSTRUCTION_FROM_COMMITED = ['After','Before']
DEFAULT_PARAMETER_LIST_INSTRUCTION_FROM_TOTAL = ['After','Before']
DEFAULT_PARAMETER_LIST_INSTRUCTION_TO = ['Fri','OffNet','Message','Amount','RFri','Cc','Fri','SP','FRO','Rate','OffNet','BankDomainName']
DEFAULT_PARAMETER_LIST_INSTRUCTION_TO_FRO = [ 'Username','Id','UserProfile']
DEFAULT_PARAMETER_LIST_STATUS = ['Code','Msg']
DEFAULT_PARAMETER_LIST_HEADER = ['Type','Ver']

# - 3 Level dictionaries
INTERNAL_INSTRUCTION_ITEMS_LEVEL_3 = ['Available','FRO','FROParents','Committed','AccountHolder','Total']
INTERNAL_INSTRUCTION_SUBKEYS_LEVEL_3 = ['From','To']

# - Separator
SEPARATOR = ';'
ITEM_SEPARATOR = '.'

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

    @staticmethod
    def cleanAtoms(myValue):
        if type(myValue) == unicode:
            renValue = myValue.encode('ascii')
        else:
	    renValue = str(myValue)
	return renValue

    @staticmethod
    def printInvalidKeys(listName,key,subkey):
        INTERNAL_LONG_DETAIL_STRING = 'Missing Key or SubKey to be reported: ' 
	INTERNAL_SEPARATOR = ' : '
	internalString = INTERNAL_LONG_DETAIL_STRING + listName + INTERNAL_SEPARATOR + key + INTERNAL_SEPARATOR + subkey
	print internalString

    def printJsonDetail(self):
        for myFile,jsonDictionary in self.myJSONObjects:
	    # - Get the object dictionary
	    print jsonDictionary
	    for key in jsonDictionary.keys():
		# - Validate keys
                if key in DEFAULT_KEYS:
		    if isinstance(jsonDictionary[key],dict):
                        if key == 'Instruction':
			    # - Instruction
			    for myInternalKey in jsonDictionary[key].keys():
		                if myInternalKey in DEFAULT_PARAMETER_LIST_INSTRUCTION:
				    if isinstance(jsonDictionary[key][myInternalKey],dict):
				        # - Dictionary
					if myInternalKey in INTERNAL_INSTRUCTION_SUBKEYS_LEVEL_3:
					    # - Process From and To
                                            print jsonDictionary[key][myInternalKey].items()
					else:
					    # - Process other subKeys
			                    for value in jsonDictionary[key][myInternalKey].items():
				                myTupleName, myTupleValue = value
                                                myTupleNameRen = JSONFileBox.cleanAtoms(myTupleName)
					        myTupleNameRen = key + ITEM_SEPARATOR + myInternalKey + ITEM_SEPARATOR + myTupleNameRen
                                                myTupleValueRen = JSONFileBox.cleanAtoms(myTupleValue)
				                myFinalTuple = ( myFile, myTupleNameRen, myTupleValueRen )
				                self.myFinalList.append(myFinalTuple)
				    else:
			                # - Atomic
				        myTupleName = myInternalKey
				        myTupleValue = jsonDictionary[key][myInternalKey]
				        myTupleNameRen = JSONFileBox.cleanAtoms(myTupleName)
				        myTupleNameRen = key + ITEM_SEPARATOR + myTupleNameRen
				        myTupleValueRen = JSONFileBox.cleanAtoms(myTupleValue)
				        myFinalTuple = ( myFile, myTupleNameRen, myTupleValueRen )
				        self.myFinalList.append(myFinalTuple)
				else:
			            JSONFileBox.printInvalidKeys("DEFAULT_PARAMETER_LIST_INSTRUCTION",key,myInternalKey)
                        else:
			    # - Other keys
			    for myInternalKey in jsonDictionary[key].keys():
			        if myInternalKey in DEFAULT_PARAMETER_LIST_STATUS or myInternalKey in DEFAULT_PARAMETER_LIST_HEADER:
                                    myTupleNameRen = JSONFileBox.cleanAtoms(myInternalKey)
				    myTupleNameRen = key + ITEM_SEPARATOR + myTupleNameRen
                                    myTupleValueRen = JSONFileBox.cleanAtoms(jsonDictionary[key].get(myInternalKey))
				    myFinalTuple = ( myFile, myTupleNameRen, myTupleValueRen )
				    self.myFinalList.append(myFinalTuple)
			        else:
				    JSONFileBox.printInvalidKeys("DEFAULT_PARAMETER_LIST_STATUS",key,myInternalKey)
				    JSONFileBox.printInvalidKeys("DEFAULT_PARAMETER_LIST_HEADER",key,myInternalKey)
		    else:
			JSONFileBox.printInvalidKeys("MONOLITIC_VALUE",key,'EMPTY')
	        else:
		    JSONFileBox.printInvalidKeys("DEFAULT_KEYS",key,'EMPTY')
            
	#print self.myFinalList
        myTemporalString = ''
	for myFile in self.myJSONFileList:
	    for myTup in self.myFinalList:
	        if myFile == myTup[0]:
	            myTemporalString = myTemporalString + myTup[1] + ITEM_SEPARATOR +  myTup[2] + SEPARATOR
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
#finalReport1.printFinalReport(jsonfile1.myFinalStringList)
