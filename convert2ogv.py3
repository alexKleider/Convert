#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# Copyright 2014 Alex Kleider; All Rights Reserved.

# file: 'convert2ogv.py3'
"""
convert2ogv.py3 
to scan for all '.mp4' files and convert them to '.ogv'.

Sister procedure is 'scan4html.py3'
to traverse a directory tree and within any html file 
preform a substitution of ".ogv" for any instance of ".mp4".
"""

print("Running Python3 script: 'convert2ogv.py3'.......")

CMD = ["avconv",
       "-i",
       None,
       "-acodec",
       "libvorbis",
       "-q",
       "0",
       None]

OLD_SUFIX = '.mp4'
NEW_SUFIX = '.ogv'

def populated_cmd(full_path_without_sufix):
    CMD[2] = "{0}{1}".format(full_path_without_sufix, OLD_SUFIX)
    CMD[-1] =  "{0}{1}".format(full_path_without_sufix, NEW_SUFIX)
    return CMD

for f_name in ('f1', 'f2', 'f3'):
    print(populated_cmd(f_name))
