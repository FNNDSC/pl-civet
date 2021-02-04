pl-civet
================================

.. image:: https://github.com/FNNDSC/pl-civet/workflows/CI/badge.svg
    :target: https://github.com/FNNDSC/pl-civet/actions

.. image:: https://raw.githubusercontent.com/FNNDSC/cookiecutter-chrisapp/master/doc/assets/badge/light.png
    :target: https://chrisstore.co/plugin/2


.. contents:: Table of Contents


Abstract
--------

CIVET is an image processing pipeline for fully automated
volumetric, corticometric, and morphometric analysis
of human brain imaging data (MRI).

http://www.bic.mni.mcgill.ca/ServicesSoftware/CIVET-2-1-0-Introduction

Description
-----------

``civet_wrapper.py`` is a ChRIS-based application that
runs the CIVET MRI processing pipeline.

Agruments
---------

.. code::

    [-v <level>] [--verbosity <level>]
    Verbosity level for app. Not used currently.

    [--version]
    If specified, print version number. 
    
    [--man]
    If specified, print (this) man page.

    [--meta]
    If specified, print plugin meta data.

Input Files
~~~~~~~~~~~

If ``-id-file`` is not given, then ``civet_wrapper.py`` will attempt to
locate all your input files in the specified input directory.
*ChRIS* does not support positional arguments (besides *inputDir* and *outputDir*).
This is different from running the ``CIVET_Processing_Pipeline`` directly, where
you are able to give subject IDs (input file prefixes) as positional arguments.

tl;dr for inputs ``incoming/*_t1.mnc``, don't specify file names via command line.

Example
-------

.. code:: bash

    docker run --rm -v $PWD/in:/incoming -v $PWD/out:/outgoing fnndsc/pl-civet:2.1.1 civet_wrapper -N3-distance 200 -lsq12 -resample-surfaces -thickness tlaplace:tfs:tlink 30:20 -VBM -combine-surface -spawn -run /incoming /outgoing

Development
-----------

.. code:: bash

    docker build -t fnndsc/pl-civet .

To learn about cross-platform and multi-architecture builds, see
https://github.com/FNNDSC/cookiecutter-chrisapp/wiki/Multi-Architectural-Images#manifest-list

Testing
=======

.. code:: bash

    docker run --rm -w /usr/local/src --entrypoint /usr/bin/python3 fnndsc/pl-civet -m unittest
