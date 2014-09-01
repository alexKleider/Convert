#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set file encoding=utf-8 :
# Copyright 2014 Alex Kleider; All Rights Reserved.

# file: 'mod_copy.py'
"""
Provided as constants in the code are:
1. name of an existing directory assumed to contain mp4 files beneath it.
2. name of another as yet non-existent directory which will be created. 
Everything under directory 1 will be moved to directory 2,
in the process changing any mp4 files into ogv format.
Changing the html code (in order that links are not broken, must be done
separately.  (See sister program scan4html.py.)
"""
import os
import sys
import shlex
import shutil
import datetime
import subprocess


ROOT_DIR = os.path.expanduser("~/Python/Conversion/Mp4")
NEW_ROOT_DIR = os.path.abspath("./NewDir")
LOGGING_FILE = "log.log"
OLD_SUFFIX = '.mp4'
NEW_SUFFIX = '.ogv'
COMMAND_LINE = "avconv -flags qscale -global_quality 1 -i {0} -acodec libvorbis  {1}"

def log(entry):
    """Logs entry to LOGGING_FILE."""
    with (open(LOGGING_FILE, "a")) as f:
        f.write("{0}\n".format(entry))

def setup_directories(old_dir, new_dir):
    """Check that old_dir exists and create new_dir.

    Program aborts if old_dir doesn't exist or if new_dir already exists.
    """
    if not os.path.isdir(old_dir):
        sys.exit("Expected directory can't be found.")
    if os.path.isdir(new_dir):
        sys.exit("Destination directory already exists.")
    os.mkdir(new_dir)

def convert_file(source, destination):
    """Convert source file (assumed to be .mp4) to destination.ogv.
    
    Return code 0 (success) or 1.
    Side effect: logs problems if they occur.
    This depends on the log function.
    """
    args = shlex.split(COMMAND_LINE.format(source, destination))
    return_code = subprocess.call(args)
    if return_code:
        log("   {0} => return code >0."\
                                .format(source))
    return return_code


def move_files(old_dir, new_dir):
    """Move all files from old_dir to new_dir converting mp4 into ogv.

    old_dir must already exit, new_dir need not.
    Only mp4 files will be changed (to ogv;) all other files 
    will be moved 'as is.'  If ogv files are found on the input side, this
    will be logged and a notification sent to stdout.
    Depends on log function.
    """
    for root, _, files in os.walk(old_dir):
        working_destination = \
        os.path.abspath(root).replace(os.path.abspath(old_dir),
                                    os.path.abspath(new_dir), 1)
        if not os.path.isdir(working_destination):
            os.mkdir(working_destination)
        for file_name in files:
            source = os.path.abspath(os.path.join(root, file_name))
            destination = source.replace(os.path.abspath(old_dir),
                                        os.path.abspath(new_dir), 1)
            if source.endswith(OLD_SUFFIX):
                destination = destination.replace(OLD_SUFFIX, NEW_SUFFIX)
                return_code = convert_file(source, destination)
                if return_code:
                    print("!!!!!!!!!Return_code is {}.".\
                                                    format(return_code))
            else:
                shutil.copyfile(source, destination) 

def main():
    """Get user confirmation before calling move_files."""
    response = input("""Assume existing directory '{}'
    and that its contents are to be transfered to 
    as yet not existing directory '{}'
    converting any mp4 files to ogv format in the process.
    OK to proceed? (Y/n) """.format(ROOT_DIR,
                                    NEW_ROOT_DIR))
    if not response or not response[0] in 'yY':
        print("""
        Please rerun after changing constants to better suit your needs.
        Bye.""")
        sys.exit(0)
    print("HERE WE GO...")
    move_files(ROOT_DIR, NEW_ROOT_DIR)

if __name__ == "__main__":
    print("Running Python3 script: 'mod_copy.py'.......")
    print('"""', end='')
    print(__doc__, end='')
    print('"""')
    main()


