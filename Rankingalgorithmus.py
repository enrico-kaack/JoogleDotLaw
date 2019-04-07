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
        position_zu = Text.find(")", position_zu+1)
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

def Rankingnummer(Absatzobjekt):
    #Gewichtugnsfaktor für Schlagwort-Faktor
    c=1000
    #Gewichtungsfaktor für Zitat-Klammer-Faktor
    d=1
    
    #Schlagwörter werden durch die Länge des Textes geteilt
    Auswertung_Schlagwoerter = (woertersuche(Absatzobjekt.textProcessed)) / len(Absatzobjekt.text) * c
    #Ergebnis der Zitate: Liste mit Ergebnis in allen drei Kategorien
    Auswertung_Zitate = (Klammerauswertung(Absatzobjekt.text)) * d  #mit String!
    features = [Auswertung_Schlagwoerter] + Auswertung_Zitate
    return (Auswertung_Schlagwoerter + sum(Auswertung_Zitate), features)

if __name__=="__main__":
    Text4 = "Wird von dem Angegriffenen in einer Notwehrlage ein Gegenangriff auf Rechtsgüter der Angreifer geführt (sog. Trutzwehr), kann darin nur dann eine Angriffsabwehr gesehen werden, wenn in diesem Vorgehen auch tatsächlich der Wille zum Ausdruck kommt, der drohenden Rechtsverletzung entgegenzutreten (BGH, Urteil vom 2. Oktober 1953 – 3 StR 151/53, BGHSt 5, 245, 247; Urteil vom 19. März 1968 – 1 StR 648/67, MDR 1969, 15, 16 bei Dallinger; Fischer, StGB, 60. Aufl., § 32 Rn. 25; Schmidhäuser, GA 1991, 91, 132; ders., JZ 1991, 937, 939; Schuenemann, GA 1985, 341, 371; Welzel, Das deutsche Strafrecht, 11. Aufl., S. 86; vgl. Alwart, GA 1983, 433, 448 ff.). Dazu reicht allein die Feststellung, dass dem Angegriffenen die Notwehrlage bekannt war, nicht aus. Die subjektiven Voraussetzungen der Notwehr sind erst dann erfüllt, wenn der Gegenangriff zumindest auch zu dem Zweck geführt wurde, den vorangehenden Angriff abzuwehren. Dabei ist ein Verteidigungswille auch dann noch als relevantes Handlungsmotiv anzuerkennen, wenn andere Beweggründe (Vergeltung für frühere Angriffe, Feindschaft etc.) hinzutreten. Erst wenn diese anderen Beweggründe so dominant sind, dass hinter ihnen der Wille das Recht zu wahren ganz in den Hintergrund tritt, kann von einem Abwehrverhalten keine Rede mehr sein (vgl. BGH, Urteil vom 9. November 2011 – 5 StR 328/11, NStZ-RR 2012, 84, 86; Urteil vom 31. Januar 2007 – 1 StR 429/06, NStZ 2007, 325, 326; Urteil vom 12. Februar 2003 – 1 StR 403/02; NJW 2003, 1955, 1957 f.; Beschluss vom 8. März 2000 – 3 StR 67/00, NStZ 2000, 365, 366; Beschluss vom 23. August 1991 – 2 StR 360/91, BGHR StGB § 32 Abs. 2 Verteidigungswille 1; Beschluss vom 5. November 1982 – 3 StR 375/82, NStZ 1983, 117; Urteil vom 4. September 1979 – 5 StR 461/79) (BGH GA 1980, 67, 68; Urteil vom 1. Juli 1952 – 1 StR 119/52, BGHSt 3, 194, 198). Hieran ist trotz in der Literatur geäußerter Kritik (vgl. LK/Rönnau/Hohn, StGB, 12. Aufl., § 32 Rn. 266; Matt/Renzikowski/Engländer, StGB, § 32 Rn. 63; MünchKommStGB/Erb, 2. Aufl., § 32 Rn. 241; Perron in Schönke/Schröder, StGB, 28. Aufl., § 32 Rn. 63) (Prittwitz, GA 1980, 381 ff.; Rath, Das subjektive Rechtfertigungselement, 2002, S. 241 f.; Waider, Die Bedeutung der Lehre von den subjektiven Rechtfertigungselementen für Methodologie und Systematik des Strafrechts, 1970, S. 91 ff.) festzuhalten. Andere gesundheitsschädliche Stoffe im Sinne des § 224 Abs. 1 Nr. 1 StGB sind Substanzen, die nach ihrer Art und dem konkreten Einsatz zu einer erheblichen Gesundheitsbeschädigung geeignet sind (vgl. BGH, Urteil vom 16. März 2006 – 4 StR 536/05, BGHSt 51, 18, 22). Ob die Wirkung dabei mechanisch, biologisch, chemisch oder thermisch erfolgt, ist ohne Belang (vgl. Hardtung in: MünchKomm.z.StGB, 3. Aufl., § 224 Rn. 6; Stree/Sternberg-Lieben in: Schönke-Schröder, StGB, 29. Aufl., § 224 Rn. 2c; Fischer, StGB, 65. Aufl., § 224 Rn. 5; Rengier, Strafrecht, Besonderer Teil II, 17. Aufl., § 14 Rn. 9; Hilgendorf, ZStW 112, 811, 828 mwN). Der gesundheitsschädliche Stoff ist dem Opfer beigebracht, wenn er durch den Täter so mit dem Körper in Verbindung gebracht worden ist, dass er seine gesundheitsschädliche Wirkung entfalten kann. Dafür kann ein äußerlicher Kontakt ausreichend sein, sofern die Schwere der möglichen Auswirkung auf die Gesundheit der Gefährdung durch einen eingeführten Stoff gleichkommt (vgl. BGH, Urteil vom 21. Oktober 1983 – 2 StR 289/83, BGHSt 32, 130, 132 f.; Urteil vom 30. Juni 1976 – 3 StR 469/75, NJW 1976, 1851; Urteil vom 12. August 1960 – 4 StR 294/60, BGHSt 15, 113, 115 [jeweils zu § 229 StGB aF]; OLG Zweibrücken, Beschluss vom 23. Februar 2012 – 1 Ss 90/11, NStZ-RR 2012, 371, 372 [Ls]; OLG Dresden, Beschluss vom 29. Juni 2009 – 2 Ss 288/09, NStZ-RR 2009, 337, 338; Engländer in: Matt/Renzikowski, StGB, § 224 Rn. 4; Stree/Sternberg-Lieben in: Schönke-Schröder, StGB, 29. Aufl., § 224 Rn. 2d; Hardtung in: MünchKomm.z.StGB, 3. Aufl., § 224 Rn. 10 f. mwN)."
    Text5 = "Das Landgericht hat insoweit lediglich ausgeführt, dass dem Adhäsionskläger wegen des Aktienkaufs, der Gegenstand der Verurteilung im Fall II.6. der Urteilsgründe ist, aus §§ 823 Abs. 2 BGB, 263 Abs. 1 und Abs. 3 Nr. 1 und 2 StGB ein Schadensersatzanspruch in Höhe von 269.844 USD zustehe. Dabei hat es nicht erkennbar bedacht, dass es sich bei Schadensersatzansprüchen regelmäßig um Geldwertschulden handelt, die grundsätzlich in inländischer Währung entstehen, soweit sie sich - wie hier - aus deutschem Recht ergeben. Ein in ausländischer Währung ermittelter Erstattungsbetrag bildet nur einen Berechnungsfaktor für die in Euro festzusetzende Anspruchshöhe (vgl. BGH, Urteil vom 19. Februar 1998 - I ZR 233/95, NJW-RR 1998, 1426, 1429; Palandt/Grüneberg, BGB, 74. Aufl., § 245 Rn. 16 f., jeweils mwN). Dies gilt hier, zumal ausweislich der Feststellungen zwei Teilzahlungen auf den Kaufpreis bar und in Euro erfolgt sind. 5 Hinzu tritt, dass sich das Landgericht in der Begründung der Adhäsionsentscheidung nicht mit dem Verteidigungsvorbringen des Angeklagten    C.    im Schriftsatz seiner Verteidigerin vom 19. Dezember 2013 auseinandergesetzt hat, das der Senat im Rahmen der Prüfung der Zulässigkeitsvoraussetzung des § 404 Abs. 1 Satz 3 StPO von Amts wegen zur Kenntnis zu nehmen hatte (vgl. hierzu etwa Senat, Beschluss vom 30. Mai 2012 - 2 StR 98/12, insoweit in StV 2013, 563 nicht abgedruckt). Auch wenn die Begründung der Adhäsionsentscheidung nicht unmittelbar an den zivilprozessualen Vorschriften zu messen ist, so muss gleichwohl für das Revisionsgericht nachvollziehbar dargelegt werden, weshalb der Anspruch begründet ist (vgl. LR/Hilger, StPO, 26. Aufl., § 406 Rn. 4; Meier/Dürre, JZ 2006, 18, 22). Dazu gehört eine Auseinandersetzung mit Verteidigungsvorbringen, wenn und soweit dieses nicht von vornherein als völlig ungeeignet erscheint (vgl. auch BGH, Beschluss vom 21. Dezember 1962 - I ZB 27/62, BGHZ 39, 333, 337 ff.). An der gebotenen Auseinandersetzung hiermit fehlt es. Das Landgericht hätte sich mit der vom Angeklagten    C.    erhobenen Verjährungseinrede, der nicht von vornherein jegliche Erheblichkeit abgesprochen werden kann, auseinander setzen müssen. 6 Eine Zurückverweisung der Sache zur neuen Verhandlung allein über den Adhäsionsanspruch kommt nicht in Betracht (vgl. nur Senat, Beschluss vom 7. Juli 2010 - 2 StR 100/10, NStZ-RR 2010, 344 mwN). Von einer Entscheidung war deshalb abzusehen.7 2. Die Entscheidung über die Kosten und Auslagen beruht auf § 473 Abs. 1 Satz 1, § 472a Abs. 2 StPO."
    print(Klammerauswertung(Text4))
    print(Klammerauswertung(Text5))

