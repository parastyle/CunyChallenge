import csv
import sqlite3
import os


cwd = os.getcwd() # Establish current directory

class CunyChallenge(): #The class we'll be usisng
    def __init__(self):
        print 'Attention: Please execute this code in the same directory as your database'
        self.parameterChecks = []
        self.selectDb()
        self.createConnectDb()
        self.selectTable() ###Basic initialization stuff
###################################################################################

    def setParameters(self):
        pass #If you want to expand upon anything, add it here

    def selectDb(self): #This method selects all files in the CWD that end with .db
        self.possibleDb ={}
        self.numberOfDbs = 0
        for item in os.listdir(os.getcwd()):
            if '.db' in item[-3:]:
                self.numberOfDbs += 1
                self.possibleDb[str(self.numberOfDbs)] = item
            else:
                pass
        print 'Please enter the corresponding number to select database (e.g. \'1\') '
        self.displayList(self.possibleDb)    
        self.dictValidation(self.possibleDb)     
        print 'Now connected to ' + self.possibleDb[self.choice]
         

    def selectTable(self):# This method finds all the tables in your selected .db and helps you choose one
        self.fetchedTables = self.c.execute('''SELECT name FROM sqlite_master WHERE type='table' ''').fetchall()
        self.tableDict = {}
        self.numberOfTables = 0
        for item in self.fetchedTables:
            self.numberOfTables += 1
            self.tableDict[str(self.numberOfTables)] = item
        print 'Please enter the corresponding number to select table (e.g. \'1\') '
        self.displayList(self.tableDict)
        self.dictValidation(self.tableDict)
        print 'You\'ve selected table ' + str(self.tableDict[self.choice])[2:11]

    def chooseColumns(self): #Choose up to two columns to be displayed
        self.fetchedColumns = self.c.execute('''PRAGMA table_info(%s); ''' %self.tableDict[str(self.choice)]).fetchall()
        self.columnDict = {}
        self.numberOfColumns = 0
        for item in self.fetchedColumns:
            self.numberOfColumns += 1
            self.columnDict[str(self.numberOfColumns)] = item[1]
        print 'Please enter the corresponding numbers to select column (e.g. \'2 4\') '
        self.displayList(self.columnDict)
        self.columnsChosen = raw_input(' >__  ').replace(" ","")
        #self.columnsChosen.replace(" ","")
        self.characterCounter = 0
        while True:
            if len(self.columnsChosen) == 0 or len(self.columnsChosen)>=3:
                print 'You\'ve either entered a number out of range, or entered something other than numbers'
                self.displayList(self.columnDict)
                self.columnsChosen = raw_input(' >__  ').replace(" ","")

            elif self.characterCounter == len(self.columnsChosen):
                break
            elif self.columnsChosen[self.characterCounter] in self.columnDict:
                self.characterCounter += 1
            else:
                print 'You\'ve either entered a number out of range, or entered something other than numbers'
                self.displayList(self.columnDict)
                self.columnsChosen = raw_input(' >__  ').replace(" ","")

                
    def showData(self):
        #self.columnsChosen = self.columnsChosen.replace("", ",")[1: -1]
        try:
            self.c.execute('''SELECT %s, %s FROM %s LIMIT 30''' % (self.columnDict[self.columnsChosen[0]], self.columnDict[self.columnsChosen[1]] , str(self.tableDict[self.choice])[2:11] ))
            print str(self.columnDict[self.columnsChosen[0]]) +'    ' +str(self.columnDict[self.columnsChosen[1]])
        except:
            self.c.execute('''SELECT %s FROM %s LIMIT 30''' % (self.columnDict[self.columnsChosen[0]], str(self.tableDict[self.choice])[2:11]))
            print str(self.columnDict[self.columnsChosen[0]])
        for row in self.c.fetchall():
            print row

    def createConnectDb(self): #Connects to the .db
        self.conn = sqlite3.connect(self.possibleDb[self.choice])
        self.c = self.conn.cursor()

    def displayList(self,dictionary): #A simple method for displaying a list
        for pair in dictionary:
            print 'Enter ' + str(pair) + ' for '+ str(dictionary[pair])

    def dictValidation(self,dictionary): #validates your answer through a dictionary
         while True:
            self.choice = raw_input(' >__  ')
            if self.choice in dictionary:
                break
            else:
                print '\nTry to only type in the corresponding number to the list below'
                self.displayList(dictionary)        


x = CunyChallenge()
x.chooseColumns()
x.showData()
#b = x.c.execute('''PRAGMA table_info(CunyCSV);''')
