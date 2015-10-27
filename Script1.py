'''
Textmining Project
10/27/15
Scripts written by Mallika Dey, Jesse Lund, and Leah Wolosianski
The following script uses a set of several functions from S2A to generate a term vector from a directory
that contains a link to all 325 Friends episodes
We subsequent ran cluster analysis on our dataset to identify common themes across the various 
'''

import os 
path = ('Path to Script2a')
os.chdir(path)
import Script2A as lw
import nltk
import urllib2
import re
import string

import glob
import pandas as pd
path = '/Users/jlund/Desktop/VM-Share/IAA_MSA/Fall2_TextMining/friendsalltranscripts/'
files=glob.glob(path+"*.html")

urls = []

for x in files:
    url =  'file:///Users/jlund/Desktop/VM-Share/IAA_MSA/Fall2_TextMining/friendsalltranscripts/'+x.split('pts/')[-1]
    urls.append(url)
del(path, files, url)

terms = set()
dics = []
scenes = []
episodes=[]
SceneText = []
Unstemmed = []
term_vec = []

for x in urls:
	texts = lw.gettexts(x)
	episode, sceneindex = lw.indexes(x, texts)
	SceneText.append(texts)
	episodes.append(episode)
	scenes.append(sceneindex)
# Flatten list of lists[item for sublist in l for item in sublist]
scenes = [item for sublist in scenes for item in sublist]
episodes = [item for sublist in episodes for item in sublist]
SceneText = [item for sublist in SceneText for item in sublist]
for x in SceneText:
	x = lw.sceneterms(x)
	term_vec.append(x)
print("Done with creating term vector")

## Flatten the term vec and turn it into a set:
All_Words = [item for sublist in term_vec for item in sublist]
All_Words = set(All_Words)


###This block gives me the guide from all words to stemmed word
Stemmed = []
porter = nltk.stem.porter.PorterStemmer()
for i in All_Words:
    Stemmed.append(porter.stem(i))
SceneText = pd.DataFrame(SceneText)
print('scene to csv starting')
SceneText.to_csv("SceneText.csv")
print('scene to csv done')
VocabFrame = pd.DataFrame ({'words':list(All_Words)},index=Stemmed)
VocabFrame.to_csv("VocabFrame.csv")

Stemmed = set(Stemmed)
for i in term_vec:
	dictionary = lw.TermLists(i)
	dics.append(dictionary)

for d in dics:
	for word in Stemmed:
			if word in d:
				pass 
			else:
				d[word]=0



docs = []
for d in dics:
	doc = []
	for term in Stemmed:
		doc.append(d[term])	
	docs.append(doc)

df = pd.DataFrame(docs, columns = Stemmed)

df['episodes']= episodes
df['scene']= scenes
print('starting df to csv')
df.to_csv('output.csv')


