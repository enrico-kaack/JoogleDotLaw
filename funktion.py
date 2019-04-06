def einzelwortsuche(Text, Schlagwort):
    Anzahl = -1 #da while Schleife immer mind. einmal durchlaufen wird
    position = 0
    #ende = len(Text)
    while -1 != position:
        position = Text.find(Schlagwort, position+1)  
        Anzahl += 1
    return Anzahl

# Funktion, die ein Urteil (Suchergebnis) nach vordefinierten Schlagwörtern durchsucht
# und so deren Wichtigkeit beurteilt
def woertersuche(Text, Schlagwortliste): #Text ist string, Schlagwortliste ist Dictionary
    for key in Schlagwortliste:
        #ursprünglicher Wichtigkeitswert wird mit Häufigkeit des Wortes multipliziert
        Schlagwortliste[key] = Schlagwortliste[key] * einzelwortsuche(Text, key) 
    return Schlagwortliste

def main():
    Text = "hallo ich heisse Lukas und komme aus Heidelberg und der Hackathon ist in Heidelberg"
    Schlagwortliste = {"Lukas" : 1, "Heidelberg" : 1.5, "und" : 0.5}
    Ergebnisliste = woertersuche(Text, Schlagwortliste)
    print(Ergebnisliste)

main()