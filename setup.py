
import sys
import os


# Make sure we are running python3.5+
if 10 * sys.version_info[0] + sys.version_info[1] < 35:
    sys.exit("Sorry, only Python 3.5+ is supported.")


from setuptools import setup


def readme():
    print("Current dir = %s" % os.getcwd())
    print(os.listdir())
    with open('README.rst') as f:
        return f.read()

setup(
      name             =   'civet_wrapper',
      # for best practices make this version the same as the VERSION class variable
      # defined in your ChrisApp-derived Python class
      version          =   '2.1.1',
      description      =   'CIVET is an image processing pipeline for fully automated volumetric, corticometric, and morphometric analysis of human brain imaging data (MRI).',
      long_description =   readme(),
      author           =   'Jennings Zhang',
      author_email     =   'Jennings.Zhang@childrens.harvard.edu',
      url              =   'http://www.bic.mni.mcgill.ca/ServicesSoftware/CIVET-2-1-0-Table-of-Contents',
      packages         =   ['civet_wrapper'],
      install_requires =   ['chrisapp', 'pudb'],
      test_suite       =   'nose.collector',
      tests_require    =   ['nose'],
      scripts          =   ['civet_wrapper/civet_wrapper.py'],
      license          =   'MIT',
      zip_safe         =   False
     )
