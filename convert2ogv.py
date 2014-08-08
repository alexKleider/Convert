#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# Copyright 2014 Alex Kleider; All Rights Reserved.

# file: 'convert2ogv.py'
"""
convert2ogv.py -  A Python 3 script
to scan for all '.mp4' files and convert them to '.ogv'.

!!!!!!!!!!!!        BE SURE TO SET ROOT_DIR        !!!!!!!!!!!
!!!  And decide if you want DELETE_ORIGINALS to be True or False. !!!

Sister procedure is 'scan4html.py'
to traverse a directory tree and within any html file
preform a substitution of ".ogv" for any instance of ".mp4".
"""


import os
import subprocess
import shlex
import sys

ROOT_DIR = os.path.expanduser("~/Python/Conversion/Test")
#DELETE_ORIGINALS = False
DELETE_ORIGINALS = True

OLD_SUFFIX = '.mp4'
NEW_SUFFIX = '.ogv'


def main():

    """Main loop for command processing"""

    print("Running Python3 script: 'convert2ogv.py'.......")
    print(__doc__)

    command_line = "avconv -i {0}{1} -acodec libvorbis -q 0 {0}{2}"

    subprocess.call("date")

    response = input("""Root directory of files to be converted is set to..
    {0}
    OK to proceed? """.format(ROOT_DIR))

    if response[0] in 'yY':
        pass
    else:
        print("Change ROOT_DIR and re-run the script.")
        sys.exit(1)

    n_files = 0
    n_conversions = 0

    # pylint: disable=W0612
    for root, dirs, files in os.walk(ROOT_DIR):
        #print("Traversing...")
        for f_name in files:
            n_files += 1
            if f_name.endswith(OLD_SUFFIX):
                n_conversions += 1
                f_name_without_suffix = f_name[:-len(OLD_SUFFIX)]
                full_path_without_suffix = \
                                os.path.join(root, f_name_without_suffix)
                print("  {0:>4}. {1}".format(n_conversions,
                                             full_path_without_suffix))

                args = shlex.split(command_line.\
                    format(full_path_without_suffix, OLD_SUFFIX, NEW_SUFFIX))
                subprocess.call(args)
                subprocess.call("date")
                if DELETE_ORIGINALS:
                    os.remove('{0}{1}'\
                            .format(full_path_without_suffix, OLD_SUFFIX))



    print("Files checked: {};  Files converted: {}.".\
                                        format(n_files, n_conversions))

