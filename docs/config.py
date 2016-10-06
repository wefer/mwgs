from os import getenv
import sys

try:
  import set_environ
except:
  pass

LIMS_URI = getenv('LIMS_URI')
LIMS_USER = getenv('LIMS_USER')
LIMS_PASSWORD = getenv('LIMS_PASSWORD')
ENTREZ_EMAIL = getenv('ENTREZ_EMAIL')


#System specific constants
if getenv('HOSTNAME') == 'rastapopoulos.scilifelab.se':
  REF_FOLDER = '/mnt/hds/proj/bioinfo/MICROBIAL/REFERENCES/'
  PICARD_JAR = '/mnt/hds/proj/bioinfo/MICROBIAL/picard-tools-1.141/picard.jar'
  JAVA = '/mnt/hds/proj/bioinfo/mip/modules/jre1.7.0_45/bin/java'
else:
  REF_FOLDER = '/home/hugo/MWGS/REFERENCES/'
  PICARD_JAR = '/home/hugo/picard-tools-1.141/picard.jar'
  JAVA = 'java'
