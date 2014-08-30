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

# The following was suggested by luca.barbato@gmail.com
COMMAND_LINE = "avconv -flags qscale -global_quality 1 -i {0}{1} -acodec libvorbis  {0}{2}"

#COMMAND_LINE = "avconv -i {0}{1} -acodec libvorbis -q 0 {0}{2}"
#COMMAND_LINE = "avconv -i {0}{1} -acodec libvorbis  {0}{2}"
# From man avconv:
#   -acodec codec (input/output)
#       Set the audio codec. This is an alias for "-codec:a".

def log(entry):
    with (open("convert.log", "a")) as f:
        f.write("{0}\n".format(entry))

def convert_file(root, full_path_without_suffix):
    """Convert file from .mp4 to .ogv: returns "Failed" if fails.
    
    Side effect: logs problems if they occur.
    This depends on the log function.
    Will not delete original if conversion is unsuccessful
    (even if DELETE_ORIGINALS is set to True.)"""

    args = shlex.split(COMMAND_LINE.format(full_path_without_suffix,
                                           OLD_SUFFIX,
                                           NEW_SUFFIX))
    try:
#       return_code = subprocess.check_call(args, timeout=300)
# timeout not available until python 3.3
        return_code = subprocess.check_call(args)
    except subprocess.CalledProcessError:
        ok2delete = False
        log("   {0}{1} => return code >0."\
                                .format(f_name_without_suffix,
                                        OLD_SUFFIX))
        return "Failed"

#   except subprocess.TimeoutExpired: # New in version 3.3
#                                       We are still at 3.2.4
#   except subprocess.SubprocessError: # Assume timeout.
#       ok2delete = False
#       log("   {0}{1} taking too long, aborted."\
#                               .format(f_name_without_suffix,
#                                       OLD_SUFFIX))
#       return "Failed"
    if DELETE_ORIGINALS and return_code == 0:
        # Won't delete if conversion is unsuccessful.
        os.remove('{0}{1}' .format(full_path_without_suffix,
                                   OLD_SUFFIX))

def main():

    """Main loop for command processing"""

    print("Running Python3 script: 'convert2ogv.py'.......")
    print(__doc__)

    response = input("""Root directory of files to be converted is set to..
    {0}
    OK to proceed? (y/n): """.format(ROOT_DIR))

    if response[0] in 'yY':
        pass
    else:
        print("Change ROOT_DIR and re-run the script.")
        sys.exit(1)

    n_files = 0
    n_attempts = 0
    n_conversions = 0
    n_failures = 0

    print("######## {} ########".format(datetime.datetime.now()))

    for root, _, files in os.walk(ROOT_DIR):
        for f_name in files:
            if os.path.isdir(f_name):
                continue  # To avoid counting or processing directories.
            n_files += 1
            if f_name.endswith(OLD_SUFFIX):
                n_attempts += 1
                f_name_without_suffix = f_name[:-len(OLD_SUFFIX)]
                full_path_without_suffix = os.path.join(root,
                                            f_name_without_suffix)
                possibly_already_converted_file = \
                    full_path_without_suffix + NEW_SUFFIX
                if os.path.isfile(possibly_already_converted_file):
                    print("Converted version ({}) already exists."\
                            .format(possibly_already_converted_file))
                    continue
                
                log("  {0:>4}. {1}: {2}".format(n_conversions,
                                 datetime.datetime.now(),
                                 full_path_without_suffix))

                if convert_file(root,
                                full_path_without_suffix) == "Failed":
                    n_failures += 1
                else:
                    n_conversions += 1
                print("##### {} ######"\
                                    .format(datetime.datetime.now()))

    print("Files checked: {};  Conversion attempts: {}; Successes: {}."\
                                                    .format(n_files,
                                                            n_attempts,
                                                            n_conversions,
                                                            ))
if __name__ == "__main__":

    log("""
####  Beginning a new instance of convert2ogv {0}.""".\
        format(datetime.datetime.now()))

    main()

    log\
("""---- Script 'convert2ogv.py' ran successfully to completion.  -----
----       Finished {}      ----""".format (datetime.datetime.now()))

