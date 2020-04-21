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
                  -VBM -combine-surface -spawn -run 00100                \\
                  input/  output/

    DESCRIPTION

        `civet_wrapper.py`
        
        A dumb Python wrapper for CIVET to work as a ChRIS plugin.
        `civet_wrapper.py` passes its CLI arguments to `CIVET_Processing_Pipeline`.
        Please scroll down to the next section for usage about CIVET itself.

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
    CIVET is an image processing pipeline for fully automated volumetric, corticometric, and morphometric analysis of human brain imaging data (MRI).
    """
    AUTHORS                 = 'Jennings Zhang (Jennings.Zhang@childrens.harvard.edu)'
    SELFPATH                = os.path.dirname(os.path.abspath(__file__))
    SELFEXEC                = os.path.basename(__file__)
    EXECSHELL               = 'python3'
    TITLE                   = 'CIVET Pipeline'
    CATEGORY                = 'MRI Processing'
    TYPE                    = 'ds'
    DESCRIPTION             = 'CIVET is an image processing pipeline for fully automated volumetric, corticometric, and morphometric analysis of human brain imaging data (MRI).'
    DOCUMENTATION           = 'http://www.bic.mni.mcgill.ca/ServicesSoftware/CIVET'
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


    # keep track of all the CIVET-specific options
    civet_options = []
    
    # trying to redefine inherited method results in
    # TypeError: 'Civet' object does not support indexing
    def add_argument_c(self, flag, type = str, optional = True, default = '', metavar = '', *args, **kwargs):
        """
        Same as self.add_argument, but with some boring defaults
        """
        if not metavar:
            metavar = flag[1].upper()
        metavar = f'<{metavar}>'
        self.add_argument(flag,
                    dest         = flag,
                    type         = type,
                    default      = default,
                    optional     = optional,
                    metavar      = metavar,
                    *args, **kwargs)
        # don't repeat these options
        if flag not in ['-sourcedir', '-targetdir']:
            self.civet_options.append(flag)

    def add_argless(self, flag, help):
        """
        Same as self.add_argument_c, intended for boolean CLI options that
        do not need input.
        """
        self.add_argument(flag,
                    dest = flag,
                    type = bool,
                    action = 'store_true',
                    default = False,
                    optional = True)
        self.civet_options.append(flag)

    def define_parameters(self):
        """
        Define the CLI arguments accepted by this plugin app.
        Use self.add_argument to specify a new app argument.
        """
        # these need to appear first in the command line call to CIVET
        self.civet_options.append('-sourcedir')
        self.civet_options.append('-targetdir')
        
        # -- Execution control -----------------------------------------------------------
        self.add_argless('-spawn',
            help = 'Use the perl system interface to spawn jobs [default: use local host scheduler DEFAULT]')
        self.add_argument_c('-queue', metavar='queue',
            help = 'Which queue to use')
        self.add_argument_c('-hosts', metavar='hosts',
            help = 'Colon separated list of hosts')
        self.add_argument_c('-qopts', metavar='opts',
            help = 'Extra options to queuing system')
        self.add_argless('-no-granular',
            help = 'Granularity level for submission of jobs using queueing system. [default]')
        self.add_argless('-granular',
            help = 'opposite of -no-granular')
        self.add_argument_c('-maxqueued', metavar='val',
            help = 'Maximum number of jobs that can be submitted at once. [default: 10000]')
        self.add_argless('-mpi',
            help = 'Submit jobs using mpirun to fill all processors on core.')
        self.add_argless('-no-mpi',
            help = 'opposite of -mpi [default]')
        # -- File options ----------------------------------------------------------------
        self.add_argument_c('-sourcedir', metavar='dir',
            help = 'Directory containing the source files.')
        self.add_argument_c('-targetdir', metavar='dir',
            help = 'Directory where processed data will be placed.')
        self.add_argument_c('-prefix', metavar='prefix',
            help = 'File prefix to be used in naming output files.')
        self.add_argless('-id-subdir',
            help = 'Indicate that the source directory contains sub-directories for each id')
        
        self.add_argument_c('-id-file', metavar='file',
            help = 'A text file that contains all the subject id\'s (separated by space, tab, return or comma) that CIVET will run on.')
        # -- Pipeline options ------------------------------------------------------------
        self.add_argument_c('-template', metavar='val',
            help = 'Define the template for image processing in stereotaxic space (0.50, 0.75, 1.00, 1.50, 2.00, 3.00, 4.00, 6.00). [default: 1.00]')
        self.add_argument_c('-model', metavar='model',
            help = 'Define the model for image-processing: "colin27" (MNI Colin27 asymmetric (2009)), "icbm152nl_09s" (MNI ICBM152 non-linear symmetric (2009a)), "icbm152nl" (MNI ICBM152 non-linear 6th generation), "icbm152lin" (MNI ICBM152 linear), "ibis-v24" (MNI IBIS 24 months, symmetric (2015)), "ADNIhires" (MNI ADNI non-linear hi-res sym 0.5mm)  [default: icbm152nl_09s]')
        self.add_argument_c('-surfreg-model', metavar='model',
            help = 'Define the model for surface registration: "icbm152MCsym" (ICBM152, marching-cubes, symmetric (2014)), "colinMCasym" (Colin, marching-cubes, asymmetric (2014)), "samirMCasym" (IBIS Phantom (Samir), marching-cubes, asymmetric (2014))')
        self.add_argument_c('-surface-atlas', metavar='model',
            help = 'Define the atlas for surface parcellation: "lobes" (coarse lobar parcellation, symmetric), "AAL" (AAL parcellation, asymmetric, based on Colin brain), "DKT" (DKT-40 parcellation, asymmetric) [default: lobes]')
        # -- CIVET options ---------------------------------------------------------------
        self.add_argless('-input_is_stx',
            help = 'Assume that the input volume is already linearly regsieted to stx space; this skips the linear registration steps')
        self.add_argless('-noinput_is_stx',
            help = 'opposite of -input_is_stx [default]')
        self.add_argless('-multispectral',
            help = 'Use T1, T2 and PD native files for tissue classification.')
        self.add_argless('-correct-pve',
            help = 'Apply correction to the mean and variance of tissue types at pve iterations. [default]')
        self.add_argless('-no-correct-pve',
            help = 'opposite of -correct-pve')
        self.add_argless('-mask-cerebellum',
            help = 'mask cerebellum and brainstem from pve classification [default]')
        self.add_argless('-no-mask-cerebellum',
            help = 'opposite of -mask-cerebellum')
        self.add_argless('-subcortical',
            help = 'create a sub-cortical SC class in pve classification [default]')
        self.add_argless('-no-subcortical',
            help = 'opposite of -subcortical')
        self.add_argless('-calibrate-white',
            help = 'Apply gradient intensity correction for calibration of white surface. [default]')
        self.add_argless('-no-calibrate-white',
            help = 'opposite of -calibrate-white')
        self.add_argless('-spectral_mask',
            help = 'Use T1, T2 and PD stereotaxic files for brain masking.')
        self.add_argument_c('-interp', metavar='method',
            help = 'Interpolation method from native to stereotaxic space ("trilinear", "tricubic", "sinc") [default: trilinear]')
        self.add_argument_c('-headheight', metavar='dist',
            help = 'head height in mm for neck cropping (use 0 for none). [default: 175]')
        self.add_argument_c('-N3-distance', metavar='dist',
            help = 'N3 spline distance in mm (suggested values: 200 for 1.5T scan; 50 for 3T scan).')
        self.add_argument_c('-N3-damping', metavar='lambda',
            help = 'N3 damping coefficient (lambda) (suggested values: 2.0e-06). [default: 2.0e-06]')
        self.add_argless('-lsq6',
            help = 'use 6-parameter transformation for linear registration [default -lsq9]')
        self.add_argless('-lsq12',
            help = 'use 12-parameter transformation for linear registration [default -lsq9]')
        self.add_argless('-no-surfaces',
            help = 'don\'t build surfaces')
        self.add_argless('-hi-res-surfaces',
            help = 'build high resolution surfaces')
        self.add_argless('-mask-blood-vessels',
            help = 'mask blood vessels prior to white surface extraction')
        self.add_argless('-no-mask-blood-vessel',
            help = 'opposite of -mask-blood-vessels [default]')
        self.add_argless('-mask-hippocampus',
            help = 'mask hippocampus and amygdala for surface extraction if model supports it [default]')
        self.add_argless('-no-mask-hippocampus',
            help = 'opposite of -mask-hippocampus')
        self.add_argument_c('-thickness',
            nargs=2, metavar='T:T:T N:N',
            help = 'compute cortical thickness and blur [tlink][:tlaplace][:tfs] [fwhm1][:fwhm2]:...[:fwhmN] kernel sizes in mm [default: tlink 30]')
        self.add_argless('-resample-surfaces',
            help = 'resample cortical surfaces')
        self.add_argless('-no-resample-surfaces',
            help = 'opposite of -resample-surfaces [default]')
        self.add_argless('-mean-curvature',
            help = 'produce mean curvature maps on surfaces')
        self.add_argless('-no-mean-curvature',
            help = 'opposite of -mean-curvature [default]')
        self.add_argument_c('-area-fwhm', metavar='fwhm',
            help = 'fwhm1:fwhm2:...:fwhmn blurring kernel sizes in mm for resampled surface areas [default: 40]')
        self.add_argument_c('-volume-fwhm', metavar='fwhm',
            help = 'fwhm1:fwhm2:...:fwhmn blurring kernel sizes in mm for resampled surface volumes [default: 40]')
        self.add_argless('-combine-surfaces',
            help = 'combine left and right cortical surfaces')
        self.add_argless('-no-combine-surfaces',
            help = 'opposite of -combine-surfaces [default]')
        # -- VBM options -----------------------------------------------------------------
        self.add_argless('-VBM',
            help = 'process VBM files for analysis [default -no-VBM]')
        self.add_argless('-no-VBM',
            help = 'don\'t process VBM files for analysis')
        self.add_argument_c('-VBM-fwhm', metavar='fwhm',
            help = 'blurring kernel size in mm for volume [default: 8]')
        self.add_argless('-VBM-symmetry',
            help = 'run symmetry tools [default -no-VBM-symmetry]')
        self.add_argless('-no-VBM-symmetry',
            help = 'don\'t run symmetry tools')
        self.add_argless('-VBM-cerebellum',
            help = 'keep cerebellum in VBM maps')
        self.add_argless('-no-VBM-cerebellum',
            help = 'mask out cerebellum in VBM maps [default -VBM-cerebellum]')
        # -- ANIMAL options --------------------------------------------------------------
        self.add_argless('-animal',
            help = 'run volumetric ANIMAL segmentation [default -no-animal]')
        self.add_argless('-no-animal',
            help = 'don\'t run volumetric ANIMAL segmentation')
        self.add_argument_c('-lobe_atlas', metavar='model',
            help = 'Use lobe atlas for ANIMAL segmentation (mandatory with -animal): "icbm152nl-VI" (ICBM152 generation VI symmetric model), "icbm152nl-2009a" (ICBM152 2009a symmetric model)')
        # -- Pipeline control ------------------------------------------------------------
        self.add_argless('-run',
            help = 'Run the pipeline.')
        self.add_argless('-status-from-files',
            help = 'Compute pipeline status from files')
        self.add_argless('-print-stages',
            help = 'Print the pipeline stages.')
        self.add_argless('-print-status',
            help = 'Print the status of each pipeline.')
        self.add_argless('-make-graph',
            help = 'Create dot graph file.')
        self.add_argless('-make-filename-graph',
            help = 'Create dot graph of filenames.')
        self.add_argless('-print-status-report',
            help = 'Writes a CSV status report to file in cwd.')
        # -- Stage Control ---------------------------------------------------------------
        self.add_argless('-reset-all',
            help = 'Start the pipeline from the beginning.')
        self.add_argument_c('-reset-from', metavar='stage_name',
            help = 'Restart from the specified stage.')
        self.add_argument_c('-reset-after', metavar='stage_name',
            help = 'Restart after the specified stage.')
        self.add_argument_c('-reset-to', metavar='stage_name',
            help = 'Run up to and including the specified stage.')
        self.add_argless('-reset-running',
            help = 'Restart currently running jobs. [default]')
        self.add_argless('-no-reset-running',
            help = 'opposite of -reset-running')        
        

    def assemble_cli(self, options):
        # note: sourcedir must come first
        args_dict = vars(options)
        args_dict['-sourcedir'] = options.inputdir
        args_dict['-targetdir'] = options.outputdir
        
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
        print('Version: %s' % self.get_version())
        print(f'{script} {self.assemble_cli(options)}')


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
        print('end of help')


# ENTRYPOINT
if __name__ == "__main__":
    chris_app = Civet()
    chris_app.launch()
