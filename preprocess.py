from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
import gensim
import re
import json

def stem(tokens):
    stemmer = SnowballStemmer("german", ignore_stopwords=True)
    stemmed_doc = [stemmer.stem(token) for token in tokens]
    return stemmed_doc
               
def tokenize_strip(text):
    """
    remove punctuation, lowercase, tokenize
    """   
    return gensim.utils.simple_preprocess(text, max_len=50)
    
def remove_html(text):
    return re.sub("<[^>]+>", "", text) 

        
def remove_stopwords(tokens):
    return [token for token in tokens if token not in stopwords.words("german")]
    
def run_complete_pipeline(text):
    return remove_stopwords(stem(tokenize_strip(remove_html(text))))
    
        
if __name__ == "__main__":

    d = {"lässt außer Acht":0.5,
"es kommt nicht darauf an":0.5,
"Rechtsprechung":1,
"Urteil":1,
"BGH":1,
"BVerfG":1,
"Beschluss":1,
"OLG":1,
"Reichsgericht":1,
"Bundesgerichtshof":1,
"Senat":1,
"Bundesverfassungsgericht":1,
"Oberlandesgericht":1,
"Zweck":1,
"ständige Rechtsprechung":2.5,
"Auslegung":1.5,
"auslegen":1.5,
"Auffassung":1.5,
"Schriftum":1.5,
"rechtsfehler":1.5,
"Ansicht":1.5,
"Rechtsauffassung":1.5,
"definieren":1.5,
"Definition":1.5,
"Wortlaut":1.5,
"Systematik":1.5,
"Telos":1.5,
"Teleologie":1.5,
"teleologisch":1.5,
"systematisch":1.5,
"historisch":1.5,
"Gesetzgeber":1.5,
"gesetzgeberisch":1.5,
"Begriff":1.5,
"begrifflich":1.5,
"Sprachgebrauch":1.5,
"Sinn und Zweck":1.5,
"Sprachsinn":1.5,
"Wissenschaft":1.5,
"umstritten":1.5,
"kontrovers":1.5,
"Entstehungsgeschichte":1.5,
"Schutzzweck":1.5,
"st. Rspr.":2.5,
"Normzweck":1.5,
"Teil der Literatur":1.5,
"gefestigte Rechtsprechung":2.5,
"stRspr":2.5,
"ständ. Rspr.":2.5}
    newdict = dict()
    for key, value in d.items():
        newdict[stem([key])[0]] = value
    #print(newdict)

    #with open("SchlagwörterDictStemmed.json", "w") as outf:
        #outf.write(str(newdict))
     
    text = """Aufgrund der Täuschung sei es bei den mit der Retaxationsprüfung betrauten Mitarbeitern der Krankenkassen zu einem Irrtum über den Erstattungsanspruch des Angeklagten gekommen. Wäre ihnen die Verwendung tatsächlich nicht zugelassener und damit nicht abrechnungsfähiger Ware bekannt gewesen, so wäre eine Retaxation jeweils auf Null erfolgt. Durch die in diesem Unterlassen zu sehende Vermögensverfügung sei den Krankenkassen ein Vermögensschaden in Höhe der jeweiligen Rezeptbeträge abzüglich (aus sonstigen Gründen) erfolgter Retaxationen und einbehaltener Beträge entstanden."""
    #print(run_complete_pipeline(text))
    text = remove_html(text)
    print(text)
    text = tokenize_strip(text)
    print(text)
    text = stem(text)
    print(text)
    text = remove_stopwords(text)
    print(text)
    