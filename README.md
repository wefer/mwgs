#MWGS
##QC-pipeline for microbial whole genome sequencing

###Folder structure and naming convention

```
<project>
│
└───<sample_name>
	│
    └───<sample_name>..._1.fastq.gz
	│
	└───<sample_name>..._2.fastq.gz
```

###Usage
```
mwgs.py /path_to/sample_folder/
```

###Output
- Fraction of reads aligned to reference genome
- Duplication rate
- Median insert size

###Requirements
- Java 1.7
- Picard 1.141
- Samtools
- BWA
