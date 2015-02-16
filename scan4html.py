#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# Copyright 2014, 2015 Alex Kleider; All Rights Reserved.

# file: 'scan4html.py'
"""
scan4html.py 

Usage:
    scan4html.py -h | --version
    scan4html.py  [-d] [-i DIRECTORY] [-f FORMAT]

Options:
  -h --help        Print this docstring.
  --version        Provide version information.
  -d --debug   Provide debugging statements.
  -i DIRECTORY --input=DIRECTORY   Directory under which the html files
                                    are to be found. [Default: ./]
  -f FORMAT --format=FORMAT   Format desired. Currently only ogv and 
                                webm are supported.  [Default: webm]

This script traverses the given DIRECTORY (or current working directory
if none is provided) and examines all files named with the '.html'
suffix.  Within the text of each such file, any file name with the suffix
'.mp4' is changed to have the suffix appropriate to the FORMAT argument
(default is 'webm' if none is provided.)  The only two formats currently
supported are webm and ogv.

Sister procedure is 'convert_mp4.py' which traverses a directory tree
and converts all mp4 files into the FORMAT specified (defaults to webm.)
The only two formats currently supported are webm and ogv.
"""

import os
import sys
from docopt import docopt


VERSION = "v0.1.0"
FILE_NAME_SUFFIX = ".html"
OLD_SUFFIX = '.mp4'

args = docopt(__doc__, version=VERSION)
if args['--debug']:
    print(args)
    response = input("Do you want to proceed? (y/n) ")
if response in 'yY':
    pass
else:
    print("Correct parameters and try again.")
    sys.exit(1)
if not args['--format'] in ('ogv', 'webm'):
    print("Unsupported format given.")
    sys.exit(1)
else:
    NEW_SUFFIX = '.{}'.format(args['--format'])

def convert_text(text, old, new):
    """Replace 'old' text with 'new' text inside variable text"""
    if text.find(old) >= 0:
        return text.replace(old, new)

for root, _, files in os.walk(args['--input']):
    if args['--debug']:
        print("Traversing {}".format(root))
    for f_name in files:
        if f_name.endswith(FILE_NAME_SUFFIX):
            full_path = os.path.join(root, f_name)
            with open(full_path) as f:
                data = f.read()
                replacement = convert_text(data, OLD_SUFFIX, NEW_SUFFIX)
            if replacement:
                if args['--debug']:
                    print("Converted: {}".format(full_path))
                with open(full_path, 'w') as f:
                    f.write(replacement)
            else:
                if args['--debug']:
                    print("No change: {}".format(full_path))

