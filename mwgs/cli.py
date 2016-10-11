"""
mwgs

Usage:
	mwgs <sample_folder>

Options:
	-h --help			Show this screen.
	--version			Show version.

Examples:
	mwgs Sample_ADM1306A13_nxdual26

Help:
	For more information visit:
	https://github.com/Clinical-Genomics/mwgs
"""

from docopt import docopt
from . import __version__ as VERSION

def main():
	"Main CLI-entrypoint."
	import scripts
	options = docopt(__doc__, version=VERSION)
	for k, v in options.iteritems():
		 
main()
