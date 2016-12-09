#!/usr/bin/env python
from genologics import lims
from genologics.config import BASEURI, USERNAME, PASSWORD


def get_reference_id(sample_id):
    """Get reference genome for a sample from LIMS

    Inputs: Sample ID
    Outputs: Reference genome - NCBI accession number
    """
    lims_api = lims.Lims(BASEURI, USERNAME, PASSWORD)
    sample = lims.Sample(lims_api, id=sample_id)
    return sample.udf.get('Reference Genome', '')
