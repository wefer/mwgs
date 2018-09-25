#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from os import path
import glob
import subprocess

from genologics.entities import Sample as LimsSample
import yaml

from mwgs.reference_handling import Reference
from mwgs.align_to_reference import perform_alignment, remove_duplicates
from mwgs.calculate_metrics import get_insert_size, reads_aligned


class Sample(object):
    def __init__(self, lims, sample_path, parallel=False):
        self.sample_path = sample_path
        self.parallel = parallel
        self.sample_name = path.basename(path.normpath(sample_path))
        self.lims_sample = LimsSample(lims, id=self.sample_name)
        self.sample_ref_nc = self.lims_sample.udf.get('Reference Genome Microbial', '')
        self.project_id = self.lims_sample.project.id
        self.external_name = self.lims_sample.name
        if not self.sample_ref_nc:
            raise ValueError('No reference found in LIMS')
        self.sample_reference = Reference(self.sample_ref_nc)
        self.r1 = glob.glob(sample_path + '/*_1.fastq.gz')
        self.r2 = [x.replace('_1.fastq.gz', '_2.fastq.gz') for x in self.r1]

    def __str__(self):
        return '<Sample {} at {}>'.format(self.sample_path,
                                          path.abspath(self.sample_path))

    def run_qc(self):
        prefix = path.join(self.sample_path, self.sample_name)
        if self.parallel:
            threads = 4
        else:
            threads = 1
        alignment = perform_alignment(prefix, self.r1, self.r2,
                                      self.sample_reference.fasta_file,
                                      threads=threads)
        self.bamfile, self.dupmetrics = remove_duplicates(alignment)
        self.total_reads, self.mapped_reads = reads_aligned(self.bamfile)
        (self.insertmetricsfile,
         self.inserthistfile) = get_insert_size(self.bamfile)
        self.median_insert = self.gather_insert_metrics()
        self.duplication_rate = self.gather_duplication_metrics()
        self.above_10X = self.gather_fraction_above_cutoff(10)
        self.above_30X = self.gather_fraction_above_cutoff(30)
        self.above_50X = self.gather_fraction_above_cutoff(50)
        self.above_100X = self.gather_fraction_above_cutoff(100)

    def gather_insert_metrics(self):
        with open(self.insertmetricsfile, 'r') as in_handle:
            line = ''
            while not line.startswith('MEDIAN_INSERT_SIZE'):
                    line = in_handle.readline()
            return in_handle.readline().split('\t')[0]

    def gather_duplication_metrics(self):
        with open(self.dupmetrics, 'r') as in_handle:
            line = ''
            while not line.startswith('LIBRARY'):
                line = in_handle.readline()
            return in_handle.readline().split('\t')[-2]

    def gather_fraction_above_cutoff(self, cutoff):
        cmd = ['samtools', 'depth', '-a', self.bamfile]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        proc_out, proc_error = p.communicate()
        lines = proc_out.decode('utf-8').split('\n')
        bases_below_cutoff = 0
        for line in lines[:-1]:
            if int(line.split('\t')[2]) < cutoff:
                bases_below_cutoff += 1
        return (len(lines) - bases_below_cutoff) / len(lines)

    def dump_metrics(self):
        duplicates = self.mapped_reads / self.total_reads
        data = {
            'Sample Name': self.sample_name,
            'External Name': self.external_name,
            'Project': self.project_id,
            'Reference Genome': self.sample_ref_nc,
            'Total Reads': self.total_reads,
            'Median Insert Size': self.median_insert,
            'Duplication Rate': self.duplication_rate,
            'Fraction aligned to Reference': duplicates,
            'Fraction of bases with cov >= 10X': self.above_10X,
            'Fraction of bases with cov >= 30X': self.above_30X,
            'Fraction of bases with cov >= 50X': self.above_50X,
            'Fraction of bases with cov >= 100X': self.above_100X
        }

        out_path = path.join(self.sample_path, 'statistics.yml')
        with open(out_path, 'w') as out_handle:
            yaml.safe_dump(data, out_handle, default_flow_style=False,
                           allow_unicode=True)


if __name__ == '__main__':
    sample_path = sys.argv[1]
    s = Sample(sample_path)
    s.run_qc()
    s.dump_metrics()
