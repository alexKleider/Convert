#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# Copyright 2014 Alex Kleider; All Rights Reserved.

# file: 'scan4html.py3'
"""
This is the "UNDO" branch- it is code to undo what has been done during
development in the "MASTER" branch.


Want to be able to traverse a directory tree and preform a substitution 
of ".ogv" for any instance of ".mp4".

Sister procedure is convert2ogv.py3 
to scan for all '.mp4' files and convert them to '.ogv'.
"""
print("Running Python3 script: 'scan4html.py3'.......")

import os
import sys

# THE FOLLOWING TWO CONSTANTS MUST BE CHANGED:

NEW_FILE_PREFIX = 'temp.'  # DURING DEBUGGING ONLY 
# IN PRODUCTION ENVIRONMENT, CHANGE ABOVE TO EMPTY STRING.
# NEXT CONSTANT SHOULD LIKELY BE SET TO RACHEL'S ROOT DIRECTORY.
ROOT_DIR = "/home/alex/WWW"

OLD = '.mp4'
NEW = '.ogv'
FILE_NAME_SUFFIX = ".html"

def convert_text(text, old, new):
    if text.find(old) >=0:
        return text.replace(old, new)

for root, dirs, files in os.walk(ROOT_DIR):
    print("Traversing...")
    for f_name in files:
        if f_name.endswith(FILE_NAME_SUFFIX) and\
                            f_name.endswith(FILE_NAME_SUFFIX):
            full_path = os.path.join(root, f_name)
            print("  Found a target file. Will delete:")
            print("  {0}".format(
            with open(full_path) as f:
                data = f.read()
                replacement = convert_text(data, OLD, NEW)
                print("    Check if conversion needed.")
            if replacement:
                print("      {0}".format(full_path))
                print("      .. converted and => media as:"
                new_file_name = os.path.join(root, 
                        (NEW_FILE_PREFIX + f_name)),
                print("      {0}".format(new_file_name))
                with open(new_file_name, 'w') as f:
                    f.write(replacement)




