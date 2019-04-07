import re

def einzelwortsuche(Liste, Schlagwort):
    Anzahl = 0
    for i in range(len(Liste)-1):
        if (Liste[i]+" "+Liste[i+1]) == Schlagwort:
            Anzahl += 1
    return Anzahl

#Zählt die Anzahl der Schlagwörter im Urteilstext
def woertersuche(Liste):
    Schlagwortdict = {
        'entstehungsgeschicht': 1.5, 
        'systemat': 1.5, 
        'rechtsfehl': 1.5, 
        'wissenschaft': 1.5, 
        'standige rechtsprech': 10, 
        'definition': 1.5, 
        'bundesgerichtshof': 1, 
        'kontrov': 1.5, 
        'beschluss': 1, 
        'begriff': 1.5, 
        'schriftum': 1.5, 
        'normzweck': 1.5, 
        'histor': 1.5, 
        'olg': 1, 
        'oberlandesgericht': 1, 
        'gesetzgeber': 1.5, 
        'wortlaut': 1.5, 
        'bgh': 1, 
        'bundesverfassungsgericht': 1, 
        'zweck': 1, 'bverfg': 1, 
        'rechtsauffass': 1.5, 
        'reichsgericht': 1, 
        'stand rspr': 10, 
        'kommt nicht darauf an': 0.5, 
        'gefestigt rechtsprech': 2.5, 
        'defini': 1.5, 
        'teleolog': 1.5, 
        'teil literatur': 1.5, 
        'gesetzgeb': 1.5, 
        'auffass': 1.5, 
        'rechtsprech': 1, 
        'ausleg': 1.5, 
        'umstritt': 1.5, 
        'lasst auss acht': 0.5, 
        'schutzzweck': 1.5, 
        'telos': 1.5, 
        'ansicht': 1.5, 
        'teleologi': 1.5, 
        'strspr': 10, 
        'sprachgebrauch': 1.5,
        'senat': 1, 
        'sprachsinn': 1.5, 
        'st rspr': 10, 
        'sinn zweck': 1.5,
        'urteil': 1
    }
    Ergebnis = 0
    for key in Schlagwortdict:
        #ursprünglicher Wichtigkeitswert wird mit Häufigkeit des Wortes multipliziert
        Ergebnis += Schlagwortdict[key] * einzelwortsuche(Liste, key) 
    return Ergebnis

#Zählt die Anzahl der Zitate in einem gesamten Urteilstext
def Klammerauswertung(Text):  
    position_auf = 0 #Position "("
    position_zu = 0 #Position ")"
    Kategorie1 = 0
    Kategorie2 = 0
    Kategorie3 = 0

    Kat1 = "EuGH|BGH|BVerfG|OLG|RG|BGHZ|BGHSt|BeckRS|Urteil|Urt\.|Urt|Beschluss|StR"
    Kat2 = "(Aufl\.|Aufl|kommentar|((§|§§|Art\.|Art)[^\)]{0,10}(Rn|Rn\.|Rdnr|Rdnr\.))|([A-Z][a-zäöüß]+([ |\],[a-zA-Zäöüß]{2,7}) [0-9]{3,4}\, [0-9]{1,4}))"
    Kat3 = "BT-Drucksache|BT-Drucks\.|BT\-Drucks|BTDrucks"

    # 1. Klammerausdrücke finden
    while -1 != position_auf:
        position_auf = Text.find("(", position_auf+1)
        position_zu = Text.find(")", position_auf) #position_zu+1
        position_semicolon = position_auf
        #Position Semicolons bestimmen
        while -1 != position_semicolon:
            position_semicolon_alt = position_semicolon
            position_semicolon = Text.find(";", position_semicolon +1 , position_zu)
            #Audruck zwischen zwei Semicolons nach Relulären Ausdrücken checken
            if position_semicolon == -1:
                if re.search(Kat1, Text[position_semicolon_alt +1 : position_zu +1]):
                    Kategorie1 += 1
                    #print(Text[position_semicolon_alt +1 : position_zu +1])
                elif re.search(Kat2, Text[position_semicolon_alt +1 : position_zu +1]):
                    Kategorie2 += 1
                    #print(Text[position_semicolon_alt +1 : position_zu +1])
                elif re.search(Kat3, Text[position_semicolon_alt +1 : position_zu +1]):
                    Kategorie3 += 1
                    #print(Text[position_semicolon_alt +1 : position_zu +1])

            else: 
                if re.search(Kat1, Text[position_semicolon_alt +1 : position_semicolon + 1]):
                    Kategorie1 += 1
                    #print(Text[position_semicolon_alt +1 : position_semicolon + 1])
                elif re.search(Kat2, Text[position_semicolon_alt +1 : position_semicolon + 1]):
                    Kategorie2 += 1
                    #print(Text[position_semicolon_alt +1 : position_semicolon + 1])
                elif re.search(Kat3, Text[position_semicolon_alt +1 : position_semicolon + 1]):
                    Kategorie3 += 1
                    #print(Text[position_semicolon_alt +1 : position_semicolon + 1])
                
    Result = [Kategorie1, Kategorie2, Kategorie3]
    return Result

