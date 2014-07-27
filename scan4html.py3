#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# Copyright 2014 Alex Kleider; All Rights Reserved.

# file: 'scan4html.py3'
"""
Want to be able to traverse a directory tree and preform a substitution 
of ".ogv" for any instance of ".mp4".

Sister procedure is convert2ogv.py3 
to scan for all '.mp4' files and convert them to '.ogv'.
"""
print("Running Python3 script: 'scan4html.py3'.......")

import os
import sys

# Decide about MODE and TEST.

TEST = True
#TEST = False

MODE = "debug"
#MODE = "production"

if MODE == "production":
    NEW_FILE_PREFIX = ''  #  IN PRODUCTION MODE 
    ROOT_DIR = "/var/www"
    OLD = '.mp4'
    NEW = '.ogv'
else:  # MODE == "debug"
    NEW_FILE_PREFIX = 'modified_'  # DURING DEBUGGING
    ROOT_DIR = "/home/alex/WWW"
    OLD = '.JPG'
    NEW = '.photo'

FILE_NAME_SUFFIX = ".html"

print(""" 
###################################
   #   Running in {0} mode.    #
###################################
""".format(MODE))


def convert_text(text, old, new):
    if text.find(old) >=0:
        return text.replace(old, new)

for root, dirs, files in os.walk(ROOT_DIR):
    print("Traversing...")
    for f_name in files:
        if f_name.endswith(FILE_NAME_SUFFIX):
            full_path = os.path.join(root, f_name)
            print("  Found '{0}'.".format(full_path))
            with open(full_path) as f:
                data = f.read()
                replacement = convert_text(data, OLD, NEW)
            if replacement:
                print("      {0}".format(full_path))
                print("      .. converted and => media as:")
                new_file_name = NEW_FILE_PREFIX + f_name
                final_path = os.path.join(root, new_file_name)
                print(" ---     {0}".format(final_path))
                if TEST:
                    print\
                    ("    .. we are in TEST mode- file not written!")
                else:
                    with open(final_path, 'w') as f:
                        f.write(replacement)
            else:
                print("      .. no conversion necessary.")





