#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# Copyright 2014 Alex Kleider; All Rights Reserved.

# file: 'rmogv.py'
"""
Put your docstring here.
"""
print("Running Python3 script: 'rmogv.py'.......")

import os

ROOT_DIR = "/home/alex/Python/Conversion/Test"
FILE_NAME_SUFFIX = '.ogv'

for root, dirs, files in os.walk(ROOT_DIR):
    print("Traversing {0}".format(root))
    for f_name in files:
        if f_name.endswith(FILE_NAME_SUFFIX):
            full_path = os.path.join(root, f_name)
            print("Deleting {0}".format(full_path))
            os.remove(full_path)
