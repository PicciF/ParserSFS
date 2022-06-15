#parser di file .sfs 
#TO-DO rinominare in modo più sensato le variabili
from difflib import SequenceMatcher
import logging
import rapidfuzz
from email.errors import InvalidMultipartContentTransferEncodingDefect
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
    print("7. Stampa le read unite e pulite")
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

def fondi(prima, seconda):
    match = SequenceMatcher(None, prima, seconda).find_longest_match(0, len(prima), 0, len(seconda))
    common = prima[match.a: match.a + match.size]
    prendere = len(seconda) - len(common)
    str = prima + seconda[-prendere:]
    return str


def fusione(sfs, posizioni):
    readPosizioniRis = []
    readRis = []
    
    for read in range(0, len(sfs)):
        ris = []
        posizioniRis = []
        for i in range(0, len(sfs[read])):
            if not len(sfs[read][i]) == 0:
                prima = sfs[read][i][len(sfs[read][i])-1]
                primaPosizione = posizioni[read][i][len(posizioni[read][i])-1]
                
                ultima = sfs[read][i][0]
                ultimaPosizione = posizioni[read][i][0]
                app = []
                #creare funzione che ritorni true se e overlap e false se non lo e
                if not (int(primaPosizione)+len(prima)>int(ultimaPosizione)):
                    risultatino = sfs[read][i][0]
                    app.append(primaPosizione)
                    app.append(ultimaPosizione)
                    posizioniRis.append(app)
                    for x in range(1, len(sfs[read][i])):
                        risultatino = fondi(sfs[read][i][x], risultatino )
                    ris.append(risultatino)  
                    #ciclo che faccia la fusione una alla volta

                else:
                    contt = []
                    cont = 0
                    #il for serve perche se sono diversi smette l'iterazione
                    for index in range (0, len(prima)):
                        for i in range (0, len(ultima)):
                            while prima[index] == ultima[i] and i<len(ultima)-1:
                                i = i + 1
                                cont = cont + 1
                        contt.append(cont)
                    common = min(contt)     
                    str = prima + ultima[common+1:]
                    #si puo salvare solo la prima in quanto poi è unito
                    app.append(primaPosizione)
                    app.append(ultimaPosizione)
                    posizioniRis.append(app)
                    ris.append(str)
        readPosizioniRis.append(posizioniRis)
        readRis.append(ris)
    return readRis, readPosizioniRis
    
def mergeRead(lista):
    finale = []
    nonOver = []
    nonOverPosizioni = []
    readOv = []
    readPositionOv = []
    
    for read in lista:
        sfs = [read[0][POSITION], read[0][LENGTH], read[0][SFS]]
        sfsRead = []
        sfsReadPos = []
        singoloOv = []
        singolaPositionOv = []
        gruppoOv = []
        gruppoPositionOv = []
        risultofinale = []
        posizioniRisultofinale =[]
        #qui ce la prima sfs
        for cont in range(1, len(read)):
            #qui entro se trovo due stringhe che sono in overleap
            if int(read[cont][POSITION]) + int(read[cont][LENGTH]) > int(sfs[0]):
                over = True
                posizione = int(sfs[0])
                singoloOv.append(sfs[2])
                singolaPositionOv.append(sfs[0])
                sfs[0] = read[cont][POSITION]
                sfs[1] = posizione + int(sfs[1]) - int(read[cont][POSITION])
                sfs[2] = read[cont][SFS]

                
            else:
                #prendere sfs non overlap
                if(over==True):
                    singoloOv.append(sfs[2])
                    singolaPositionOv.append(sfs[0])
                    over = False
                sfs[0] = read[cont][POSITION]
                sfs[1] = read[cont][LENGTH]
                sfs[2] = read[cont][SFS]
                
                app = [read[cont]]
                risultofinale.append(read[cont][SFS])
                posizioniRisultofinale.append(read[cont][POSITION])

                gruppoOv.append(singoloOv)
                singoloOv = []
                gruppoPositionOv.append(singolaPositionOv)
                singolaPositionOv = []
            if cont==len(read)-1:
                if over == True:
                    singoloOv.append(sfs[2])
                    singolaPositionOv.append(sfs[0])
                    over = False
                gruppoOv.append(singoloOv)
                singoloOv = []
                gruppoPositionOv.append(singolaPositionOv)
                singolaPositionOv = []
            sfsReadPos.append(posizioniRisultofinale)
            sfsRead.append(risultofinale)
        nonOver.append(sfsRead)
        nonOverPosizioni.append(sfsReadPos)
        
        
        readOv.append(gruppoOv)

        readPositionOv.append(gruppoPositionOv)

    sfsUnite, posizioni = fusione(readOv, readPositionOv)
    
    #metto in listone le sfs non in over
    f = []
    
    for i in range(0, len(sfsUnite)):
        #ho modificato 
        #TO-DO mettere dimensione dinamica in base alla lunghezza della read
        finale= ["*"] * 25000
        for x in range(0, len(posizioni[i])):
            cont = int(posizioni[i][x][0])
            for c in sfsUnite[i][x]:
                finale[cont-1] = c
                cont = cont + 1
        for x in range(0, len(nonOverPosizioni[i])):
            cont = int(nonOverPosizioni[i][x][0])
            for c in nonOver[i][x]:
                finale[cont-1] = c
                cont = cont + 1
        f.append(finale)           
        #ora devo unire le stringhe
        #AATAACACA 
        #  TAACACAGAG
        #    ACACAGAGC
        #     CACAGAGCG
        #AATAACACAGAGCG
        
        #qui ho solo quelle non overlappate in risultofinale
        #printList(risultofinale)
        ##ris = []
        #print(overlappate[2])
        #print(position[2])
        

            
        
        #in sfs ce lunghezza e posizione iniziale dell overleap
        #in ris ho l overlap f  
    return f
    
            
        
            

        
