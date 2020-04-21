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

    python civet_wrapper.py                                         \
        [-v <level>] [--verbosity <level>]                          \
        [--version]                                                 \
        [--man]                                                     \
        [--meta]                                                    \
        --args <CLI_ARGS>                                           \
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


Run
----

This ``plugin`` can only run as a containerized docker image.


Using ``docker run``
~~~~~~~~~~~~~~~~~~~~

To run using ``docker``, be sure to assign an "input" directory to ``/incoming`` and an output directory to ``/outgoing``. *Make sure that the* ``$(pwd)/out`` *directory is world writable!*

Now, prefix all calls with 

.. code:: bash

    docker run --rm -v $(pwd)/out:/outgoing                           \
            fnndsc/pl-civet:2.1.1 civet_wrapper.py                    \

Thus, getting inline help is:

.. code:: bash

    mkdir in out && chmod 777 out
    docker run --rm -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing    \
            fnndsc/pl-civet:2.1.1 civet_wrapper.py                    \
            --man                                                     \
            /incoming /outgoing

Examples
--------

.. code:: bash

    docker run --rm -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing fnndsc/pl-civet:2.1.1 civet_wrapper.py -N3-distance 200 -lsq12 -resample-surfaces -thickness tlaplace:tfs:tlink 30:20 -VBM -combine-surface -spawn -run 00100 /incoming /outgoing

Development
-----------

.. code:: bash

    docker build -t fnndsc/pl-civet:2.1.1 $PWD
    # if you are on the BCH network, you need to configure the proxy
    docker build -t fnndsc/pl-civet:2.1.1 --build-arg http_proxy=http://proxy.tch.harvard.edu:3128 $PWD
