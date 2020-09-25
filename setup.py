from os import path
from setuptools import setup

with open(path.join(path.abspath(path.dirname(__file__)), 'README.rst')) as f:
    readme = f.read()

setup(
    name             = 'civet_wrapper',
    version          = '2.1.1.2',
    description      = 'CIVET is an image processing pipeline for fully automated volumetric, corticometric, and morphometric analysis of human brain imaging data (MRI).',
    long_description = readme,
    author           = 'Jennings Zhang',
    author_email     = 'Jennings.Zhang@childrens.harvard.edu',
    url              = 'http://www.bic.mni.mcgill.ca/ServicesSoftware/CIVET-2-1-0-Table-of-Contents',
    packages         = ['civet_wrapper'],
    install_requires = ['chrisapp==1.1.6'],
    license          = 'Civet core',
    zip_safe         = False,
    python_requires  = '>=3.6',
    entry_points     = {
    'console_scripts': [
        'civet_wrapper = civet_wrapper.__main__:main'
        ]
    }
)
