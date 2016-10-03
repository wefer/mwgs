#/usr/bin/env python

import logging
import sys
from os import path
import glob

from reference_handling import Reference
from get_lims_info import get_reference_id
from align_to_reference import perform_alignment, remove_duplicates
from calculate_metrics import get_insert_size, reads_aligned


class Sample(object):
	def __init__(self, sample_path):
		self.sample_path = sample_path
		self.sample_name = path.basename(path.normpath(sample_path))
		self.sample_ref_nc = get_reference_id(self.sample_name)
		self.sample_reference = Reference(self.sample_ref_nc)
		self.r1 = glob.glob(sample_path + '/*_1.fastq.gz') 
		self.r2 = [x.replace('_1.fastq.gz', '_2.fastq.gz') for x in self.r1]

	def run_qc(self):
		prefix = path.join(self.sample_path, self.sample_name)
		self.bamfile, self.dupmetrics = remove_duplicates(perform_alignment(prefix, self.r1, self.r2, self.sample_reference.fasta_file))
		self.total_reads, self.mapped_reads = reads_aligned(self.bamfile)
		self.insertmetricsfile, self.inserthistfile = get_insert_size(self.bamfile)

	def __str__(self):
		return '<Sample {} at {}>'.format(self.sample_path, path.abspath(self.sample_path))

	def dump_metrics(self):
		with open(os.join(self.sample_path, 'stats.csv'), 'w') as f:
			f.write('')

if __name__ == '__main__':
	sample_path = sys.argv[1]
	s = Sample(sample_path)
	s.run_qc()


