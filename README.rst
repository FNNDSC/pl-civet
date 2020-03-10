pl-civet
================================

.. image:: https://badge.fury.io/py/civet_wrapper.svg
    :target: https://badge.fury.io/py/civet_wrapper

.. image:: https://travis-ci.org/FNNDSC/civet_wrapper.svg?branch=master
    :target: https://travis-ci.org/FNNDSC/civet_wrapper

.. image:: https://img.shields.io/badge/python-3.5%2B-blue.svg
    :target: https://badge.fury.io/py/pl-civet_wrapper

.. contents:: Table of Contents


Abstract
--------

CIVET is an image processing pipeline for fully automated volumetric, corticometric, and morphometric analysis of human brain imaging data (MRI).


Synopsis
--------

.. code::

    python civet_wrapper.py                                           \
        [-v <level>] [--verbosity <level>]                          \
        [--version]                                                 \
        [--man]                                                     \
        [--meta]                                                    \
        <inputDir>
        <outputDir> 

Description
-----------

``civet_wrapper.py`` is a ChRIS-based application that...

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

This ``plugin`` can be run in two modes: natively as a python package or as a containerized docker image.

Using PyPI
~~~~~~~~~~

To run from PyPI, simply do a 

.. code:: bash

    pip install civet_wrapper

and run with

.. code:: bash

    civet_wrapper.py --man /tmp /tmp

to get inline help. The app should also understand being called with only two positional arguments

.. code:: bash

    civet_wrapper.py /some/input/directory /destination/directory


Using ``docker run``
~~~~~~~~~~~~~~~~~~~~

To run using ``docker``, be sure to assign an "input" directory to ``/incoming`` and an output directory to ``/outgoing``. *Make sure that the* ``$(pwd)/out`` *directory is world writable!*

Now, prefix all calls with 

.. code:: bash

    docker run --rm -v $(pwd)/out:/outgoing                             \
            fnndsc/pl-civet_wrapper civet_wrapper.py                        \

Thus, getting inline help is:

.. code:: bash

    mkdir in out && chmod 777 out
    docker run --rm -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing      \
            fnndsc/pl-civet_wrapper civet_wrapper.py                        \
            --man                                                       \
            /incoming /outgoing

Examples
--------





