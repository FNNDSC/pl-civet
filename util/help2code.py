#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 18:26:28 2020

@author: Jennings Zhang <Jennings.Zhang@childrens.harvard.edu>

Purpose: parse output of `CIVET_Processing_Pipeline -help` to generate
         Python argparse-like code for pl-civet, a Python wrapper for CIVET

Usage:
       CIVET_Processing_Pipeline -help | python help2code.py
"""

import sys

for line in sys.stdin:
    if line.startswith('Summary of options:'):
        break
    else:
        continue


flag = ''
metavar = ''
help_string = []

edge_cases = {
        '-thickness': "nargs=2, metavar='T:T:T N:N'"
}

def fix_quote(string):
    return "\\'".join(string.split("'"))


def finish_help():
    global flag, help_string
    if flag:
        help_string = map(fix_quote, help_string)
        help_string = ' '.join(help_string)
        print(f",\n    help = '{help_string}')")
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
        print('# ' + line)
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
        print(f"self.add_argument_c('{flag}',\n    {edge_cases[flag]}", end='')
    elif metavar:
        print(f"self.add_argument_c('{flag}', metavar='{metavar}'", end='')
    else:
        print(f"self.add_argless('{flag}'", end='')

    line = line[flag_end:].lstrip()
    if line:
        help_string.append(line)

finish_help()
