
from setuptools import Command, find_packages, setup
from os import path

this_dir = path.abspath(path.dirname(__file__))
with open(path.join(this_dir, 'README.md'), encoding='utf-8') as f:
	long_description = f.read()


class RunTests(Command):
	"""Run all tests."""
	description = 'run tests'
	
	def initialize_options(self):
		pass

	def finalize_options(self):
		pass

	def run(self):
		pass


setup(
	name = 'mwgs',
	version = '0.1',
	description = 'A tool to make QC on microbial samples',
	long_description = long_description,
	url = 'https://github.com/Clinical-Genomics/mwgs',
	author = 'Hugo Wefer',
	author_email = 'hugo.wefer@scilifelab.se',
	packages = find_packages(exclude=['tests*']),
	entry_points = {'console_scripts' : ['mwgs=mwgs.cli:main',]}
	)

