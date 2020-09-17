import nltk
from nltk import UnigramTagger
from nltk.tag.brill import *
import nltk.tag.brill_trainer as btrainer
from pickle import dump,load
from nltk.probability import FreqDist
from nltk.tag import untag
from tagger import sentenceTagger
###################################################################################
def fileWrite(filename,corpora):
    file = open(filename, "w")
    file.write(str(corpora))
    file.close()
def tagFrequency(corpora):
    frequencyOfTags = dict()
    for i in corpora:
        for j in i:
            if j[1] not in frequencyOfTags.keys():
                frequencyOfTags.update({j[1]:0})
            frequencyOfTags[j[1]] += 1
    return frequencyOfTags
def saveTagger(tagger):
    output = open('Hiligaynon tagger.pickle', 'wb')
    dump(tagger, output, -1)  
    output.close()
def readCorpus(filename):
    corpus = []
    with open(filename) as file:
        for line in file:
            sentences = []
            for pair in line.split():
                sentences.append(tuple(pair.split('/')))
            corpus.append(sentences)
    file.close()
    return corpus
####################################################################################
    
filename = 'Hiligaynon Corpus with tags.txt' #Corpora
#sentences = readPerLine(filename) #Read Corpora by line
bigList = readCorpus(filename) #Convert to list of list of tuples
#print(len(bigList))#Number of sentences
takenPercent = int((len(bigList)*(0.8))) #Get 80% for training
trainingData = bigList[:takenPercent]#Get 80% for training
testingData = bigList[takenPercent:]# Remaining for testing
#print(testingData) #Testing Data to be used
#print(len(trainingData),len(testingData)) #Print the size of the data
tagged_sentences = trainingData

Input = open('Hiligaynon tagger.pickle', 'rb')
tagger = load(Input)
Input.close()
