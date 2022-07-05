from difflib import SequenceMatcher
from importlib.resources import path
from operator import length_hint
import rapidfuzz
import argparse




def inTheMeaddle(lista, a, b):
    ris = []
    allPosition = get(lista, POSITION)
    for cont in range(0, len(lista)):
        if int(allPosition[cont]) >= a and int(allPosition[cont]) <= b:
            ris.append(lista[cont])
    return ris

def getFromSFS(lista, sfs, idUser):
    allSFS = get(lista, SFS)
    for cont in range(0, len(allSFS)):
        if allSFS[cont] == sfs and lista[cont][ID]==idUser:
            return lista[cont][POSITION], lista[cont][LENGTH]

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
    return ris

def printList(lista):
    for l in lista:
        print(l)

def getRead(record):
    result = []
    support = []
    precRead = []
    id = record[0][0]
    first = True
    for read in record:
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
    
def mergeRead(record):
    res = []
    readOv = []
    readPositionOv = []    
    sfsRead= []
    sfsReadPos = []
    
    for read in record:
        sfs = [read[0][POSITION], read[0][LENGTH], read[0][SFS]]
        singleOv = []
        singlePositionOv = []
        groupOv = []
        groupPositionOv = []
        finalResult = []
        positionFinalResutl =[]
        
        for cont in range(1, len(read)):
            if int(read[cont][POSITION]) + int(read[cont][LENGTH]) > int(sfs[0]):
                #there is a overlap
                over = True
                posizione = int(sfs[0])
                singleOv.append(sfs[2])
                singlePositionOv.append(sfs[0])
                sfs[0] = read[cont][POSITION]
                sfs[1] = posizione + int(sfs[1]) - int(read[cont][POSITION])
                sfs[2] = read[cont][SFS]     
            else: 
                if(over==True):
                    singleOv.append(sfs[2])
                    singlePositionOv.append(sfs[0])
                    over = False
                sfs[0] = read[cont][POSITION]
                sfs[1] = read[cont][LENGTH]
                sfs[2] = read[cont][SFS]
                finalResult.append(read[cont][SFS])
                positionFinalResutl.append(read[cont][POSITION]) 
                groupOv.append(singleOv)
                singleOv = []
                groupPositionOv.append(singlePositionOv)
                singlePositionOv = []
            if cont==len(read)-1:
                if over == True:
                    singleOv.append(sfs[2])
                    singlePositionOv.append(sfs[0])
                    over = False
                groupOv.append(singleOv)
                singleOv = []
                groupPositionOv.append(singlePositionOv)
                singlePositionOv = []    
        sfsReadPos.append([positionFinalResutl])
        sfsRead.append(finalResult)
        readOv.append(groupOv)
        readPositionOv.append(groupPositionOv)
    sfsUnified, position = fusion(readOv, readPositionOv)
    
    result = []
    for i in range(0, len(sfsUnified)):
        print("Processing new read N:", i)
        length = 0
        pInitial = 0
        if not len(sfsUnified[i])==0:
            if len(sfsUnified)>1:
                length = len(sfsUnified[i][0])
            else:
                length(sfsUnified[i])
            pInitial = int(position[i][0][0])
            dim = length+pInitial+1       
            res = ["*"] * dim 

            for x in range(0, len(sfsUnified[i])):   
                cont = int(position[i][x][0])
                for c in sfsUnified[i][x]:
                    res[cont] = c
                    cont+=1
        for j in range(0, len(sfsRead[i])):
            cont = int(sfsReadPos[i][0][j]) - 1        
            for c in sfsRead[i][j]:    
                res[cont] = c
                cont+=1
        
        result.append(res)

    return result
      
def formatting(record):
    support = []
    result = []
    for l in record:
        support = l.split()
        result.append(support)
    result = asteriskRemoval(result)
    return result   
 


def similarity():
    file = open(outputDir + "sequence.txt", 'r')
    counter = 0
    id = []
    reads = []
    #taking sfs and subdivision for read and saving relative read id
    for i in file:
        if counter%2==0:
            id.append(i)
        else:
            splitting = i.split("*")
            splittingCleared = list(filter(None, splitting))
            splittingCleared.pop()
            reads.append(splittingCleared)
        counter = counter + 1
    file.close()
    #subdivision in cluster for similarity up 80%
    cluster = []
    support = []
    ratio = []
    ratioTotal = []
    #create first cluster with first sfs
    if len(cluster)==0:
        support.append(reads[0][0])
        cluster.append(support)
    
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
                if ratioTotal[index] > THRESHOLD:
                    # da tenere print("ho aggiunto ", reads[x][y], "in cluster n: ", index)
                    if not reads[x][y] in cluster[index]:
                        cluster[index].append(reads[x][y])
                    
                    break
                    
                elif index==len(ratioTotal)-1:
                    support = []
                    support.append(reads[x][y])
                    # da tenere print("ho creato un nuovo cluster")
                    
                    cluster.append(support)
                    break
            ratioTotal=[]      
    file = open(outputDir + "cluster.txt", 'w')
    
    #listaApp = []
    suppList = []
    import collections
    for r in reads:
        for j in r:
            suppList.append(j)
    weight = collections.Counter(suppList)
   


    for i in range(0, len(cluster)):
        file.write("Cluster Number " + str(i+1) + ": ")
        for sfs in cluster[i]:
            
            file.write("SFS: " + sfs + " ")
            file.write("Weight: " + str(weight.get(sfs)) + ", ")
        
        #file.write(", ".join(cluster[i]))
        file.write("\n")
        
    file.close()
            
                
