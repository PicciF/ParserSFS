#parser di file .sfs 
#TO-DO add argument
#TO-DO rinominare in modo più sensato le variabili
from difflib import SequenceMatcher
import rapidfuzz

ID = 0
SFS = 1
POSITION = 2
LENGTH = 3

def inTheMeaddle(lista, a, b):
    ris = []
    allPosition = get(lista, POSITION)
    for cont in range(0, len(lista)):
        if int(allPosition[cont]) >= a and int(allPosition[cont]) <= b:
            ris.append(lista[cont])
    return ris

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
    print("8. Clusterizza")
    print("9. Genera rappresentanti")
    print("10. Esci")
    scelta = int(input("Inserisci la scelta "))
    return scelta

def get(lista, x):
    ris = []
    for l in lista:
        ris.append(l[x])
        print(l[x])
    return ris

def printList(lista):
    for l in lista:
        print(l)
def getRead(lista):
    ris = []
    app = []
    #TO-DO inserire inizializzazione adeguata cosi non prende il primo della prima read
    r = []
    id = lista[0][0]
    prima = True
    for read in lista:
        if read[0] == id:
            if prima:
                if(not(len(r))==0):
                    app.append(r)
                app.append(read)
                prima = False
            else:
                app.append(read)
        else:
            id = read[0]
            
            prima = True
            if(len(app)==0):
                ris.append([r])
            else:
                ris.append(app)
            r = read
            app = []
    return ris

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
                    for index in range (0, len(prima)):
                        for i in range (0, len(ultima)):
                            while prima[index] == ultima[i] and i<len(ultima)-1:
                                i = i + 1
                                cont = cont + 1
                        contt.append(cont)
                    common = min(contt)     
                    str = prima + ultima[common+1:]
                    app.append(primaPosizione)
                    app.append(ultimaPosizione)
                    posizioniRis.append(app)
                    ris.append(str)
        readPosizioniRis.append(posizioniRis)
        readRis.append(ris)
    return readRis, readPosizioniRis
    
def mergeRead(lista):
    finale = []
    readOv = []
    readPositionOv = []    
    sfsRead= []
    sfsReadPos = []
    
    for read in lista:
        sfs = [read[0][POSITION], read[0][LENGTH], read[0][SFS]]
        singoloOv = []
        singolaPositionOv = []
        gruppoOv = []
        gruppoPositionOv = []
        risultofinale = []
        posizioniRisultofinale =[]
        
        for cont in range(1, len(read)):
            if int(read[cont][POSITION]) + int(read[cont][LENGTH]) > int(sfs[0]):
                #there is a overlap
                over = True
                posizione = int(sfs[0])
                singoloOv.append(sfs[2])
                singolaPositionOv.append(sfs[0])
                sfs[0] = read[cont][POSITION]
                sfs[1] = posizione + int(sfs[1]) - int(read[cont][POSITION])
                sfs[2] = read[cont][SFS]     
            else: 
                if(over==True):
                    singoloOv.append(sfs[2])
                    singolaPositionOv.append(sfs[0])
                    over = False
                sfs[0] = read[cont][POSITION]
                sfs[1] = read[cont][LENGTH]
                sfs[2] = read[cont][SFS]
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
        sfsReadPos.append([posizioniRisultofinale])
        sfsRead.append(risultofinale)
        readOv.append(gruppoOv)
        readPositionOv.append(gruppoPositionOv)
    sfsUnite, posizioni = fusione(readOv, readPositionOv)
    
    f = []
    for i in range(0, len(sfsUnite)):
        print("Sto processando una nuova read ", i)
        if not len(sfsUnite[i])==0:
            #TO-DO create method to set dim dynamically
            '''print()
            print(posizioni[i][0][0], " ", posizioni[i][0][1])
            massimo = 0
            if not len(sfsReadPos[i][0]) == 0:
                massimo = max(sfsReadPos[i][0])
            mam = max(posizioni[i][0])
            
            if int(massimo) + len(sfsRead[i]) > int(posizioni[i][0][0])+  int(posizioni[i][0][1]):
                print("sono qui")
                dim = (massimo+len(sfsRead[i]))
            else:
                print("scherzavo")
                dim = (int(posizioni[i][0][0])+  int(posizioni[i][0][1])) 
            '''
            dim = 10000
            finale = ["*"] * dim 

            for x in range(0, len(sfsUnite[i])):   
                cont = int(posizioni[i][x][0])
                for c in sfsUnite[i][x]:
                    finale[cont] = c
                    cont+=1
        for j in range(0, len(sfsRead[i])):
            cont = int(sfsReadPos[i][0][j]) - 1        
            for c in sfsRead[i][j]:    
                finale[cont] = c
                cont+=1
        
        f.append(finale)

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

