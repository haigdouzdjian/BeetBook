import csv
import json
from utils import *

#takes in meta and entries dictionary and saves to file
def saveJSON(file,meta,entries):
    try:
        with open(file,'w') as book:
            tempDict = {}
            tempDict["meta"] = meta
            tempDict["entries"] = entries
            json.dump(tempDict,book,indent=4)
    except IOError:
        print("Error Opening Output File")

#takes in file and returns dictionary of metadata
def getMetaJSON(file):
    try:
        with open(file,'r') as book:
            dict = json.load(book)
            dict = dict.get("meta")
            return dict
    except IOError:
        print("Error Getting JSON Metadata")

#takes in file and returns array of dictionaries containing entries
def getEntriesJSON(file):
    try:
        with open(file,'r', encoding = 'utf-8') as book:
            dict = json.load(book)
            dict = dict.get("entries")
            return dict
    except IOError:
        print("Error Getting JSON Entries")

def getJSON(filename):
    try:
        with open(filename, 'r') as book:
            dictionary = json.load(book)
            return dictionary
    except IOError:
        log('Error loading address book: {}'.format(filename), logging.ERROR)

#returns single dictionary of metadata
def getMetaTSV(file):
    try:

        with open(file,newline='') as book:

            #using the csv standard reader to interpret the line as a string
            bookReader = csv.reader(book,delimiter='\t')

            #empty dictionary declaration
            metaDict = {}

            #splits line based on ':' delimiter
            line = next(bookReader)[0].split(':')

            #Check to see if the line is metadata
            while line[0] == 'meta':

                # add metadata to initialized dict and proceed to next line
                metaDict[line[1]] = line[2]
                line = next(bookReader)[0].split(':')

        return metaDict
    except:
        log('Error loading address book: {}'.format(file), logging.ERROR)

#returns list of dictionaries representing entries
def getEntriesTSV(file):
    try:
        with open(file,newline='') as book:

            # When initializing the DictReader the current line is interpreted as
            # the keys so we will need to move to the appropriate position
            # need to substract 1 so we end on the previous line \n
            seekLocation = getEntriesStart(file) - 1
            book.seek(seekLocation+1)

            # initialize the DictReader with proper keys/header location
            bookReader = csv.DictReader(book,delimiter='\t')

            # create a list of all entries
            entries = []
            for line in bookReader:
                entries.append(line)
        return entries
    except:
        log('Error loading address book: {}'.format(file), logging.ERROR)

#returns the start location of entries / the end location of the metadata
def getEntriesStart(file):
    try:

        with open(file,newline='') as book:

            #using the built in reader
            line = book.readline()

            # will need to return 0 if there is no metadata so as to navigate to
            # the beginning of the file
            end = 0

            while 'meta' in line:
                end += len(line)
                line = book.readline()

        return end
    except:
        log('Error loading address book: {}'.format(file), logging.ERROR)

#writes metadata and entries to TSV. Metadata is a dictionary and entries is list of dictionaries
def saveTSV(file,entries):
    try:

        with open(file,'w',newline='') as book:

            #create dictWriter
            bookWriter = csv.DictWriter(book,fieldnames=entries[0].keys(), delimiter="\t")

            #write the header line
            bookWriter.writeheader()

            #write all entries provided
            for entry in entries:
                bookWriter.writerow(entry)
    except:
        log('Error loading address book: {}'.format(file), logging.ERROR)