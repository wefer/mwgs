#!/usr/bin/env python

import os
from Bio import Entrez
from subprocess import Popen
from config import ENTREZ_EMAIL, REF_FOLDER

#Set up a temporary trap for output
DEVNULL = open(os.devnull, 'wb')

Entrez.email = ENTREZ_EMAIL


class Reference(object):
	"""
	Reference genome object
	"""

	def __init__(self, ref_nc):
		self.ref_nc = ref_nc
		self.ref_folder = os.path.join(REF_FOLDER, ref_nc)
		if not self.reference_exists:
			self.download_reference()
			self.index_reference()
		else:
			print('Reference genome in place')
			self.fasta_file = os.path.join(self.ref_folder, self.ref_nc + '.fasta')

	@property
	def reference_exists(self):
		"""
		Check if the reference genome is already in place
		"""
		return os.path.exists(self.ref_folder)

	def download_reference(self):
		"""
		Download nucleotide sequence from NCBI
		"""
		nc_number = self.ref_nc.upper().lstrip('NC_')
		print('Downloading reference genome: {}'.format(self.ref_nc))
		record = Entrez.efetch(db='nucleotide', id=self.ref_nc, rettype='fasta', retmod='text')
		sequence = record.read()
		os.mkdir(self.ref_folder)
		self.fasta_file = os.path.join(self.ref_folder, self.ref_nc + '.fasta')
		print('Creating file: {}'.format(self.fasta_file))
		with open(self.fasta_file, 'w') as f:
			f.write(sequence)

	def index_reference(self):
		"""
		Index reference sequence with bwa
		"""
		print('Indexing reference genome...')
		p = Popen(['/mnt/hds/proj/bioinfo/MICROBIAL/bwa', 'index', self.fasta_file], stderr=DEVNULL, stdout=DEVNULL)
		p.wait()
		print('Indexing finished')
