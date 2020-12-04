#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Jennings Zhang <Jennings.Zhang@childrens.harvard.edu>

Purpose: parse output of `CIVET_Processing_Pipeline -help` to generate
         Python argparse-like code for pl-civet, a Python wrapper for CIVET

Usage:
        CIVET_Processing_Pipeline -help | util/help2code.py >> civet_wrapper/arguments.py

    That happens in Dockerfile, so

        docker build -t fnndsc/pl-civet .

    Verify

        docker run --rm --entrypoint /bin/cat fnndsc/pl-civet /usr/local/lib/python3.6/dist-packages/civet_wrapper/arguments.py
        docker run --rm fnndsc/pl-civet civet_wrapper --help
"""

import sys

for line in sys.stdin:
    if line.startswith('Summary of options:'):
        break
    else:
        continue

indent = '    '
print('def add_civet_arguments(p: CustomArgsApp):')

# global state
flag = ''
metavar = ''
help_string = []

# denote which flags are formatted too weirdly for automatic processing,
# and manually define the code for it.
edge_cases = {
        '-thickness': indent + "nargs=2, metavar='T:T:T N:N'"
}


def fix_quote(string):
    return "\\'".join(string.split("'"))


def finish_help():
    global flag, help_string
    if flag:
        help_string = map(fix_quote, help_string)
        help_string = ' '.join(help_string)
        print(f",\n{indent}{indent}help = '{help_string}')")
        flag = ''
        help_string = []


for line in sys.stdin:
    if line.startswith('USAGE:'):
        break
    
    line = line.rstrip()

    if len(line) == 0:
        continue

    if line.startswith('-- '):
        finish_help()
        print(indent + '# ' + line)
        continue

    if line.startswith('   -'): # found a new option
        finish_help()
    else:  # continue building the help string of the current flag
        help_string.append(line.lstrip())
        continue

    line = line.lstrip()
    flag_end = line.index(' ')
    flag = line[0:flag_end]

    if line[flag_end+1] == '<':
        metavar_end = line.index('>')
        metavar = line[flag_end+2:metavar_end]
        flag_end = metavar_end + 1
    else:
        metavar = ''
    
    if flag in edge_cases:
        code = f"p.add_argument_c('{flag}',\n    {edge_cases[flag]}"
    elif metavar:
        code = f"p.add_argument_c('{flag}', metavar='{metavar}'"
    else:
        code = f"p.add_argless('{flag}'"
    print(indent + code, end='')

    line = line[flag_end:].lstrip()
    if line:
        help_string.append(line)

finish_help()
