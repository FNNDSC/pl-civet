from chrisapp.base import ChrisApp


class CustomArgsApp(ChrisApp):
    DESCRIPTION = ''
    TYPE = ''
    TITLE = ''
    LICENSE = ''
    SELFPATH = ''
    SELFEXEC = ''
    EXECSHELL = ''
    OUTPUT_META_DICT = ''
    AUTHORS = ''
    VERSION = ''
    def add_argument_c(self, flag, type=str, optional=True, default='', metavar='', *args, **kwargs):
        """
        Same as self.add_argument, but with some boring defaults
        """
        if not metavar:
            metavar = flag[1].upper()
        metavar = f'<{metavar}>'
        self.add_argument(flag,
                          dest=flag,
                          type=type,
                          default=default,
                          optional=optional,
                          metavar=metavar,
                          *args, **kwargs)
        # don't repeat these options
        if flag not in ['-sourcedir', '-targetdir']:
            self.civet_options.append(flag)

    def add_argless(self, flag, *args, **kwargs):
        """
        Same as self.add_argument_c, intended for boolean CLI options that
        do not need input.
        """
        self.add_argument(flag,
                          dest=flag,
                          type=bool,
                          action='store_true',
                          default=False,
                          optional=True,
                          *args, **kwargs)
        self.civet_options.append(flag)


