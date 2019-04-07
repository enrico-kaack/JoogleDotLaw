import json
import os
import inspect
import re
from bs4 import BeautifulSoup
from preprocess import run_complete_pipeline
from Rankingalgorithmus import Rankingnummer
from nltk.stem.snowball import SnowballStemmer
from flask import Flask
from collections import defaultdict
from nltk.metrics import edit_distance
from regression import makeTrainingData, makeFeatures, fitParametersLinear, fitParametersLogistic, predictClass



class Urteil:
    def __init__(self, dic, reload=False):
        self.doknr = dic["doknr"]
        self.ecli = dic["ecli"]
        self.gertyp = dic["gertyp"]
        self.gerort = dic["gerort"]
        self.spruchkoerper = dic["spruchkoerper"]
        self.aktenzeichen = dic["aktenzeichen"]
        self.doktyp = dic["doktyp"]
        self.vorinstanz = dic["vorinstanz"]
        self.mitwirkung = dic["mitwirkung"]
        self.tenor = dic["tenor"]
        self.tatbestand = dic["tatbestand"]
        self.sonstlt = dic["sonstlt"]
        self.identifier = dic["identifier"]
        self.coverage = dic["coverage"]
        self.language = dic["language"]
        self.publisher = dic["publisher"]
        self.accessRights = dic["accessRights"]
        self.leitsatz = dic["leitsatz"]
        if not reload:            
            self.entschDatum = dic["entsch-datum"]            
            self.regionAbk = dic["region"]["abk"]
            self.regionLong = dic["region"]["long"]
            self.titel = dic["titelzeile"]
            self.norm = []
            norm = dic["norm"].split(",")
            for n in norm:
                n = re.sub("Abs \d ", "", n)
                self.norm.append(n.strip())
            if (len(dic["entscheidungsgruende"]) > 0):
                self.gruende = dic["entscheidungsgruende"]
            else:
                self.gruende = dic["gruende"]
            self.abweichendeMeinung = dic["abwmeinung"]
            self.absaetze = self._findAbsaetze()
            self.gruendeProcessed = run_complete_pipeline(self.gruende)
            
        else:
            self.gruende = dic["gruende"]
            self.gruendeProcessed = dic["gruendeProcessed"]
            self.entschDatum = dic["entschDatum"]            
            self.regionAbk = dic["regionAbk"]
            self.regionLong = dic["regionLong"]
            self.titel = dic["titel"]
            self.norm = []
            normen = dic["norm"]
            for n in normen:
                n = re.sub("Abs \d ", "", n)
                self.norm.append(n.strip())
            self.absaetze = dic["absaetze"]
            
    def _findAbsaetze(self):
        absaetze = []
        soup = BeautifulSoup(self.gruende, 'html.parser')
        for dl in (soup.find_all('dl')):
            soup2 = BeautifulSoup(str(dl), 'html.parser')
            if len(soup2.find_all('a')) == 1:
                num = soup2.find_all('a')[0].string
                text = soup2.find_all('p')[0].string
                if text is None:
                    text = soup2.find_all('p')[0].text
                #absatz = Absatz(num, text)
                absatz = dict()
                absatz["num"] = num
                absatz["text"] = text
                absatz["textProcessed"] = run_complete_pipeline(text)
                absaetze.append(absatz)

        return absaetze


class Absatz:
    def __init__(self, num, text, textProcessed=None):
        self.num = num
        self.text = text
        if textProcessed is None:
            self.textProcessed = run_complete_pipeline(text)
        else:
            self.textProcessed = textProcessed

        
        
class Norm:
    def __init__(self, paragraph, title, text):
        self.paragraph = paragraph
        self.title = title
        self.text = text

    def isTextInNorm(self, searchText):
        pass #TODO should we do this???
        
    
    
def saveUrteile(urteilListe):
    for urteil in urteilListe:
        filen = urteil.doknr + ".json"
        with open(os.path.join("urteile/",filen), "w", encoding="utf-8") as f:
            json.dump(urteil.__dict__, f)
            
def loadUrteile():
    urteilListe = []
    for filename in os.listdir("urteile"):
        with open(os.path.join("urteile/",filename), encoding='utf-8') as json_file:
            d = json.load(json_file)
            #print(d.keys())
            u = Urteil(d, True)
            urteilListe.append(u)
    return urteilListe
    
  
