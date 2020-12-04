pl-civet
================================

.. image:: https://badge.fury.io/py/pl-civet.svg
    :target: https://badge.fury.io/py/pl-civet

.. image:: https://travis-ci.org/FNNDSC/pl-civet.svg?branch=master
    :target: https://travis-ci.org/FNNDSC/pl-civet

.. image:: https://img.shields.io/badge/python-3.5%2B-blue.svg
    :target: https://badge.fury.io/py/pl-civet

.. contents:: Table of Contents


Abstract
--------

CIVET is an image processing pipeline for fully automated
volumetric, corticometric, and morphometric analysis
of human brain imaging data (MRI).

http://www.bic.mni.mcgill.ca/ServicesSoftware/CIVET-2-1-0-Introduction

Synopsis
--------

.. code::

    civet_wrapper                                                   \
        [-v <level>] [--verbosity <level>]                          \
        [--version]                                                 \
        [--man]                                                     \
        [--meta]                                                    \
        <inputDir>
        <outputDir> 

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

Run
----

This ``plugin`` can only run as a containerized docker image.


Using ``docker run``
~~~~~~~~~~~~~~~~~~~~

To run using ``docker``, be sure to assign an "input" directory to ``/incoming`` and an output directory to ``/outgoing``. *Make sure that the* ``$(pwd)/out`` *directory is world writable!*

Now, prefix all calls with 

.. code:: bash

    docker run --rm -v $PWD/in:incoming -v $PWD/out:/outgoing fnndsc/pl-civet:2.1.1 civet_wrapper

Thus, getting inline help is:

.. code:: bash

    docker run --rm fnndsc/pl-civet:2.1.1 civet_wrapper --man

Examples
--------

.. code:: bash

    docker run --rm -v $PWD/in:/incoming -v $PWD/out:/outgoing fnndsc/pl-civet:2.1.1 civet_wrapper -N3-distance 200 -lsq12 -resample-surfaces -thickness tlaplace:tfs:tlink 30:20 -VBM -combine-surface -spawn -run /incoming /outgoing

Development
-----------

.. code:: bash

    docker build -t fnndsc/pl-civet .

To learn about cross-platform and multi-architecture builds, see
https://github.com/FNNDSC/ubuntu-python3/blob/master/README.md#build

Testing
=======

.. code:: bash

    docker run --rm -w /usr/local/src --entrypoint /usr/bin/python3 fnndsc/pl-civet -m unittest
