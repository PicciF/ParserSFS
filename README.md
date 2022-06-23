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

