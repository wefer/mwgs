#!/usr/bin/env python

from genologics import lims
from genologics.config import BASEURI, USERNAME, PASSWORD

def get_reference_id(sample_name):
	"""
	Get reference genome for a sample from LIMS
	Inputs: Sample ID
	Outputs: Reference genome - NCBI accession number
	"""
	
	l = lims.Lims(BASEURI, USERNAME, PASSWORD)
	s = lims.Sample(l, id=sample_name)
	return s.udf.get('Reference Genome', '')
