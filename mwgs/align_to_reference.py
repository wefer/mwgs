#!/usr/bin/env python
import subprocess
import os

from config import PICARD_JAR, JAVA

#Temporary trap for output
DEVNULL=open(os.devnull, 'wb')

def perform_alignment(sample_name, pe_reads_1, pe_reads_2, ref, threads=1):
	"""
	Perform alignment to reference genome with bwa mem.
	Sort and convert to .bam-format
	Inputs: Sample_name, Forward fastqs, reverse fastqs, index reference genome
	Returns: .bam filepath
	"""
	bamfile_prefix = sample_name + '_srt'
	
	cmd1 = ['/mnt/hds/proj/bioinfo/MICROBIAL/bwa', 'mem', '-t', str(threads), '-M', 
			ref, 
			'<(cat {})'.format(*pe_reads_1), 
			'<(cat {})'.format(*pe_reads_2)]
	p1 = subprocess.Popen(cmd1, stdout=subprocess.PIPE)

	cmd2 = ['samtools', 'view', '-bS', '-']
	p2 = subprocess.Popen(cmd2, stdin=p1.stdout, stdout=subprocess.PIPE)

	cmd3 = ['samtools', 'sort', '-', bamfile_prefix]
	p3 = subprocess.Popen(cmd3, stdin=p2.stdout)

	rcode = p3.wait()
	if rcode != 0:
		raise subprocess.CalledProcessError(rcode, cmd1+cmd2+cmd3)		
	return bamfile_prefix + '.bam'

def remove_duplicates(bamfile):
	"""
	Remove duplicates with samtools
	"""
	bam_rmdup = bamfile.replace('.bam', '_rmdup.bam')
	dup_metrics = bamfile.replace('.bam', '_dupmetr.txt')
	cmd = [JAVA, '-jar', PICARD_JAR,
			'MarkDuplicates', 
			'I={}'.format(bamfile),
			'O={}'.format(bam_rmdup),
			'M={}'.format(dup_metrics),
			'REMOVE_DUPLICATES=true']

	p = subprocess.Popen(cmd)
	rcode = p.wait()
	if rcode != 0:
		raise subprocess.CalledProcessError(rcode, cmd)
	return (bam_rmdup, dup_metrics)


