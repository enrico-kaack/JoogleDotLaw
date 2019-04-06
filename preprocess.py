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
    return gensim.utils.simple_preprocess(text)
    
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
    print(newdict)

    with open("SchlagwörterDictStemmed.json", "w") as outf:
        outf.write(str(newdict))
     
    text = """\n      <div>\n         <dl class=\"RspDL\">\n            <dt/>\n            <dd>\n               <h1>A.</h1>\n            </dd>\n         </dl>\n         <dl class=\"RspDL\">\n            <dt>\n               <a name=\"rd_1\">1</a>\n            </dt>\n            <dd>\n               <p>Die Verfassungsbeschwerde betrifft die Zulässigkeit der Auslieferung zum Zwecke der Strafverfolgung an die Republik Türkei wegen Staatsschutzdelikten bei drohender Verurteilung zu einer sogenannten erschwerten lebenslänglichen Freiheitsstrafe.</p>\n            </dd>\n         </dl>\n         <dl class=\"RspDL\">\n            <dt/>\n            <dd>\n               <h2>I.</h2>\n            </dd>\n         </dl>\n         <dl class=\"RspDL\">\n            <dt>\n               <a name=\"rd_2\">2</a>\n            </dt>\n            <dd>\n               <p>Der Beschwerdeführer besitzt die türkische Staatsangehörigkeit. Unter Bezugnahme auf einen Haftbefehl des Schwurgerichts zu D. vom 28. November 2007 ersuchte die türkische Regierung um seine Auslieferung. Ihm wird vorgeworfen, als Gebietsverantwortlicher der Arbeiterpartei Kurdistans (PKK) für die Region E. die Ausführung eines Bombenanschlags auf den Gouverneur von B. am 5. April 1999 durch ein Mitglied der PKK, den T..., beschlossen und angeordnet zu haben. Bei diesem Bombenattentat kamen T... und eine weitere Person ums Leben; weitere 14 Personen, darunter Polizeibeamte, wurden verletzt.</p>\n            </dd>\n         </dl>\n         <dl class=\"RspDL\">\n            <dt>\n               <a name=\"rd_3\">3</a>\n            </dt>\n            <dd>\n               <p>1. Mit Beschluss vom 13. Januar 2009 ordnete das Oberlandesgericht Hamm die förmliche Auslieferungshaft gegen den Beschwerdeführer an. Dieser wurde am 2. April 2009 festgenommen und befindet sich seitdem in Auslieferungshaft. Der Beschluss wurde dem Verfolgten am 2. April 2009 durch den Richter des Amtsgerichts Bochum verkündet.</p>\n            </dd>\n         </dl>\n         <dl class=\"RspDL\">\n            <dt>\n               <a name=\"rd_4\">4</a>\n            </dt>\n            <dd>\n               <p>2. Mit Beschluss vom 2. Juni 2009 erklärte das Oberlandesgericht Hamm die Auslieferung des Verfolgten in die Türkei zum Zwecke der Strafverfolgung wegen der ihm mit Anklage der Oberstaatsanwaltschaft der Republik bei dem staatlichen Sicherheitsgericht zu D. vom 28. November 2007 und dem hierauf gestützten Haftbefehl des Schwurgerichts zu D. vom 28. November 2007 zur Last gelegten Straftaten für zulässig und ordnete die Fortdauer der Auslieferungshaft an. Bedenken gegen das in der Türkei zu erwartende Strafverfahren gegen den Verfolgten ergäben sich nicht. Die türkischen Behörden hätten zugesichert, dass die Rechte und Garantien der Europäischen Menschenrechtskonvention gewahrt würden. Die gemäß Art. 25 GG in der Bundesrepublik Deutschland verbindlichen völkerrechtlichen Mindeststandards sowie die unabdingbaren Grundsätze der deutschen verfassungsrechtlichen Ordnung stünden einer Auslieferung nicht entgegen.</p>\n            </dd>\n         </dl>\n         <dl class=\"RspDL\">\n            <dt>\n               <a name=\"rd_5\">5</a>\n            </dt>\n            <dd>\n               <p>3. Mit Schriftsatz vom 26. Juni 2009 stellte der Beschwerdeführer einen Antrag nach § 33 Abs. 1 IRG und verband damit die Anhörungsrüge. Er rügte unter anderem mit näheren Ausführungen die Verletzung rechtlichen Gehörs dadurch, dass ihm das Oberlandesgericht Hamm den Antrag der Generalstaatsanwaltschaft vom 19. Mai 2009 vor seiner Entscheidung nicht zur Kenntnis gebracht habe, in dem diese beantragt hatte, die Auslieferung des Verfolgten in die Türkei für zulässig zu erklären.</p>\n            </dd>\n         </dl>\n         <dl class=\"RspDL\">\n            <dt>\n               <a name=\"rd_6\">6</a>\n            </dt>\n            <dd>\n               <p>4. Mit Beschluss vom 24. August 2009 wies das Oberlandesgericht Hamm einen Antrag des Beschwerdeführers, den Vorsitzenden Richter am Oberlandesgericht R... wegen Besorgnis der Befangenheit abzulehnen, als unbegründet zurück.</p>\n            </dd>\n         </dl>\n         <dl class=\"RspDL\">\n            <dt>\n               <a name=\"rd_7\">7</a>\n            </dt>\n            <dd>\n               <p>5. Mit Beschluss vom 17. September 2009 wies das Oberlandesgericht Hamm die Anhörungsrüge sowie die Einwendungen des Verfolgten gegen die Zulässigkeit der Auslieferung zurück. Aus der fehlenden Übersendung der Antragsschrift der Generalstaatsanwaltschaft vom 19. Mai 2009 zur Kenntnisnahme und eventuellen Stellungnahme ergebe sich keine Gehörsverletzung. Der Verfolgte habe im Rahmen seiner mündlichen Anhörung vor dem Amtsgericht Bochum am 29. April 2009 Gelegenheit zur Stellungnahme und damit hinreichend rechtliches Gehör gehabt. Überdies sei es, so das Oberlandesgericht Hamm wörtlich: \"im Auslieferungsverfahren - wie in jedem anderen Haftbefehlsverfahren - nicht vorgesehen, dass den Verfolgten die jeweiligen Antragsschriften der Generalstaatsanwaltschaft vor der Beschlussfassung durch den Senat zur Kenntnisnahme und eventuellen Stellungnahme übermittelt werden\".</p>\n            </dd>\n         </dl>\n         <dl class=\"RspDL\">\n            <dt>\n               <a name=\"rd_8\">8</a>\n            </dt>\n            <dd>\n               <p>Der von dem Verfolgten erhobene Einwand, ihm drohe im Falle seiner Verurteilung eine sogenannte erschwerte lebenslange Freiheitsstrafe bis zum Tod, ohne dass die Möglichkeit einer bedingten Strafaussetzung beziehungsweise vorzeitigen Entlassung aus dem Strafvollzug bestünde, greife nicht durch. Die Auslieferung verstoße nicht gegen unabdingbare Grundsätze der deutschen verfassungsrechtlichen Ordnung. Nach der Auskunft des Bundesamtes für Justiz vom 30. Juni 2009 habe die Botschaft der Republik Türkei mitgeteilt, dass nach Art. 104 der türkischen Verfassung der Präsident der Republik als Oberhaupt des Staates das Gnadenrecht ausübe und Strafen aus Gründen dauernder Krankheit, Behinderung und altersbedingt mindern oder erlassen könne."""
    #print(run_complete_pipeline(text))