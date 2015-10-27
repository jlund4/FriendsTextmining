
'''
set of routines for formatting, cleaning, and preparing the data
for subsequent analysis
'''

# import libraries
import urllib2
import re
import nltk
import string
#from collections import Counter #used to count term occurance from Scene_Terms list

import os 
path1 = ('FilePAth')
os.chdir(path1)
from collections import Counter 


def gettexts(urlin):
    #set url
    url=urlin
    pos = url.rfind('/')
    EpisodeID = url[pos+1:- 5]
    del(pos)
    
    sock = urllib2.urlopen(url)
    htmlSourceLines = sock.readlines()
    sock.close()
    #print htmlSourceLines
    

      
    
    ### Create a list of strings from the lines of the html file###
    #create a blank list to read the html lines into
    list_1 = []
    #clean up formatting from html lines and read into a list
    for index in range(0,len(htmlSourceLines)):
        temp1 = re.sub(r'<.+?>', '', htmlSourceLines[index])
        list_1.append(str(temp1))
        del(temp1)
        del(index)
    #remove beginning and end of line characters from the list
    list_1=[x.rstrip() for x in list_1]
    #remove blank lines fromm the list
    list_1=filter(None, list_1)
    del(x, htmlSourceLines)
    
    Scene_Ind = []
    #find the index number of strings that contain '[Scene' to indicate the beginning of a scene
    Scene_Ind = [i for i, s in enumerate(list_1) if '[Scene' in s]
    #add an item for end of file so that we can read all scenes in and don't miss the last one
    Scene_Ind.append(len(list_1))
    if len(Scene_Ind) == 1:
        Scene_Ind.insert(0,5)
    #print Scene_Ind
    
    ##Print the Scenes into a list by Scene##
    #Create a blank array to print the scenes into - 
    
    All_Scenes=[]
    for index in range(0,len(Scene_Ind)-1):
        Scene = list_1[Scene_Ind[index]:Scene_Ind[index+1]-1]
        Scene_1 = ' '.join(Scene)
        All_Scenes.append(Scene_1)
        #print All_Scenes[index]
    del(Scene, Scene_1, index, list_1, Scene_Ind)
    newlist = [] 
    for foo in All_Scenes:
        newlist.append(foo)   
    
    
    #remove punctuation that is leading to splitting errors  
    punctuation=['.','(',')', '-', "'", '[', ']', '&nbsp', '&quot', '&', ',', '--'] # list of punctuation to be replaced with a space
    All_Scenes_Clean = [] #create a new list to read clean strings into
    
    names = ['Monica:', 'Chandler:', 'Joey:', 'Phoebe:', 'Rachel:', 'Ross:']
    for scene in range(0,len(All_Scenes)):
        i = newlist[scene]
        for punc in range(0,len(punctuation)):
            i = i.replace(punctuation[punc],' ')
        i="".join([x for x in i if ord(x) < 128])
        i= "".join([x for x in i if not x.isdigit()])
        for n in names:
            i= i.replace(n, '')
        All_Scenes_Clean.append(i)
    #del(punc, scene, All_Scenes, punctuation, i)
    return All_Scenes_Clean

def indexes(url, list):
    scene = []
    for x in range(len(list)):
        scene.append(x+1)
    pos = url.rfind('/')
    episode = url[pos+1:len(url) - 5]
    episode = [episode]*len(list)
    
    return episode, scene

def sceneterms(scenetext):
    punc = re.compile('[%s]' % re.escape(string.punctuation))
    string.punctuation
    term_vec = [] 
    scenetext=scenetext.lower()
    scenetext = punc.sub('', scenetext)   
    term_vec = (nltk.word_tokenize(scenetext))
    term_list = [word for word in term_vec if word not in nltk.corpus.stopwords.words('english')]     
    return term_list
   # del(i, term, term_list)
   # del(stop_words)

def TermLists(Scene_Terms):
    terms = []
    porter = nltk.stem.porter.PorterStemmer()
    for i in Scene_Terms:
        terms.append(porter.stem(i))   
    Term_Dict = {}      
    Term_Dict = Counter(terms)
    return Term_Dict













