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
import datetime

ROOT_DIR = os.path.expanduser("~/Python/Conversion/Mp4")
DELETE_ORIGINALS = False
#DELETE_ORIGINALS = True

OLD_SUFFIX = '.mp4'
NEW_SUFFIX = '.ogv'

#COMMAND_LINE = "avconv -i {0}{1} -acodec libvorbis -q 0 {0}{2}"
COMMAND_LINE = "avconv -i {0}{1} -acodec libvorbis  {0}{2}"
# From man avconv:
#   -acodec codec (input/output)
#       Set the audio codec. This is an alias for "-codec:a".

def log(entry):
    with (open("convert.log", "a")) as f:
        f.write("{0}\n".format(entry))

def convert_file(root, f_name):
    """Convert file from .mp4 to .ogv: returns "Failed" if fails.
    
    Side effect: logs problems if they occur.
    This depends on the log function.
    Will not delete original if conversion is unsuccessful
    (even if DELETE_ORIGINALS is set to True.)"""

    f_name_without_suffix = f_name[:-len(OLD_SUFFIX)]
    full_path_without_suffix = os.path.join(root,
                                            f_name_without_suffix)
    args = shlex.split(COMMAND_LINE.format(full_path_without_suffix,
                                           OLD_SUFFIX,
                                           NEW_SUFFIX))
    ok2delete = True
    try:
        subprocess.check_call(args, timeout=300)
    except subprocess.CalledProcessError:
        ok2delete = False
        log("   {0}{1} => return code >0."\
                                .format(f_name_without_suffix,
                                        OLD_SUFFIX))
        return "Failed"
    except subprocess.TimeoutExpired:
        ok2delete = False
        log("   {0}{1} taking too long, aborted."\
                                .format(f_name_without_suffix,
                                        OLD_SUFFIX))
        return "Failed"

    if DELETE_ORIGINALS:
        # Won't delete if conversion is unsuccessful.
        os.remove('{0}{1}' .format(full_path_without_suffix,
                                   OLD_SUFFIX))

def main():

    """Main loop for command processing"""

    print("Running Python3 script: 'convert2ogv.py'.......")
    print(__doc__)

    response = input("""Root directory of files to be converted is set to..
    {0}
    OK to proceed? """.format(ROOT_DIR))

    if response[0] in 'yY':
        pass
    else:
        print("Change ROOT_DIR and re-run the script.")
        sys.exit(1)

    n_files = 0
    n_attempts = 0
    n_failures = 0

    log("""
###################################################
Beginning a new instance of convert2ogv {0}\n""".\
        format(datetime.datetime.now()))

    subprocess.call("date")

    # pylint: disable=W0612
    for root, dirs, files in os.walk(ROOT_DIR):
        for f_name in files:
            if os.path.isdir(f_name):
                continue  # To avoid counting or processing directories.
            n_files += 1
            if f_name.endswith(OLD_SUFFIX):
                n_attempts += 1
                log("  {0:>4}. {1}".format(n_attempts,
                                 full_path_without_suffix))

                if convert_file(root, f_name) == "Failed":
                    n_failures += 1
                subprocess.call("date")

    print("Files checked: {};  Files converted: {}; Failures: {}."\
                                                    .format(n_files,
                                                            n_attempts,
                                                            n_failures))

if __name__ == "__main__":
    main()
