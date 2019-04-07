from sklearn.linear_model import LinearRegression
import numpy as np
import os
import random
from Rankingalgorithmus import Rankingnummer
from preprocess import run_complete_pipeline

#X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
#y = np.dot(X, np.array([1, 2]))
#y = [1,2,1,3]
#reg = LinearRegression().fit(X, y)
#print(reg.coef_)

class Absatz:
    def __init__(self, num, text, textProcessed=None):
        self.num = num
        self.text = text
        if textProcessed is None:
            self.textProcessed = run_complete_pipeline(text)
        else:
            self.textProcessed = textProcessed
            
def makeTrainingData(word, norm, featureList, resultsForHumans, numSamples):
    output = ""
    feats = []
    for index in random.sample(range(len(featureList)), numSamples):
        output += resultsForHumans[index] + "\n\n" + "#"*40 +"\n\n"
        feats += featureList[index]
    outfile = "results_{}_{}.txt".format(word, norm)
    with open(outfile, "w", encoding="utf-8") as outf:
        outf.write(output)
    # Ergebnisse der Annotatoren in dieser Reihenfolge sind dann unser y
    print("Created {} training instances".format(len(feats)))
    return
    
def makeFeatures():
    feats = []
    for filename in os.listdir("zumAnnotieren"):
        with open(os.path.join("zumAnnotieren/",filename), encoding='utf-8') as f:
            absaetze = f.read().split("#"*40)
            for abs in absaetze[:-1]:
                text = abs
                absatz = Absatz(1,text)
                features = Rankingnummer(absatz)[1]
                feats.append(features)
    print("Created {} training instances".format(len(feats)))
    return feats
                
    
    
def fitParameters(X_train, y_train):
    reg = LinearRegression().fit(X_train, y_train)
    return reg.coef_