def rappresentant():
    file = open(outputDir + "cluster.txt", 'r')
    representatives = []
    sfs = []
    suppSfs = []
    weight = []
    suppWeight = []
    for row in file:
        #clean file and get sfs and weight
        cluster = row.split(" ") 
        cluster = cluster[4:]
        for c in cluster:
            if c=="SFS:":
                cluster.remove(c)
        cluster.remove("\n")
        for index in range(0, len(cluster), 3):
            suppSfs.append(cluster[index])
            suppWeight.append(cluster[index+2].replace(",",""))
        
        sfs.append(suppSfs)
        weight.append(suppWeight)
        suppSfs = []
        suppWeight = []
    #I determine the sfs representatives for each cluster
    file.close()
    for i in range(0, len(weight)):
        maxi = max(weight[i])
        representatives.append(sfs[i][weight[i].index(maxi)])
    clusterDeleted = []
    #removing and saving the number of clusters deleted
    repsFiltered = [] 
    #for i in range(0, len(rappresentanti)):
     
    for r in representatives:
        if len(r)<15:
            clusterDeleted.append(representatives.index(r))
        else:
            repsFiltered.append(r)

    fileFasta = open(outputDir + "representatives.fastq", 'w')
    
    for i in range(0, len(repsFiltered)):
        fileFasta.write(">"+ str(i+1))
        fileFasta.write("\n")
        fileFasta.write(repsFiltered[i])
        fileFasta.write("\n")

    fileFasta.close()   

def main():
    pass
#scelta = menu()
parser = argparse.ArgumentParser(description="Welcome in MONI")

parser.add_argument("o", type=int, default=1, help="Operation")
parser.add_argument("sfsFile", help="Insert sfs file path" )
parser.add_argument("workdir", help="Output Directory" )
subparsers = parser.add_subparsers(title='Operation options', description='Number and description of possible operation',help='sub-command help')
subparsers.add_parser("1", help="Print all sfs")
subparsers.add_parser("2", help="print all position of sfs")
subparsers.add_parser("3", help="print all lenghts")
subparsers.add_parser("4", help="print all id of sfs")
subparsers.add_parser("5", help="print position and lenght from specific sfs")
subparsers.add_parser("6", help="print all sfs between two position")
subparsers.add_parser("7", help="Generate sequence file that is a merging all sfs")
subparsers.add_parser("8", help="Generate cluster file")
subparsers.add_parser("9", help="Generate representive file")



args = parser.parse_args()

choice = int(args.o)
pathSfsFile = str(args.sfsFile)
outputDir = str(args.workdir)

ID = 0
SFS = 1
POSITION = 2
LENGTH = 3
THRESHOLD = 79


firstList = []

file = open(pathSfsFile, 'r')

for single in file:
    firstList.append(single)
file.close()
record = []
record = formatting(firstList)

idList = []
for i in record:
    id = i[0]
    if not id in idList:
        idList.append(id)


#if we use python 3.10 we could use switch statement
#so for now use simply if statement

#while(scelta != 11):
if choice == 1:
    #print all sfs
    sfs = get(record, SFS)
    printList(sfs)
if choice == 2:
    #print all positions
    sfs = get(record, POSITION)
    printList(sfs)
if choice == 3:
    #print all lenghts
    sfs = get(record, LENGTH)
    printList(sfs)
if choice == 4:
    #print all id
    sfs = get(record, ID)
    printList(sfs)
if choice == 5:
    #print position and length from specif sfs
    sfsUser = input("Inserisci la sfs di cui vuoi posizione e lunghezza: ")
    idUser = input("Inserisci l`id della read di cui fa parte l`sfs inserita: ")
    sfsUser = sfsUser.upper() 
    position, length = getFromSFS(record, sfsUser, idUser)
    print("la posizione della sfs inserita è: " + position)
    print("La lunghezza della sfs inserita è: " + length)
if choice == 6:
    a = int(input("Inserisci la posizione minima compresa: "))
    b = int(input("Inserisci la posizione massima compresa: "))
    sfs = inTheMeaddle(record, a, b)
    printList(sfs)
if choice == 7:
    #list of lists, in which for each position have a read, in which have all sequences
    read = getRead(record)
    
    cont = 0
    read = mergeRead(read)
    str = ""
    #rename this list
    ls =[]
    
    for r in read:
        str=""
        for x in r:
            str += x  
        ls.append(str)
    
    #return unified string 
    file = open(outputDir + "sequence.txt", 'w')
    
    for i in range(0, len(read)):
        file.write(idList[i])
        file.write("\n")
        file.write("".join(read[i]))
        file.write("\n") 
    file.close()    
if choice==8:
    similarity()
if choice==9:
    rappresentant()


if __name__ == "__main__":
    main()
    