def formatting(lista):
    app = []
    ris = []
    for l in lista:
        app = l.split()
        ris.append(app)
    ris = sostitutionAst(ris)
    return ris   
 



lista = []
file = open("./ParserSFS/solution_batch_0.sfs", 'r')

for single in file:
    lista.append(single)
file.close()

#rimuovo la stringa iniziale 
#lista[0] = lista[0][36:]

#creo una lista(ogni riga) di lista(ogni campo della riga) 
#lis = formatting(lista[:10]) utile per debug
#invece di avere tutte le righe, così è più capibile 
lis = formatting(lista)

idList = []
for i in lis:
    ap = i[0]
    if not ap in idList:
        idList.append(ap)

def similarita():
    file = open("./ParserSFS/sequenza.txt", 'r')
    contatore = 0
    id = []
    reads = []
    #taking sfs and subdivision for read and saving relative read id
    for i in file:
        if contatore%2==0:
            id.append(i)
        else:
            splitting = i.split("*")
            splittingCleared = list(filter(None, splitting))
            splittingCleared.pop()
            reads.append(splittingCleared)
        contatore = contatore + 1
    file.close()
    #subdivision in cluster for similarity up 80%
    cluster = []
    appoggio = []
    ratio = []
    ratioTotal = []
    #create first cluster with first sfs
    if len(cluster)==0:
        appoggio.append(reads[0][0])
        cluster.append(appoggio)
    
    for x in range(0, len(reads)):
        for y in range(0, len(reads[x])):
            #loop confronta sfs con ogni singola sfs del cluster, ricevo tutti
            #i ratio, media, se superiore a 80 butto li
            # da tenere  print("Sto eseguendo il controllo sulla sfs ", reads[x][y])
            for i in range(0, len(cluster)):
                
                for j in range(0, len(cluster[i])):
                    ratio.append(rapidfuzz.fuzz.ratio(reads[x][y], cluster[i][j]))
                ratioTotal.append(sum(ratio)/len(ratio))
                ratio = []
                # da tenere  print("nel cluster ", i, " ha ratio ", ratioTotal[i])
            for index in range(0, len(ratioTotal)):
                if ratioTotal[index] > 79:
                    # da tenere print("ho aggiunto ", reads[x][y], "in cluster n: ", index)
                    cluster[index].append(reads[x][y])
                    break
                    
                elif index==len(ratioTotal)-1:
                    appoggio = []
                    appoggio.append(reads[x][y])
                    # da tenere print("ho creato un nuovo cluster")
                    cluster.append(appoggio)
                    break
            ratioTotal=[]      
    file = open("./ParserSFS/cluster.txt", 'w')
    
    listaApp = []
    import collections
    for r in reads:
        for j in r:
            listaApp.append(j)
    weight = collections.Counter(listaApp)
   

    for i in range(0, len(cluster)):
        file.write("Cluster Numero " + str(i+1) + ": ")
        for sfs in cluster[i]:
            
            file.write("SFS: " + sfs + " ")
            file.write("Peso: " + str(weight.get(sfs)) + ", ")
        
        #file.write(", ".join(cluster[i]))
        file.write("\n")
        
    file.close()
            
    #print((cluster))    
                
                    
        
        

scelta = menu()

#idList = getIdSFS()

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
        cont = 0
        read = mergeRead(read)
        stringa = ""
        ls =[]
        for r in read:
            stringa=""
            for x in r:
                stringa += x  
            ls.append(stringa)
        #ritorna la stringa unificata per ogni read
        file = open("sequenza.txt", "w")
        #inserire for 
        for i in range(0, len(read)):
            file.write(idList[i])
            file.write("\n")
            file.write("".join(read[i]))
            file.write("\n")
        file.close()
    if scelta == 9:
        #\\wsl$\Ubuntu\home\picci\PingPong\example
        #funzione di controllo
        #prendo il file con le read complete e lo riscrivo
        #controllo che ci siano tutte
        file = open("child.fq", 'r')
        faile = []
        cont = 0
        for cas in file:
            faile.append(cas)
        for i in faile:
            if i[1:].rstrip("\n") in idList:
               cont+=1
        okFile = False
        if cont == len(idList):
            okFile = True
        readComplete = []
        idFile = []
        for c in range(0, len(faile)):
            r = faile[c]
            if r[1:].rstrip("\n") in idList:
                idFile.append(r)
                readComplete.append(faile[c+1])
        file.close()    
        #id list non e in ordine come nel file di read complete
        new = open("verifica.txt", 'w')
        for i in range(0, len(readComplete)):
            new.write(idFile[i])
            new.write("".join(readComplete[i]))
        new.close()  
    if scelta==10:
        file = open('sequenza.txt', 'r')
        fileString = ""
        for c in file:
            for car in c:
                fileString = fileString + car

        test = fileString.split('*')     
        print(list(filter(None,test)))
    if scelta==11:
        similarita()


    scelta = menu()