def Rankingnummer(Absatzobjekt, use_logreg=False, reg=None):

        
    ############################################
    #Gewichtugnsfaktor für Schlagwort-Faktor
    c=20.5968
    #Gewichtungsfaktor für Zitate (alle 3 Kategorien)
    d=1
    #Gewichtungen für Kategorien:
    #Kategorie 1:
    e = 0.045
    #Kategorie 2:
    f =-0.3099
    #Kategorie 3:
    g = 0.62478
    #############################################
    
    #Schlagwörter werden durch die Länge des Textes geteilt
    Auswertung_Schlagwoerter = (woertersuche(Absatzobjekt.textProcessed)) * c / len(Absatzobjekt.text)
    #Ergebnis der Zitate: Liste mit Ergebnis in allen drei Kategorien
    Auswertung_Zitate = (Klammerauswertung(Absatzobjekt.text))  #mit String!
    
    predicted_class = None
    if use_logreg:
        X_pred = [[Auswertung_Schlagwoerter]+Auswertung_Zitate]
        predicted_class = reg.predict(X_pred)

    
    Auswertung_Zitate[0] = Auswertung_Zitate[0] * e * d
    Auswertung_Zitate[1] = Auswertung_Zitate[1] * f * d
    Auswertung_Zitate[2] = Auswertung_Zitate[2] * g * d

    features = [Auswertung_Schlagwoerter] + Auswertung_Zitate
    return (Auswertung_Schlagwoerter + sum(Auswertung_Zitate), features, predicted_class)

if __name__=="__main__":
    Text = "b) Zwar entstehungsgeschicht ist es nicht erforderlich, dass der Täter der Einfuhr das Rauschgift eigenhändig ins Inland verbringt. Vielmehr kann auch derjenige, der die Betäubungsmittel nicht selbst nach Deutschland transportiert, (Mit-)Täter der Einfuhr des unmittelbar handelnden Täters sein, wenn er einen Tatbeitrag erbringt, der sich bei wertender Betrachtung nicht nur als Förderung fremden Tuns, sondern als Teil der zur Tatbestandsverwirklichung führenden Tätigkeit aller Mitwirkenden darstellt, und der die Tathandlungen der anderen als Ergänzung seines eigenen Tatanteils erscheinen lässt (st. Rspr.; vgl. BGH, Urteil vom 22. Juli 1992 - 3 StR 35/92, BGHSt 38, 315, 319 mwN). Wesentliche Anhaltspunkte für die Täterschaft sind dabei der Grad seines Tatinteresses, der Umfang der Tatbeteiligung, die Tatherrschaft und der Wille dazu, die in eine wertende Gesamtbetrachtung einzubeziehen sind (st. Rspr.; BGH, Beschluss vom 11. Juli 1991 - 1 StR 357/91, BGHSt 38, 32, 33 mwN). Auch der im Inland aufhältige Empfänger von Betäubungsmitteln aus dem Ausland kann deshalb wegen täterschaftlicher Einfuhr von Betäubungsmitteln strafbar sein, wenn er sie durch Dritte über die Grenze bringen lässt und dabei mit Täterwillen die Tatbestandsverwirklichung fördernde Beiträge leistet. Hat der Empfänger hingegen keinen Einfluss auf den Einfuhrvorgang und wartet er nur darauf, dass der Lieferant ihm die eingeführten Betäubungsmittel bringt, kann er sich zwar etwa wegen einer Bestellung des Rauschgifts wegen Handeltreibens mit Betäubungsmitteln strafbar machen; die bloße Bereitschaft zur Entgegennahme der eingeführten Betäubungsmittel begründet aber weder die Stellung als Mittäter noch als Gehilfe der Einfuhr (Körner/Patzak/Volkmer, BtMG, 8. Aufl., § 29 Teil 5 Rn. 167 mwN). a) Mittäter ist, wer nicht nur fremdes Tun fördert, sondern einen eigenen Tatbeitrag derart in eine gemeinschaftliche Tat einfügt, dass sein Beitrag als Teil der Tätigkeit des anderen und umgekehrt dessen Tun als Ergänzung seines eigenen Tatanteils erscheint. Ob ein Beteiligter ein so enges Verhältnis zur Tat hat, ist nach den gesamten Umständen, die von seiner Vorstellung umfasst sind, in wertender Betrachtung zu beurteilen. Wesentliche Anhaltspunkte können der Grad des eigenen Interesses am Taterfolg, der Umfang der Tatbeteiligung und die Tatherrschaft oder wenigstens der Wille zur Tatherrschaft sein (st. Rspr.; vgl. nur BGH, Urteile vom 15. Januar 1991 – 5 StR 492/90, BGHSt 37, 289, 291; vom 9. April 2013 – 1 StR 586/12, BGHSt 58, 218, 225 f.; vom 13. Juli 2016 – 1 StR 94/16, Rn. 17). Bei Beteiligung mehrerer Personen, von denen nicht jede sämtliche Tatbestandsmerkmale verwirklicht, ist Mittäter, wer seinen eigenen Tatbeitrag so in die Tat einfügt, dass er als Teil der Handlung eines anderen Beteiligten und umgekehrt dessen Handeln als Ergänzung des eigenen Tatanteils erscheint. Stets muss sich diese Mitwirkung aber nach der Willensrichtung des sich Beteiligenden als Teil der Tätigkeit aller darstellen (st. Rspr.; vgl. BGH, Beschluss vom 29. September 2015 – 3 StR 336/15, NStZ-RR 2016, 6)."
    d=1
    e = 0.045
    f =-0.3099
    g = 0.62478
    Auswertung_Zitate = (Klammerauswertung(Text))  #mit String!
    Auswertung_Zitate[0] = Auswertung_Zitate[0] * e * d
    Auswertung_Zitate[1] = Auswertung_Zitate[1] * f * d
    Auswertung_Zitate[2] = Auswertung_Zitate[2] * g * d
    print("Auswertung Zitate: ")
    print(Auswertung_Zitate)

