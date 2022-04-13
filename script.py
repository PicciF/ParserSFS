#parser di file .sfs 

def getFromSFS(lista, sfs):
    allSFS = get(lista, SFS)
    for cont in range(0, len(allSFS)):
        if allSFS[cont] == sfs:
            return lista[cont][1], lista[cont][2]
def menu():
    print("1. Stampa tutte le SFS")
    print("2. Stampa tutte le posizioni")
    print("3. Stampa tutte le lunghezze")
    print("4. Stampa posizione e lunghezza di una specifica sfs")
    print("5. Esci")
    scelta = int(input("Inserisci la scelta "))
    return scelta
def get(lista, x):
    ris = []
    for l in lista:
        ris.append(l[x])
    return ris

#rimozione dell'asterisco 
def removeAst(lista):
    for cont in range(0, len(lista)):
        if len(lista[cont]) != 4:
            lista[cont] = lista[cont][1:]
    return lista
def formatting(lista):
    app = []
    ris = []
    for l in lista:
        app = l.split()
        ris.append(app)
        #print(app)
    ris = removeAst(ris)
    return ris    
#dichiarazione costanti
SFS = 0
POSITION = 1
LENGTH = 2


lista = []
file = open("solution_batch_0.sfs", 'r')
for single in file:
    lista.append(single)


#rimuovo la stringa iniziale 
lista[0] = lista[0][36:]


#creo una lista(ogni riga) di lista(ogni campo della riga) 
lis = formatting(lista[:10])

scelta = menu()

#personalmente userei uno switch ma è presente solo
#nella versione 3.10 di python e non so se si può usare
#quindi ora inserisci un semplice if
while(scelta != 5):
    if scelta == 1:
        #stampo tutte le sfs
        sfs = get(lis, SFS)
        for s in sfs:
            print(s)
    if scelta == 2:
        #stampo tutte le posizioni
        sfs = get(lis, POSITION)
        for s in sfs:
            print(s)
    if scelta == 3:
        #stampo tutte le lunghezze
        sfs = get(lis, LENGTH)
        for s in sfs:
            print(s)
    if scelta == 4:
        #stampo posizione e lunghezza da una specifica sfs
        sfsUtente = input("Inserisci la sfs di cui vuoi posizione e lunghezza: ")

        #converto in upper case in caso l'utente abbia inserito i caratteri in minuscolo
        sfsUtente = sfsUtente.upper()
        
        posizione, lunghezza = getFromSFS(lis, sfsUtente)
        print("la posizione della sfs inserita è: " + posizione)
        print("La lunghezza della sfs inserita è: " + lunghezza)

    scelta = menu()







#print(file.read())