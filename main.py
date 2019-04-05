import json
import os

class Urteil:
    def __init__(self, dic):
        self.doknr = dic["doknr"]
        self.ecli = dic["ecli"]
        self.gertyp = dic["gertyp"]
        self.gerort = dic["gerort"]
        self.spruchkoerper = dic["spruchkoerper"]
        self.entschDatum = dic["entsch-datum"]
        self.aktenzeichen = dic["aktenzeichen"]
        self.doktyp = dic["doktyp"]
        self.norm = dic["norm"]
        self.vorinstanz = dic["vorinstanz"]
        self.regionAbk = dic["region"]["abk"]
        self.regionLong = dic["region"]["long"]
        self.mitwirkung = dic["mitwirkung"]
        self.titel = dic["titelzeile"]
        self.leitsatz = dic["leitsatz"]
        self.tenor = dic["tenor"]
        self.tatbestand = dic["tatbestand"]
        if (len(dic["entscheidungsgruende"]) > 0):
            self.gruende = dic["entscheidungsgruende"]
        else:
            self.gruende = dic["gruende"]
        self.abweichendeMeinung = dic["abwmeinung"]
        self.sonstlt = dic["sonstlt"]
        self.identifier = dic["identifier"]
        self.coverage = dic["coverage"]
        self.language = dic["language"]
        self.publisher = dic["publisher"]
        self.accessRights = dic["accessRights"]

class Norm:
    def __init__(self, paragraph, title, text):
        self.paragraph = paragraph
        self.title = title
        self.text = text

    def isTextInNorm(self, searchText):
        pass


urteilListe = []
bgb = []
stgb = []

def setup():
    # read all urteile
    for filename in os.listdir("StR"):
        with open(os.path.join("StR/",filename)) as json_file:
            d = json.load(json_file)
            u = Urteil(d)
            urteilListe.append(u)

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

if __name__ == "__main__":
    setup()