def add_civet_arguments(p: CustomArgsApp):
    # -- Execution control -----------------------------------------------------------
    p.add_argless('-spawn',
                  help='Use the perl system interface to spawn jobs [default: use local host scheduler DEFAULT]')
    p.add_argument_c('-queue', metavar='queue',
                     help='Which queue to use')
    p.add_argument_c('-hosts', metavar='hosts',
                     help='Colon separated list of hosts')
    p.add_argument_c('-qopts', metavar='opts',
                     help='Extra options to queuing system')
    p.add_argless('-no-granular',
                  help='Granularity level for submission of jobs using queueing system. [default]')
    p.add_argless('-granular',
                  help='opposite of -no-granular')
    p.add_argument_c('-maxqueued', metavar='val',
                     help='Maximum number of jobs that can be submitted at once. [default: 10000]')
    p.add_argless('-mpi',
                  help='Submit jobs using mpirun to fill all processors on core.')
    p.add_argless('-no-mpi',
                  help='opposite of -mpi [default]')
    # -- File options ----------------------------------------------------------------
    p.add_argument_c('-sourcedir', metavar='dir',
                     help='Directory containing the source files.')
    p.add_argument_c('-targetdir', metavar='dir',
                     help='Directory where processed data will be placed.')
    p.add_argument_c('-prefix', metavar='prefix',
                     help='File prefix to be used in naming output files.')
    p.add_argless('-id-subdir',
                  help='Indicate that the source directory contains sub-directories for each id')

    p.add_argument_c('-id-file', metavar='file',
                     help='A text file that contains all the subject id\'s (separated by space, tab, return or comma) that CIVET will run on.')
    # -- Pipeline options ------------------------------------------------------------
    p.add_argument_c('-template', metavar='val',
                     help='Define the template for image processing in stereotaxic space (0.50, 0.75, 1.00, 1.50, 2.00, 3.00, 4.00, 6.00). [default: 1.00]')
    p.add_argument_c('-model', metavar='model',
                     help='Define the model for image-processing: "colin27" (MNI Colin27 asymmetric (2009)), "icbm152nl_09s" (MNI ICBM152 non-linear symmetric (2009a)), "icbm152nl" (MNI ICBM152 non-linear 6th generation), "icbm152lin" (MNI ICBM152 linear), "ibis-v24" (MNI IBIS 24 months, symmetric (2015)), "ADNIhires" (MNI ADNI non-linear hi-res sym 0.5mm)  [default: icbm152nl_09s]')
    p.add_argument_c('-surfreg-model', metavar='model',
                     help='Define the model for surface registration: "icbm152MCsym" (ICBM152, marching-cubes, symmetric (2014)), "colinMCasym" (Colin, marching-cubes, asymmetric (2014)), "samirMCasym" (IBIS Phantom (Samir), marching-cubes, asymmetric (2014))')
    p.add_argument_c('-surface-atlas', metavar='model',
                     help='Define the atlas for surface parcellation: "lobes" (coarse lobar parcellation, symmetric), "AAL" (AAL parcellation, asymmetric, based on Colin brain), "DKT" (DKT-40 parcellation, asymmetric) [default: lobes]')
    # -- CIVET options ---------------------------------------------------------------
    p.add_argless('-input_is_stx',
                  help='Assume that the input volume is already linearly regsieted to stx space; this skips the linear registration steps')
    p.add_argless('-noinput_is_stx',
                  help='opposite of -input_is_stx [default]')
    p.add_argless('-multispectral',
                  help='Use T1, T2 and PD native files for tissue classification.')
    p.add_argless('-correct-pve',
                  help='Apply correction to the mean and variance of tissue types at pve iterations. [default]')
    p.add_argless('-no-correct-pve',
                  help='opposite of -correct-pve')
    p.add_argless('-mask-cerebellum',
                  help='mask cerebellum and brainstem from pve classification [default]')
    p.add_argless('-no-mask-cerebellum',
                  help='opposite of -mask-cerebellum')
    p.add_argless('-subcortical',
                  help='create a sub-cortical SC class in pve classification [default]')
    p.add_argless('-no-subcortical',
                  help='opposite of -subcortical')
    p.add_argless('-calibrate-white',
                  help='Apply gradient intensity correction for calibration of white surface. [default]')
    p.add_argless('-no-calibrate-white',
                  help='opposite of -calibrate-white')
    p.add_argless('-spectral_mask',
                  help='Use T1, T2 and PD stereotaxic files for brain masking.')
    p.add_argument_c('-interp', metavar='method',
                     help='Interpolation method from native to stereotaxic space ("trilinear", "tricubic", "sinc") [default: trilinear]')
    p.add_argument_c('-headheight', metavar='dist',
                     help='head height in mm for neck cropping (use 0 for none). [default: 175]')
    p.add_argument_c('-N3-distance', metavar='dist',
                     help='N3 spline distance in mm (suggested values: 200 for 1.5T scan; 50 for 3T scan).')
    p.add_argument_c('-N3-damping', metavar='lambda',
                     help='N3 damping coefficient (lambda) (suggested values: 2.0e-06). [default: 2.0e-06]')
    p.add_argless('-lsq6',
                  help='use 6-parameter transformation for linear registration [default -lsq9]')
    p.add_argless('-lsq12',
                  help='use 12-parameter transformation for linear registration [default -lsq9]')
    p.add_argless('-no-surfaces',
                  help='don\'t build surfaces')
    p.add_argless('-hi-res-surfaces',
                  help='build high resolution surfaces')
    p.add_argless('-mask-blood-vessels',
                  help='mask blood vessels prior to white surface extraction')
    p.add_argless('-no-mask-blood-vessel',
                  help='opposite of -mask-blood-vessels [default]')
    p.add_argless('-mask-hippocampus',
                  help='mask hippocampus and amygdala for surface extraction if model supports it [default]')
    p.add_argless('-no-mask-hippocampus',
                  help='opposite of -mask-hippocampus')
    p.add_argument_c('-thickness',
                     nargs=2, metavar='T:T:T N:N',
                     help='compute cortical thickness and blur [tlink][:tlaplace][:tfs] [fwhm1][:fwhm2]:...[:fwhmN] kernel sizes in mm [default: tlink 30]')
    p.add_argless('-resample-surfaces',
                  help='resample cortical surfaces')
    p.add_argless('-no-resample-surfaces',
                  help='opposite of -resample-surfaces [default]')
    p.add_argless('-mean-curvature',
                  help='produce mean curvature maps on surfaces')
    p.add_argless('-no-mean-curvature',
                  help='opposite of -mean-curvature [default]')
    p.add_argument_c('-area-fwhm', metavar='fwhm',
                     help='fwhm1:fwhm2:...:fwhmn blurring kernel sizes in mm for resampled surface areas [default: 40]')
    p.add_argument_c('-volume-fwhm', metavar='fwhm',
                     help='fwhm1:fwhm2:...:fwhmn blurring kernel sizes in mm for resampled surface volumes [default: 40]')
    p.add_argless('-combine-surfaces',
                  help='combine left and right cortical surfaces')
    p.add_argless('-no-combine-surfaces',
                  help='opposite of -combine-surfaces [default]')
    # -- VBM options -----------------------------------------------------------------
    p.add_argless('-VBM',
                  help='process VBM files for analysis [default -no-VBM]')
    p.add_argless('-no-VBM',
                  help='don\'t process VBM files for analysis')
    p.add_argument_c('-VBM-fwhm', metavar='fwhm',
                     help='blurring kernel size in mm for volume [default: 8]')
    p.add_argless('-VBM-symmetry',
                  help='run symmetry tools [default -no-VBM-symmetry]')
    p.add_argless('-no-VBM-symmetry',
                  help='don\'t run symmetry tools')
    p.add_argless('-VBM-cerebellum',
                  help='keep cerebellum in VBM maps')
    p.add_argless('-no-VBM-cerebellum',
                  help='mask out cerebellum in VBM maps [default -VBM-cerebellum]')
    # -- ANIMAL options --------------------------------------------------------------
    p.add_argless('-animal',
                  help='run volumetric ANIMAL segmentation [default -no-animal]')
    p.add_argless('-no-animal',
                  help='don\'t run volumetric ANIMAL segmentation')
    p.add_argument_c('-lobe_atlas', metavar='model',
                     help='Use lobe atlas for ANIMAL segmentation (mandatory with -animal): "icbm152nl-VI" (ICBM152 generation VI symmetric model), "icbm152nl-2009a" (ICBM152 2009a symmetric model)')
    # -- Pipeline control ------------------------------------------------------------
    p.add_argless('-run',
                  help='Run the pipeline.')
    p.add_argless('-status-from-files',
                  help='Compute pipeline status from files')
    p.add_argless('-print-stages',
                  help='Print the pipeline stages.')
    p.add_argless('-print-status',
                  help='Print the status of each pipeline.')
    p.add_argless('-make-graph',
                  help='Create dot graph file.')
    p.add_argless('-make-filename-graph',
                  help='Create dot graph of filenames.')
    p.add_argless('-print-status-report',
                  help='Writes a CSV status report to file in cwd.')
    # -- Stage Control ---------------------------------------------------------------
    p.add_argless('-reset-all',
                  help='Start the pipeline from the beginning.')
    p.add_argument_c('-reset-from', metavar='stage_name',
                     help='Restart from the specified stage.')
    p.add_argument_c('-reset-after', metavar='stage_name',
                     help='Restart after the specified stage.')
    p.add_argument_c('-reset-to', metavar='stage_name',
                     help='Run up to and including the specified stage.')
    p.add_argless('-reset-running',
                  help='Restart currently running jobs. [default]')
    p.add_argless('-no-reset-running',
                  help='opposite of -reset-running')
