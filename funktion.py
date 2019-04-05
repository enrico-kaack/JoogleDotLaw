# Funktion, die ein Urteil (Suchergebnis) nach vordefinierten Schlagwörtern durchsucht
# und so deren Wichtigkeit beurteilt
def woertersuche (Text, Schlagwortliste):
    ergebnismap = {}

    #Iterieren über Schlagwortliste
    for i in range(len(Schlagwortliste)):
        Paar = (Schlagwortliste[i] : einzelwortsuche(Text, Schlagwortliste[i]))
        ergebnismap.update(Paar)
    
    return ergebnismap

def einzelwortsuche (Text, Schlagwort):
    j = -1 #da while Schleife immer mind. einmal durchlaufen wird
    position = 0
    ende = len(Text)
    while position != -1
        position = Text.find(Schlagwort[,position[,ende]])  
        j += 1
    return j