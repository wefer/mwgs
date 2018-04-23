#MWGS
A simple QC analysis pipeline developed to assess microbial whole genome sequencing results. The package exposes a CLI for starting analyses and uploading results to a database. It also has a Flask web server for displaying the uploaded results in a web interface.




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
- Python 3.x
- Java 1.7
- Picard 1.141
- Samtools
- BWA


###Example config file
```
$ cat config.py
URI = 'https://example-lims.domain.com'
USER = 'lims_user'
PASSWORD = 'lims_password'
ENTREZ_EMAIL = 'user@example.com' #Can be any email-address
#System specific constants
REF_FOLDER = '/mnt/hds/proj/bioinfo/MICROBIAL/REFERENCES/'
PICARD_JAR = '/mnt/hds/proj/bioinfo/MICROBIAL/picard-tools-1.141/picard.jar'
JAVA = '/mnt/hds/proj/bioinfo/mip/modules/jre1.7.0_45/bin/java'
```

###Environment variable'
```
MWGS_SQL_DATABASE_URI 'SQLAlchemy database URI pointing to the database'
```

###Starting analyses


You can use the CLI to start analyses in two different ways: either for a particular sample or for all samples contained in a project.


$ mwgs start [path to sample dir]

This will launch an analysis right away. Since most samples have relatively few sequenced reads it doesn't take more than 10-20 minutes to complete but it's still not advisable to run it on the login-node for other than testing.


You will more likely start analyses for all samples in a project at a time:


$ mwgs project [path to project dir]

This command will generate a SBATCH script and submit it as a job to a node using SLURM. It parallelizes the analyses using GNU parallel to make use of all available cores on the node. When an analysis finishes it will automatically upload the results to the database.


###Uploading analysis results


If you need to upload results to the database manually you can simply point to the "statistics.yml" output file.


$ mwgs add [path to stats file]