file = open("/home/picci/PingPong/asgal-wd/solution_batch_0.sfs", 'r')

for single in file:
    lista.append(single)
file.close()
lis = formatting(lista)

idList = []
for i in lis:
    ap = i[0]
    if not ap in idList:
        idList.append(ap)

def similarita():
    file = open("sequenza.txt", 'r')
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
                    if not reads[x][y] in cluster[index]:
                        cluster[index].append(reads[x][y])
                    
                    break
                    
                elif index==len(ratioTotal)-1:
                    appoggio = []
                    appoggio.append(reads[x][y])
                    # da tenere print("ho creato un nuovo cluster")
                    
                    cluster.append(appoggio)
                    break
            ratioTotal=[]      
    file = open("cluster.txt", 'w')
    
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
            
                
def indicizza():
    file = open("cluster.txt", 'r')
    rappresentanti = []
    sfs = []
    appsfs = []
    peso = []
    apppeso = []
    for row in file:
        #clean file and get sfs and weight
        cluster = row.split(" ") 
        cluster = cluster[4:]
        for c in cluster:
            if c=="SFS:":
                cluster.remove(c)
        cluster.remove("\n")
        for index in range(0, len(cluster), 3):
            appsfs.append(cluster[index])
            apppeso.append(cluster[index+2].replace(",",""))
        
        sfs.append(appsfs)
        peso.append(apppeso)
        appsfs = []
        apppeso = []
    #I determine the sfs representatives for each cluster
    file.close()
    for i in range(0, len(peso)):
        maxi = max(peso[i])
        rappresentanti.append(sfs[i][peso[i].index(maxi)])
    clusterDeleted = []
    #removing and saving the number of clusters deleted
    for r in rappresentanti:
        if len(r)<15:
            clusterDeleted.append(rappresentanti.index(r))
            rappresentanti.remove(r)
    fileFasta = open("rappresentanti.fastq", 'w')
    for i in range(0, len(rappresentanti)):
        fileFasta.write(">"+ str(i+1))
        fileFasta.write("\n")
        fileFasta.write(rappresentanti[i])
        fileFasta.write("\n")
    
    
    
    fileFasta.close()   

scelta = menu()



#if we use python 3.10 we could use switch statement
#so for now use simply if statement

while(scelta != 11):
    if scelta == 1:
        #print all sfs
        sfs = get(lis, SFS)
        printList(sfs)
    if scelta == 2:
        #print all positions
        sfs = get(lis, POSITION)
        printList(sfs)
    if scelta == 3:
        #print all lenghts
        sfs = get(lis, LENGTH)
        printList(sfs)
    if scelta == 4:
        #print all id
        sfs = get(lis, ID)
        printList(sfs)
    if scelta == 5:
        #print position and length from specif sfs
        sfsUtente = input("Inserisci la sfs di cui vuoi posizione e lunghezza: ")
        sfsUtente = sfsUtente.upper() 
        posizione, lunghezza = getFromSFS(lis, sfsUtente)
        print("la posizione della sfs inserita è: " + posizione)
        print("La lunghezza della sfs inserita è: " + lunghezza)
    if scelta == 6:
        a = int(input("Inserisci la posizione minima compresa: "))
        b = int(input("Inserisci la posizione massima compresa: "))
        sfs = inTheMeaddle(lis, a, b)
        printList(sfs)
    if scelta == 7:
        #list of lists, in which for each position have a read, in which have all sequences
        read = getRead(lis)
        cont = 0
        read = mergeRead(read)
        stringa = ""
        ls =[]
        
        for r in read:
            stringa=""
            for x in r:
                stringa += x  
            ls.append(stringa)
        
        #return unified string 
        file = open("sequenza.txt", 'w')
       
        for i in range(0, len(read)):
            file.write(idList[i])
            file.write("\n")
            file.write("".join(read[i]))
            file.write("\n") 
        file.close()    
    if scelta==8:
        similarita()
    if scelta==9:
        indicizza()
    if scelta==10:
        file = open('sequenza.txt', 'r')
        fileString = ""
        for c in file:
            for car in c:
                fileString = fileString + car

        test = fileString.split('*')     
        print(list(filter(None,test)))

    scelta = menu()