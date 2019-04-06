import json
import os
import inspect
import re
from bs4 import BeautifulSoup
from preprocess import run_complete_pipeline

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
            self.norm = dic["norm"]
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
            if "sentencedtext" in norm and "artara" in norm:
                n = Norm(d["artpara"], d["title"], d["sentencedtext"])
                bgb.append(norm)
    
    # read norms for stgb
    with open("stgb.json") as stgb_file:
        d = json.load(stgb_file)
        for norm in d["normen"]:
            if "sentencedtext" in norm and "artara" in norm:
                n = Norm(d["artpara"], d["title"], d["sentencedtext"])
                stgb.append(norm)
                
    return urteilListe, stgb, bgb
    
def searchAndSort(searchstring, urteilListe, norm):
    results = []
    for urteil in UrteilListe:
        if norm in urteil.norm:
            for abs in urteil.absaetze:
                absatz = Absatz(abs["num"], abs["text"], abs["textProcessed"])
                if einzelwortsuche(searchstring, absatz.textProcessed) > 0:
                    ranking_res = ranking(absatz)
                    results.append((urteil.doknr, absatz.num, ranking_res)) 
    results = sorted(results, key=lambda x: x[2])
    return(results)
        

if __name__ == "__main__":

    reloadUrteile = False
    
    urteilListe, stgb, bgb = setup(reloadUrteile)
    
    for u in urteilListe:
        print(u.norm)

    print(searchAndSort(searchstring, urteilListe, norm))
