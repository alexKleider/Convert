#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# Copyright 2014 Alex Kleider; All Rights Reserved.

# file: 'convert_mp4.py'  A Python 3 script
"""
convert_mp4.py

Usage:
    convert_mp4.py -h | --version
    convert_mp4.py [-d] [-l LOGFILE] [-i DIRECTORY] [-f FORMAT]

Options:
  -h --help        Print this docstring.
  --version        Provide version information.
  -d --delete   Delete the original file if successfully converted.
  -i DIRECTORY --input=DIRECTORY   Directory under which mp4 files are
                                    found. [Default: ./]
  -f FORMAT --format=FORMAT   Format desired. Currently only ogv and 
                                webm are supported.  [Default: webm]
  -l LOGFILE --logfile=LOGFILE  Specify log file.  [Default: /tmp/conv.log]

This script traverses the given directory (or current working
directory if none is provided) and converts all mp4 files into the
FORMAT specified (defaults to webm.)  The only two formats currently
supported are webm and ogv.

Sister procedure is 'scan4html.py' which traverses a directory tree
and within any html file preforms the appropriate substitution for 
any instance of ".mp4".
"""

import os
import subprocess
import shlex
import sys
import datetime
from docopt import docopt

VERSION = "v0.1.0"

OLD_SUFFIX = '.mp4'

def get_args():
    args = docopt(__doc__, version=VERSION)
    args['--input'] = os.path.abspath(os.path.expanduser(args['--input']))
    if args['--format'] == 'ogv':
        args['COMMAND_LINE'] =(
"avconv -flags qscale -global_quality 1 -i {0}{1} -acodec libvorbis {0}.{2}")
    elif args['--format'] == 'webm':
        args['COMMAND_LINE'] =(
    "avconv -flags qscale -global_quality 1 -i {0}{1} -y {0}.{2}")
    else:
        print("'{}' is an unrecognized format. Terminating."
                    .format(args['--format']))
        sys.exit(1)
    print(args)
    return(args)

#COMMAND_LINE = "avconv -i {0}{1} -acodec libvorbis -q 0 {0}{2}"
#COMMAND_LINE = "avconv -i {0}{1} -acodec libvorbis  {0}{2}"
# From man avconv:
#   -acodec codec (input/output)
#       Set the audio codec. This is an alias for "-codec:a".

def log(entry, args):
    with (open(args['--logfile'], "a")) as f:
        f.write("{0}\n".format(entry))

def convert_file(root, full_path_without_suffix, args):
    """Convert .mp4 file to format specified by args['--format'].
    
    Returns "Failed" if fails.
    
    Side effect: logs problems if they occur.
    This depends on the log function.
    Will not delete original if conversion is unsuccessful
    (even if args['--delete'] is set.)          
    """
    command_args = shlex.split(args['COMMAND_LINE']
                                .format(full_path_without_suffix,
                                       OLD_SUFFIX,
                                       args['--format']))
    try:
#       return_code = subprocess.check_call(args, timeout=300)
# timeout not available until python 3.3
        return_code = subprocess.check_call(command_args)
        print('Return code is {}.'.format(return_code))
    except subprocess.CalledProcessError:
        print('Failed return code is {}.'.format(return_code))
        log("   {0}{1} => return code >0."\
                                .format(full_path_without_suffix,
                                        OLD_SUFFIX),
            args)
        return "Failed"

#   except subprocess.TimeoutExpired: # New in version 3.3
#                                       We are still at 3.2.4
#   except subprocess.SubprocessError: # Assume timeout.
#       ok2delete = False
#       log("   {0}{1} taking too long, aborted."\
#                               .format(f_name_without_suffix,
#                                       OLD_SUFFIX),
#           args)
#       return "Failed"
    if args['--delete']:
        # Won't delete if conversion is unsuccessful.
        os.remove('{0}{1}' .format(full_path_without_suffix,
                                   OLD_SUFFIX))

def main():

    """Main loop for command processing"""

    print("Running Python3 script: 'convert_mp4.py'.......")
#   print(__doc__)

    args = get_args()
    response = input("""Root directory of files to be converted is set to..
    {0}
    OK to proceed? (y/n): """.format(args['--input']))

    if response[0] in 'yY':

        log("""
####  Beginning a new instance of convert_mp4 {0}.""".\
                format(datetime.datetime.now()),
            args)
    else:
        print(
"Re-run the script setting option -i  --input to desired directory.")
        sys.exit(0)

    n_files = 0
    n_attempts = 0
    n_conversions = 0
    n_failures = 0

    print("######## {} ########".format(datetime.datetime.now()))

    for root, _, files in os.walk(args['--input']):
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
                    full_path_without_suffix + args['--format']
                if os.path.isfile(possibly_already_converted_file):
                    print("Converted version ({}) already exists."\
                            .format(possibly_already_converted_file))
                    continue
                
                log("  {0:>4}. {1}: {2}".format(n_conversions,
                                 datetime.datetime.now(),
                                 full_path_without_suffix),
                    args)

                if convert_file(root,
                                full_path_without_suffix,
                                args) == "Failed":
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

    log(
"""---- Script 'convert_mp4.py' ran successfully to completion.  -----
----       Finished {}      ----""".format (datetime.datetime.now()),
        args)


if __name__ == "__main__":

    main()

