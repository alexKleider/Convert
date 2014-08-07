#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# Copyright 2014 Alex Kleider; All Rights Reserved.

# file: 'scan4html.py'
"""scan4html.py  - a Python 3 script:
Want to be able to traverse a directory tree and preform a substitution
of ".ogv" for any instance of ".mp4" (simple string substitution)
found in any file with a name ending in ".html".

Sister procedure is convert2ogv.py
to scan for all '.mp4' files and convert them to '.ogv'.
"""
print("Running ", end='')
print(__doc__)

import os
import sys

# Decide about MODE and TEST.

#TEST = True
TEST = False

MODE = "debug"
#MODE = "production"

if MODE == "production":
    NEW_FILE_PREFIX = ''  #  IN PRODUCTION MODE
        # in production mode we don't rename, we replace.
    ROOT_DIR = "/home/alex/Python/Conversion/WWW"
    OLD = '.mp4'
    NEW = '.ogv'
else:  # MODE == "debug"
    NEW_FILE_PREFIX = 'modified_'  # DURING DEBUGGING
    ROOT_DIR = "/home/alex/Python/Conversion/WWW"
    OLD = '.JPG'
    NEW = '.photo'

FILE_NAME_SUFFIX = ".html"

print("""
#####################################
   #   Running in {0} mode.    #
   #   TEST is set to {1}.     #
ROOT_DIR is set to {2}
#####################################
""".format(MODE, TEST, ROOT_DIR))
print("""
In debug mode we use '.JPG' and '.photo' as our
test suffixes and rather than replacing files containing
them, we add another file with its name prefixed 
with 'modified_'.
In production mode, we use '.mp4' and '.ogv',
and file names are left unchanged.

If test is True: files are not modified.  This allows us
to test traversal without changing any files.
"""

response = input("Do you want to proceed? (y/n) ")
if response in 'yY':
    pass
else:
    print("Correct parameters and try again.")
    sys.exit(1)


def convert_text(text, old, new):
    """Replace 'old' text with 'new' text inside variable text"""
    if text.find(old) >= 0:
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





