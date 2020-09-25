#!/usr/bin/env python3
#
# civet_wrapper ds ChRIS plugin app
#
# (c) 2016-2020 Fetal-Neonatal Neuroimaging & Developmental Science Center
#                   Boston Children's Hospital
#
#              http://childrenshospital.org/FNNDSC/
#                        dev@babyMRI.org
#

## Author: Jennings Zhang <Jennings.Zhang@childrens.harvard.edu>
##
## Date: 2020-04-20
##
## Purpose: A dumb Python wrapper for CIVET to work as a ChRIS plugin.
##          CLI options to pass to `CIVET_Processing_Pipeline`
##          are assembled from the data within Python's argparse
##
## Note: This wrapper does not care about checking whether
##       or not the options are legal, any validation is
##       checked at the lower level by CIVET itself.


import os
import pkg_resources

from glob import glob
from tempfile import NamedTemporaryFile

from civet_wrapper.arguments import CustomArgsApp, add_civet_arguments

Gstr_title = """
 _____ _____ _   _ _____ _____ 
/  __ \_   _| | | |  ___|_   _|
| /  \/ | | | | | | |__   | |  
| |     | | | | | |  __|  | |  
| \__/\_| |_\ \_/ / |___  | |  
 \____/\___/ \___/\____/  \_/  
                               
"""

Gstr_synopsis = """

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
            [--version]                                                 \\
            <inputDir>                                                  \\
            <outputDir> 

    BRIEF EXAMPLE

        * Bare bones execution

            mkdir input
            cp t1.mnc input/00100_t1.mnc
            python civet_wrapper.py -N3-distance 200 -lsq12              \\
                  -resample-surfaces -thickness tlaplace:tfs:tlink 30:20 \\
                  -VBM -combine-surface -spawn -run                      \\
                  input/  output/

    DESCRIPTION

        `civet_wrapper.py`
        
        A dumb Python wrapper for CIVET to work as a ChRIS plugin.
        `civet_wrapper.py` passes its CLI arguments to `CIVET_Processing_Pipeline`.
        Please scroll down to the next section for usage about CIVET itself.
        
        Limitations: scan id cannot be passed inline.
                     If -idfile is not specified, then
                     one is created with all *_t1.mnc.

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

script = os.path.join(os.environ['MNIBASEPATH'], os.environ['CIVET'], 'CIVET_Processing_Pipeline')

class Civet(CustomArgsApp):
    """
    CIVET is an image processing pipeline for fully automated volumetric,
    corticometric, and morphometric analysis of human brain imaging data (MRI).
    """
    AUTHORS                 = 'Jennings Zhang <Jennings.Zhang@childrens.harvard.edu>'
    SELFPATH                = os.path.dirname(os.path.abspath(__file__))
    SELFEXEC                = os.path.basename(__file__)
    EXECSHELL               = 'python3'
    TITLE                   = 'CIVET Pipeline'
    CATEGORY                = 'MRI Processing'
    TYPE                    = 'ds'
    DESCRIPTION             = 'CIVET is an image processing pipeline for fully automated volumetric,' \
                              'corticometric, and morphometric analysis of human brain imaging data (MRI).'
    DOCUMENTATION           = 'http://www.bic.mni.mcgill.ca/ServicesSoftware/CIVET'
    VERSION                 = pkg_resources.require('civet_wrapper')[0].version
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
    OUTPUT_META_DICT = {}  # TODO


    # keep track of all the CIVET-specific options
    civet_options = []

    def define_parameters(self):
        """
        Define the CLI arguments accepted by this plugin app.
        Use self.add_argument to specify a new app argument.
        """
        # these need to appear first in the command line call to CIVET
        self.civet_options.append('-sourcedir')
        self.civet_options.append('-targetdir')
        
        add_civet_arguments(self)

    def assemble_cli(self, options):
        # note: sourcedir must come first
        args_dict = vars(options)
        args_dict['-sourcedir'] = options.inputdir
        args_dict['-targetdir'] = options.outputdir
        
        # create an id-file if one is not provided
        if not args_dict['-id-file']:
            self.civet_options.append('-id-file')
            with NamedTemporaryFile('w', encoding='utf-8', delete=False) as tmp:
                args_dict['-id-file'] = tmp.name
                scan_files = os.path.join(options.inputdir, '*_t1.mnc')
                for scan_id in glob(scan_files):
                    scan_id = os.path.basename(scan_id)
                    scan_id = scan_id[:-len('_t1.mnc')]
                    tmp.write(scan_id)
        
        # ChRIS does not support positional arguments
        # self.add_argument requires dest
        # KeyError: "'dest' option required."
        # however specufiying dest does not make sense for positional arguments
        # ValueError: dest supplied twice for positional argument
        cli_string = []
        for option in self.civet_options:
            arg = args_dict[option]
            # print(f'{option}: "{arg}"')
            if not arg:
                continue
            if arg == True:
                cli_string.append(option)
            else:
                if isinstance(arg, list):
                    arg = ' '.join(arg)
                cli_string.append(f'{option} {arg}')
        

        return ' '.join(cli_string)

    def run(self, options):
        """
        Define the code to be run by this plugin app.
        """
        print(Gstr_title)
        print('Version: %s' % self.get_version(), flush=True)
        os.system(f'{script} {self.assemble_cli(options)}')


    def show_man_page(self):
        """
        Print the app's man page.
        """
        print(Gstr_synopsis)
        print("""
+---------------------------------------------------------------+
|                                                               |
|                         CIVET Options                         |
|                                                               |
+---------------------------------------------------------------+
        """, flush=True)
        os.system(script + ' -help')
