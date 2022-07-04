# Descrizione funzioni

## 1. Stampa tutte le sfs

La funzione in questione stampa tutte le sfs presenti nel file .sfs caricato in input

## 2. Stampa tutte le posizioni

La funzione in questione stampa tutte le posizioni delle sfs presenti nel file .sfs caricato in input

## 3. Stampa tutte le lunghezze 

La funzione in questione stampa tutte le lunghezze delle sfs presenti nel file .sfs caricato in input

## 4. Stampa tutti gli id 

La funzione in questione stampa tutti gli id delle read appartenenti delle sfs presenti nel file .sfs caricato in input

## 5. Stampa posizione e lunghezza 

La funzione richiede in input una sfs e restituisce come output la posizione e la lunghezza

## 6. Sfs tra due posizioni

La funzione richiede in input due posizioni, rispettivamente quella iniziale e quella finale, come output restituisce tutte le sfs in questo intervallo

## 7. Creazione file sequenza.txt

La funzione prima di generare un file, unisce tutte le sfs in overlap e crea una lista contente tante liste quante sono le read. In ogni sotto lista è contenuta la sequenza totale unificata, quindi sfs in overlap con le sfs che non erano in overlap. Ovviamente nel file delle sfs dato input non è presente la totalità delle basi, quindi ogni base ignota viene sostituita con un asterisco.
Succesivamente genera un file (sequenza.txt) il quale contiene tutte le sequenze con tutte le read. 

## 8. Creazione file cluster.txt

La funzione usa il file precedentemente creato per creare i cluster con un criterio dell`80% di similarità, usa il file creato in precedenza in modo da rendere a se stanti le funzioni. In coclusione il metodo genera il file cluster.txt in modo da poter vedere tutti i cluster con tutte le sfs presenti e il loro peso, il peso indica il numero di volte che quella sfs si ripete, ed è di fondamentale importanza nella creazione del file dei rappresentanti.

## 9. Creazione file rappresentative.fastq

La funzione estrapola dal file generato con la funzione precedente una sfs rappresentante il cluster, è stabilito a seconda di quale sfs ha un peso maggiore, ossia ripetuta più volte. Al termine della selezione genera il file di output, rappresentive.fastq 














# Comandi eseguiti sui dati di test

1. Conversione sample_1.fa in sample_1.fq

```bash
seqtk seq -F '#' /home/picci/galig/example/input/sample_1.fa > /home/picci/galig/example/input/sample_converted_1.fq
```

2. Indicizzazione genoma

```bash
./PingPong index --fastq /home/picci/galig/example/input/genome.fa --index /home/picci/galig/example/input/genome.fa.fmd
```

3. Ricerca SFS

```bash
./PingPong search --index /home/picci/galig/example/input/genome.fa.fmd --fastq /home/picci/galig/example/input/sample_converted_1.fq --overlap -1 --workdir asgal-wd --threads 1
```

4. Indicizzazione cromosomi 

```bash
./bwa index /home/picci/galig/example/input/genome.fa
```

5. Esecuzione comando fastmap

```bash
./bwa fastmap /home/picci/galig/example/input/genome.fa /home/picci/ParserSFS/rappresentanti.fastq
```

