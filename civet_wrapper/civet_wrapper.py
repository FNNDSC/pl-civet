#!/usr/bin/env python                                            
#
# civet_wrapper ds ChRIS plugin app
#
# (c) 2016-2019 Fetal-Neonatal Neuroimaging & Developmental Science Center
#                   Boston Children's Hospital
#
#              http://childrenshospital.org/FNNDSC/
#                        dev@babyMRI.org
#


import os
import sys
sys.path.append(os.path.dirname(__file__))

# import the Chris app superclass
from chrisapp.base import ChrisApp


Gstr_title = """
 _____ _____ _   _ _____ _____ 
/  __ \_   _| | | |  ___|_   _|
| /  \/ | | | | | | |__   | |  
| |     | | | | | |  __|  | |  
| \__/\_| |_\ \_/ / |___  | |  
 \____/\___/ \___/\____/  \_/  
                               
"""

Gstr_synopsis = """

(Edit this in-line help for app specifics. At a minimum, the 
flags below are supported -- in the case of DS apps, both
positional arguments <inputDir> and <outputDir>; for FS apps
only <outputDir> -- and similarly for <in> <out> directories
where necessary.)

    NAME

       civet_wrapper.py 

    SYNOPSIS

        python civet_wrapper.py                                         \\
            [-h] [--help]                                               \\
            [--json]                                                    \\
            [--man]                                                     \\
            [--meta]                                                    \\
            [--savejson <DIR>]                                          \\
            [-v <level>] [--verbosity <level>]                          \\
            --args <CLI_ARGS>                                           \\
            [--version]                                                 \\
            <inputDir>                                                  \\
            <outputDir> 

    BRIEF EXAMPLE

        * Bare bones execution
        
            mkdir input
            cp t1.mnc input/00100_t1.mnc
            python civet_wrapper.py --args "-N3-distance 200 -lsq12 -resample-surfaces -thickness tlaplace:tfs:tlink 30:20 -VBM -combine-surface -spawn -run 00100" source/  output/

    DESCRIPTION

        `civet_wrapper.py` ...

    ARGS

        [-h] [--help]
        If specified, show help message and exit.
        
        [--json]
        If specified, show json representation of app and exit.
        
        [--man]
        If specified, print (this) man page and exit.

        [--meta]
        If specified, print plugin meta data and exit.
        
        [--savejson <DIR>] 
        If specified, save json representation file to DIR and exit. 
        
        [-v <level>] [--verbosity <level>]
        Verbosity level for app. Not used currently.
        
        [--version]
        If specified, print version number and exit. 

"""

script = '/opt/CIVET/Linux-x86_64/CIVET-2.1.1/CIVET_Processing_Pipeline'

class Civet(ChrisApp):
    """
    CIVET is an image processing pipeline for fully automated volumetric, corticometric, and morphometric analysis of human brain imaging data (MRI)..
    """
    AUTHORS                 = 'Jennings Zhang (Jennings.Zhang@childrens.harvard.edu)'
    SELFPATH                = os.path.dirname(os.path.abspath(__file__))
    SELFEXEC                = os.path.basename(__file__)
    EXECSHELL               = 'python3'
    TITLE                   = 'CIVET Pipeline'
    CATEGORY                = ''
    TYPE                    = 'ds'
    DESCRIPTION             = 'CIVET is an image processing pipeline for fully automated volumetric, corticometric, and morphometric analysis of human brain imaging data (MRI).'
    DOCUMENTATION           = 'http://www.bic.mni.mcgill.ca/ServicesSoftware/CIVET-2-1-0-Table-of-Contents'
    VERSION                 = '2.1.1'
    ICON                    = '' # url of an icon image
    LICENSE                 = 'Civet core'
    MAX_NUMBER_OF_WORKERS   = 1  # Override with integer value
    MIN_NUMBER_OF_WORKERS   = 1  # Override with integer value
    MAX_CPU_LIMIT           = '' # Override with millicore value as string, e.g. '2000m'
    MIN_CPU_LIMIT           = '' # Override with millicore value as string, e.g. '2000m'
    MAX_MEMORY_LIMIT        = '' # Override with string, e.g. '1Gi', '2000Mi'
    MIN_MEMORY_LIMIT        = '' # Override with string, e.g. '1Gi', '2000Mi'
    MIN_GPU_LIMIT           = 0  # Override with the minimum number of GPUs, as an integer, for your plugin
    MAX_GPU_LIMIT           = 0  # Override with the maximum number of GPUs, as an integer, for your plugin

    # Use this dictionary structure to provide key-value output descriptive information
    # that may be useful for the next downstream plugin. For example:
    #
    # {
    #   "finalOutputFile":  "final/file.out",
    #   "viewer":           "genericTextViewer",
    # }
    #
    # The above dictionary is saved when plugin is called with a ``--saveoutputmeta``
    # flag. Note also that all file paths are relative to the system specified
    # output directory.
    OUTPUT_META_DICT = {}

    def define_parameters(self):
        """
        Define the CLI arguments accepted by this plugin app.
        Use self.add_argument to specify a new app argument.
        """
        self.add_argument('--args',
                   dest         = 'cli_args',
                   type         = str,
                   optional     = False,
                   help         = 'CLI arguments to pass to CIVET_Processing_Pipeline')
        

    def run(self, options):
        """
        Define the code to be run by this plugin app.
        """
        print(Gstr_title)
        print('Version: %s' % self.get_version())

        folders = '-sourcedir ' + options.inputdir
        folders += ' -targetdir ' + options.outputdir
        # note: sourcedir must come first
        os.system(f'{script} {folders} {options.cli_args}')

    def show_man_page(self):
        """
        Print the app's man page.
        """
        os.system(script + ' -help')


# ENTRYPOINT
if __name__ == "__main__":
    chris_app = Civet()
    chris_app.launch()
