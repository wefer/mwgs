#!/usr/bin/env python

import subprocess

from config import PICARD_JAR, JAVA

def get_insert_size(bamfile):
	"""
	Run Picard tools Collect Insert Size Metrics
	"""
	output = bamfile.rstrip('.bam') + '.insertmetrics.txt'
	hist = bamfile.rstrip('.bam') + '.inserthistogram.pdf'
	cmd = [JAVA,
			'-jar',
			PICARD_JAR,
			'CollectInsertSizeMetrics',
			'H={}'.format(hist),
			'I={}'.format(bamfile),
			'O={}'.format(output)]
	p = subprocess.Popen(cmd)
	p.wait()
	
	return (output, hist)


def reads_aligned(bamfile):
	"""
	Calculate fraction of reads mapped to reference
	"""
	cmd_mapped = ['samtools', 'view', '-c', '-F', '4', bamfile]
	p1 = subprocess.Popen(cmd_mapped, stdout=subprocess.PIPE)
	mapped_reads = int(p1.stdout.read().rstrip())

	cmd_total = ['samtools', 'view', '-c', bamfile]
	p2 = subprocess.Popen(cmd_total, stdout=subprocess.PIPE)
	total_reads = int(p2.stdout.read().rstrip())

	return (total_reads, mapped_reads)
