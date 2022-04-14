#parser di file .sfs 
#TO-DO rinominare in modo più sensato le variabili
#TO-DO funzione che ritorni le sfs con medesima lunghezza
'''
- riunire per read
- creare una stringa unica per read con ovearlap
- funzione che verifichi la similarita
'''
#dichiarazione costanti
ID = 0
SFS = 1
POSITION = 2
LENGTH = 3

#funzione che stampa tutte le sfs tra due posizioni
def inTheMeaddle(lista, a, b):
    ris = []
    allPosition = get(lista, POSITION)
    for cont in range(0, len(lista)):
        if int(allPosition[cont]) >= a and int(allPosition[cont]) <= b:
            ris.append(lista[cont])
    return ris

#funzione che stampa lunghezza e posizione data una specifica SFS
def getFromSFS(lista, sfs):
    allSFS = get(lista, SFS)
    for cont in range(0, len(allSFS)):
        if allSFS[cont] == sfs:
            return lista[cont][1], lista[cont][2]

def menu():
    print("1. Stampa tutte le SFS")
    print("2. Stampa tutte le posizioni")
    print("3. Stampa tutte le lunghezze")
    print("4. Stampa tutte gli id")
    print("5. Stampa posizione e lunghezza di una specifica sfs")
    print("6. Stampa SFS fra due posizioni")
    print("7. Stampa le read raggruppate")
    scelta = int(input("Inserisci la scelta "))
    return scelta

#funzione che permette di ritornare cio che si vuole
#sfs, posizione o lunghezza
#fare una funzione per ognuna di essa creava ripetizione inutile di codice
def get(lista, x):
    ris = []
    for l in lista:
        ris.append(l[x])
        print(l[x])
    return ris

#ogni funzione restituisce una lista
#per far si che sia una stampa più compresibile 
#faccio un ciclo, per non ripetere codice ho creato questa funzione
def printList(lista):
    for l in lista:
        print(l)
def getRead(lista):
    ris = []
    app = []
    id = lista[0][0]
    for read in lista:
        if read[0] == id:
            app.append(read)
        else:
            id = read[0]
            ris.append(app)
            app = []
    return ris
#rimozione dell'asterisco 
def sostitutionAst(lista):
    idRead = "" 
    for read in lista:
        if not read[0] == "*":
            idRead = read[0]
        else:
            read[0] = idRead
    return lista
def mergeRead(lista):
    
    for read in lista:
        sfs = [read[0][POSITION], read[0][LENGTH]]
        for cont in range(1, len(read)):
            if int(read[cont][POSITION]) + int(read[cont][LENGTH]) > int(sfs[0]):
                #sfs = []
                print("entro")
                #sfs.append(read[cont][POSITION])
                #sfs.append(int(read[cont+1][POSITION])+int(read[cont+1][LENGTH])-int(read[cont][POSITION]))
                posizione = int(sfs[0])
                sfs[0] = read[cont][POSITION]
                sfs[1] = posizione + int(sfs[1]) - int(read[cont][POSITION])
    print(sfs)
            
        
            

        
def formatting(lista):
    app = []
    ris = []
    for l in lista:
        app = l.split()
        ris.append(app)
        #print(app)
    ris = sostitutionAst(ris)
    return ris   
 



lista = []
file = open("solution_batch_0.sfs", 'r')
for single in file:
    lista.append(single)

#rimuovo la stringa iniziale 
#lista[0] = lista[0][36:]

#creo una lista(ogni riga) di lista(ogni campo della riga) 
#lis = formatting(lista[:10]) utile per debug
#invece di avere tutte le righe, così è più capibile 
lis = formatting(lista)
#m54329U_190615_010947/134415974/ccs
#m54329U_190617_231905/26280060/ccs

scelta = menu()

#personalmente userei uno switch ma è presente solo
#nella versione 3.10 di python e non so se si può usare
#quindi ora inserisci un semplice if

while(scelta != 8):
    if scelta == 1:
        #stampo tutte le sfs
        sfs = get(lis, SFS)
        printList(sfs)
    if scelta == 2:
        #stampo tutte le posizioni
        sfs = get(lis, POSITION)
        printList(sfs)
    if scelta == 3:
        #stampo tutte le lunghezze
        sfs = get(lis, LENGTH)
        printList(sfs)
    if scelta == 4:
        #stampo tutti gli id
        sfs = get(lis, ID)
        printList(sfs)
    if scelta == 5:
        #stampo posizione e lunghezza da una specifica sfs
        sfsUtente = input("Inserisci la sfs di cui vuoi posizione e lunghezza: ")

        #converto in upper case in caso l'utente abbia inserito i caratteri in minuscolo
        sfsUtente = sfsUtente.upper()
        
        posizione, lunghezza = getFromSFS(lis, sfsUtente)
        print("la posizione della sfs inserita è: " + posizione)
        print("La lunghezza della sfs inserita è: " + lunghezza)
    if scelta == 6:
        #inserimento del range di posizione
        a = int(input("Inserisci la posizione minima compresa: "))
        b = int(input("Inserisci la posizione massima compresa: "))

        sfs = inTheMeaddle(lis, a, b)
        printList(sfs)
    if scelta == 7:
        #lista di liste in cui ho ogni posizione una read contentente tutte le sequence
        read = getRead(lis)
        
        #un lista contente tutte le read complete
        read = mergeRead(read[:1])
        
        #printList(read)

    scelta = menu()