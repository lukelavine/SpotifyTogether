import numpy
from sklearn import preprocessing
import numpy as np
import numpy.linalg as npla
import random
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import Perceptron
from sklearn.ensemble import RandomForestClassifier

minsim = .75

clfs = [
        MLPClassifier(hidden_layer_sizes=50, max_iter=100),
        DecisionTreeClassifier(),
        Perceptron(),
        RandomForestClassifier()
]

#Get audio features for a list of tracks
def audiofeatures(sp, ids):
	features = sp.audio_features(ids)
	tracks = list()
	for feat in features:
		track = list()
		track.append(feat['id'])
		track.append(feat['danceability'])
		track.append(feat['energy'])
		track.append(feat['key'])
		track.append(feat['loudness'])
		track.append(feat['mode'])
		track.append(feat['speechiness'])
		track.append(feat['acousticness'])
		track.append(feat['instrumentalness'])
		track.append(feat['liveness'])
		track.append(feat['valence'])
		track.append(feat['tempo'])
		tracks.append(track)
	return tracks

# Converts our data from string values to float.
def converttofloat(inlist):
    retlist = list()
    for j in inlist:
        templist = list()
        for i in j[1:]:
            templist.append(float(i))
        retlist.append(templist)
    return retlist


# Normalizes our data.
def normalizedata(infeat):
    featvals = list()
    for i in infeat:
        i[2] /= 11
        i[3] /= -60
        i[10] /= 200
    return infeat


# Generates and returns a list of data dissimilar to our input data set.
def generatefalsedata(innorm):
	fakesongs = list()
    i = 0
    while i < len(inorm):
        toosim = False
        fakesong = random.uniform(0.0, 1.0, size=(1,10))
        for song in innorm:
            cosinesimlarity(song, fakesong)
            if cosinesimlarity(song, fakesong) > minsim:
                toosim = True
                break
        if not toosim:
            fakesong.append(float(-1))
            fakesongs.append(fakesong)
            i += 1
    return fakevals


# Computes cosine similarity between two songs and return sim.
def cosinesimlarity(list1, list2):
    return np.dot(list1, list2) / (npla.norm(list1) * npla.norm(list2))


# Train our data on a classifier.
def runonclf(indata, inlabels):
    X_train, X_test, y_train, y_test = train_test_split(indata, inlabels, test_size=.25)
    retclf = list()
    for clf in clfs:
        clf.fit(X_train, y_train)
        preds = clf.predict(X_test)
        print(accuracy_score(y_test, preds))
        retclf.append(clf)
    return retclf


def printlist(inlist):
    count = 1
    for l in inlist:
        print(count, l)
        count += 1
    #input()

def runprog(sp, tracks):
    #Get features for audio tracks
	features = audio_features(sp, tracks)
	
	# Our non-normalized data
    features = converttofloat(features)

    # Our data normalized without the label
    features = normalizedata(features)

    # The fake data we will use to train our ML alg
    fakedata = generatefalsedata(features)

    # The data to be used to train our ML alg (has labels)
    for n in features:
        n.append(float(1))

    # Appends all of our data into one list for training/testing.
    alldata = list()
    alllabels = list()
    for i in range(len(features)):
        alldata.append(features[i][:-1])
        alldata.append(fakedata[i][:-1])
        alllabels.append(features[i][-1])
        alllabels.append(fakedata[i][-1])
    # Trains and tests our data on an ML algorithm
    clfs = runonclf(alldata, alllabels)
    return clfs
