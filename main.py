import json

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
        self.entscheidungsgruende = dic["entscheidungsgruende"]
        self.gruende = dic["gruende"]
        self.abweichendeMeinung = dic["abwmeinung"]
        self.sonstlt = dic["sonstlt"]
        self.identifier = dic["identifier"]
        self.coverage = dic["coverage"]
        self.language = dic["language"]
        self.publisher = dic["publisher"]
        self.accessRights = dic["accessRights"]

    

with open("Str/JURE100055074.json") as json_file:
    d = json.load(json_file)
    u = Urteil(d)
    print(u)


