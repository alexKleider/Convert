#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# Copyright 2014 Alex Kleider; All Rights Reserved.

# file: 'rmogv.py'
"""
Removes files with names ending in FILE_NAME_SUFFIX, 
currently set to '.ogv'
This is a utility which removes the ogv files created by 
convert2ogv.py, useful when testing so you can delete the files 
created when testing (as long as you've done it 
DELETE_ORIGINALS set to False.)
"""
print("Running Python3 script: 'rmogv.py'.......")

import os

ROOT_DIR = "/home/alex/Python/Conversion/Mp4"
FILE_NAME_SUFFIX = '.ogv'

response = input("""##########################
We are about to remove all files ending in {}
In and beneath the directory {}.
Are you sure you want to proceed? (y/n) """.format(FILE_NAME_SUFFIX,
                                                    ROOT_DIR))

if response and response[0] in "yY":
    for root, dirs, files in os.walk(ROOT_DIR):
        print("Traversing {0}".format(root))
        for f_name in files:
            full_path = os.path.join(root, f_name)
            if os.path.isfile(full_path) and full_path.endswith(FILE_NAME_SUFFIX):
                os.remove(full_path)