def setup(reloadUrteile=False):
    urteilListe = []
    bgb = []
    stgb = []
    normIndex = []

    # read and save all urteile
    if not reloadUrteile:
        for filename in os.listdir("StR"):
            with open(os.path.join("StR/",filename), encoding='utf-8') as json_file:
                d = json.load(json_file)
                u = Urteil(d)
                urteilListe.append(u)
        saveUrteile(urteilListe)
    else: # reload all urteile
        urteilListe = loadUrteile()

    # read norms for bgb
    with open("bgb.json") as bgb_file:
        d = json.load(bgb_file)
        for norm in d["normen"]:
            if "sentencedtext" in norm and "artpara" in norm and "title" in norm:
                n = Norm(norm["artpara"], norm["title"], norm["sentencedtext"])
                normIndex.append(n.paragraph + " BGB")
                bgb.append(n)
    
    # read norms for stgb
    with open("stgb.json") as stgb_file:
        d = json.load(stgb_file)
        for norm in d["normen"]:
            if "sentencedtext" in norm and "artpara" in norm and "title" in norm:
                n = Norm(norm["artpara"], norm["title"], norm["sentencedtext"])
                normIndex.append(n.paragraph + " StGB")
                stgb.append(n)
    
    y = [4,3,3,1,1,2,1,4,3,3,1,1,1,1,3,2,1,1,3,1,1,1,1,1,4,4,3,2,4,3,1,1,1,2,1,3,3,1,1,2,1,2,4,2,4,1,1,1,4,2,2,1,2,1,1,2,2,1,1,1,2,2,1,1,2,2,2,4,4,1,4,4,1,3,1,1,1,1,1,1,1,2,1,2,3,1,1,4,4,1,1,1,1,4,2,1,1,1,1,2,2,1,2,3,1,3,1,3,1,4,1,1,4,3,1,1,4,1,1,4,4,1,1,1,1,3,1,1,2,4,4,2,1,1,1,2,4,4,2,1,2,1,3,2,1,1,2,1,1,1,1,1,1,1,4,1,4,1]
    featureList = makeFeatures()
    assert(len(y)==len(featureList))
    #print(fitParametersLinear(featureList, y))
    logreg = fitParametersLogistic(featureList, y)
    
         
    return urteilListe, stgb, bgb, normIndex, logreg
    
def searchAndSort(searchstring, urteilListe, norm, logreg):
    stemmer = SnowballStemmer("german")
    searchstring = stemmer.stem(searchstring)
    results = []
    resultsForHumans = []
    featureList = []
    for urteil in urteilListe:
        if norm in urteil.norm:
            for abs in urteil.absaetze:
                absatz = Absatz(abs["num"], abs["text"], abs["textProcessed"])
                if searchstring in absatz.textProcessed:
                    res = dict()
                    ranking_res, features, predictedClass = Rankingnummer(absatz, False, logreg)
                    res["abs"] = absatz.num
                    res["ranking"] = ranking_res
                    res["urteil"] = urteil.__dict__
                    res["features"] = features
                    #res["class"] = int(predictedClass[0])
                    results.append(res)
                    featureList.append(features)
                    for a in urteil.absaetze:
                        if a["num"] == absatz.num:
                            resultsForHumans.append(a["text"])
    resultsSorted = sorted(results, key=lambda x: x["ranking"], reverse=True)
    #return(results, resultsSorted, resultsForHumans)
    return resultsSorted

def getPageranks(urteilListe):
        pagerankPattern = "\d StR \d+/\d+"
        pagerankdict = defaultdict(int)
        for urteil in urteilListe:
            references = re.findall(pagerankPattern, urteil.gruende)
            for ref in references:
                pagerankdict[ref] += 1
        return(pagerankdict)
            

def autoCompleteNormFor(normStart):
    r = []
    for n in normIndex:
        if normStart in n:
            r.append(n)
    return r[0:10]


if __name__ == "__main__":

    reloadUrteile = True
    
    urteilListe, stgb, bgb, normIndex, logreg = setup(reloadUrteile)
    
    
    #for u in urteilListe:
        #print(u.norm)
    '''   
    app = Flask(__name__)
        
    @app.route("/")
        def start(searchstring, norm):
            return searchAndSort(searchstring, urteilListe, norm)
    '''
    #with open("result.txt", "w", encoding="utf-8") as outf:
        #outf.write(str(searchAndSort("Mittäterschaft", urteilListe, "§ 25 Abs 2 StGB")))
    
    """
    trainExamples = [("Mittäter", "§ 25 StGB"), ("unmittelbar", "§ 22 StGB"), ("beendet", "§ 24 StGB"), ("Garant","§ 13 StGB"), ("Hilfeleistung", "§ 27 StGB"), ("bestimmen", "§ 26 StGB"), ("erforderlich", "§ 22 StGB"), ("Wegnahme", "§ 242 StGB"), ("Vermögensschaden", "§ 263 StGB"), ("Vermögensverfügung", "§ 263 StGB"), ("Gewalt", "§ 249 StGB")]
        
    for word, norm in trainExamples:
        results, resultsSorted, resultsForHumans = searchAndSort(word, urteilListe, norm)
        print(len(results))
        makeTrainingData(word, norm, results, resultsForHumans, min(len(results),30))
    """
    
    searchAndSort("beendet", urteilListe, "§ 24 StGB", logreg)
    

