#parser di file .sfs 
#TO-DO add argument
#TO-DO rinominare in modo più sensato le variabili
from difflib import SequenceMatcher
from importlib.resources import path
from operator import length_hint
import rapidfuzz
import argparse
#/home/picci/tmp/ParserSFS/solution_batch_0.sfs



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

#probabily is to remove 
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

def getRead(list):
    result = []
    support = []
    precRead = []
    id = list[0][0]
    first = True
    for read in list:
        if read[0] == id:
            if first:
                if(not(len(precRead))==0):
                    support.append(precRead)
                support.append(read)
                first = False
            else:
                support.append(read)
        else:
            id = read[0]
            
            first = True
            if(len(support)==0):
                result.append([precRead])
            else:
                result.append(support)
            precRead = read
            support = []
    return result

def asteriskRemoval(lista):
    idRead = "" 
    for read in lista:
        if not read[0] == "*":
            idRead = read[0]
        else:
            read[0] = idRead
    return lista

#join two single sfs
def union(first, second):
    match = SequenceMatcher(None, first, second).find_longest_match(0, len(first), 0, len(second))
    common = first[match.a: match.a + match.size]
    take = len(second) - len(common)
    str = first + second[-take:]
    return str


def fusion(sfs, position):
    readPositionResult = []
    readResult = []
    
    for read in range(0, len(sfs)):
        result = []
        positionResult = []
        for i in range(0, len(sfs[read])):
            if not len(sfs[read][i]) == 0:
                first = sfs[read][i][len(sfs[read][i])-1]
                firstPosition = position[read][i][len(position[read][i])-1]
                
                last = sfs[read][i][0]
                lastPosition = position[read][i][0]
                support = []
                #creare funzione che ritorni true se e overlap e false se non lo e
                if not (int(firstPosition)+len(first)>int(lastPosition)):
                    res = sfs[read][i][0]
                    support.append(firstPosition)
                    support.append(lastPosition)
                    positionResult.append(support)
                    for x in range(1, len(sfs[read][i])):
                        res = union(sfs[read][i][x], res )
                    result.append(res)  
                    #ciclo che faccia la fusione una alla volta

                else:
                    contMin = []
                    cont = 0
                    for index in range (0, len(first)):
                        for i in range (0, len(last)):
                            while first[index] == last[i] and i<len(last)-1:
                                i = i + 1
                                cont = cont + 1
                        contMin.append(cont)
                    common = min(contMin)     
                    str = first + last[common+1:]
                    support.append(firstPosition)
                    support.append(lastPosition)
                    positionResult.append(support)
                    result.append(str)
        readPositionResult.append(positionResult)
        readResult.append(result)
    return readResult, readPositionResult
    
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
    sfsUnite, posizioni = fusion(readOv, readPositionOv)
    
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
      
def formatting(list):
    support = []
    result = []
    for l in list:
        support = l.split()
        result.append(support)
    result = asteriskRemoval(result)
    return result   
 


def similarity():
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
            
                
def index():
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
    rappresentantiVeri = [] 
    #for i in range(0, len(rappresentanti)):
    ##    print(rappresentanti[i])
     
    for r in rappresentanti:
        if len(r)<15:
            clusterDeleted.append(rappresentanti.index(r))
        else:
            rappresentantiVeri.append(r)
    #print(len(rappresentantiVeri))

    fileFasta = open("rappresentanti.fastq", 'w')
    
    for i in range(0, len(rappresentantiVeri)):
        fileFasta.write(">"+ str(i+1))
        fileFasta.write("\n")
        fileFasta.write(rappresentantiVeri[i])
        fileFasta.write("\n")

    fileFasta.close()   

#scelta = menu()
parser = argparse.ArgumentParser(description="Welcome in MONI")
#se metti il trattino indica che è opzionale, dire a nada
parser.add_argument("o", type=int, default=1, help="Operazione")
parser.add_argument("sfsFile", help="insert sfs file path" )


args = parser.parse_args()

choice = int(args.o)
pathSfsFile = str(args.sfsFile)


ID = 0
SFS = 1
POSITION = 2
LENGTH = 3

firstList = []

file = open(pathSfsFile, 'r')

for single in file:
    firstList.append(single)
file.close()
list = []
list = formatting(firstList)

idList = []
for i in list:
    id = i[0]
    if not id in idList:
        idList.append(id)


#if we use python 3.10 we could use switch statement
#so for now use simply if statement

#while(scelta != 11):
if choice == 1:
    #print all sfs
    sfs = get(list, SFS)
    printList(sfs)
if choice == 2:
    #print all positions
    sfs = get(list, POSITION)
    printList(sfs)
if choice == 3:
    #print all lenghts
    sfs = get(list, LENGTH)
    printList(sfs)
if choice == 4:
    #print all id
    sfs = get(list, ID)
    printList(sfs)
if choice == 5:
    #print position and length from specif sfs
    sfsUser = input("Inserisci la sfs di cui vuoi posizione e lunghezza: ")
    sfsUser = sfsUser.upper() 
    position, length = getFromSFS(list, sfsUser)
    print("la posizione della sfs inserita è: " + position)
    print("La lunghezza della sfs inserita è: " + length)
if choice == 6:
    a = int(input("Inserisci la posizione minima compresa: "))
    b = int(input("Inserisci la posizione massima compresa: "))
    sfs = inTheMeaddle(list, a, b)
    printList(sfs)
if choice == 7:
    #list of lists, in which for each position have a read, in which have all sequences
    read = getRead(list)
    cont = 0
    read = mergeRead(read)
    str = ""
    ls =[]
    
    for r in read:
        str=""
        for x in r:
            str += x  
        ls.append(str)
    
    #return unified string 
    file = open("sequence.txt", 'w')
    
    for i in range(0, len(read)):
        file.write(idList[i])
        file.write("\n")
        file.write("".join(read[i]))
        file.write("\n") 
    file.close()    
if choice==8:
    similarity()
if choice==9:
    index()
if choice==11:
    file = open('sequenza.txt', 'r')
    fileString = ""
    for c in file:
        for car in c:
            fileString = fileString + car

    test = fileString.split('*')     
    print(list(filter(None,test)))
if choice == 12:
    getRead(list)

    #scelta = menu()