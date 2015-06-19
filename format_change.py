#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set file encoding=utf-8 :
# Copyright 2014, 2015 Alex Kleider; All Rights Reserved.

# file: 'format_change.py'
"""
format_change.py

Usage:
    format_change.py -h | --version
    format_change.py [options] -o OUT_DIR
    format_change.py [options] --in-place

Options:
  -h --help        Print this docstring.
  --version        Provide version information.
  -d --debug       Debug mode: provides debugging information.
  -v --verbose     Provides progress information.
  -l LOGFILE --logfile=LOGFILE  Specify log file.
                                            [Default: /tmp/conv.log]
  -s STATUSFILE --statusfile=STATUSFILE   Specify a status file.
                                          [Default: .status-report]
  -f FORMAT --format=FORMAT   Format desired. Currently only ogv and 
                                webm are supported. [Default: webm]
  -i IN_DIR --input=IN_DIR   Directory under which the html and mp4
                                    files are found. [Default: ./]
  -o OUT_DIR --output=OUT_DIR    Destination directory which will be
                                created if it doesn't already exist. 
  --in-place    Make changes to the source directory rather than 
                              creating a new one.

This script traverses the IN_DIR directory (or current working
directory if none is provided) looking for non proprietary video files.
Those found, are converted to the format specified by FORMAT.
To date, this script supports conversion of only mp4 and flv videos to
webm (the default) or ogv format.
In order that links remain unbroken, html files are also scanned and
where need be, the links are renamed as appropriate.
If OUT_DIR is specified, another directory structure is created
incorporating the changes, leaving the original unchanged.  If it
already exists, its content is updated (i.e. work previously done is not
repeated.)
If --in-place is specified, original files are modified.
At completion, a report is presented outlining time taken and extra
disk space required expressed in various ways.
"""

import os
import sys
import shlex
import shutil
import datetime
import subprocess
from docopt import docopt

VERSION = 'v0.1.0'
PROPRIETARY_SUFFIXES = ('.mp4', '.flv',)
ENCODING = "latin-1"

def get_args():
    """Sets and returns globals (as a dictionary.)
    
    Use docopt to collect command line arguments, 
    and sets up other globals.
    Causes termination if invalid format is given.
    """
    args = docopt(__doc__, version=VERSION)
    args['--input'] = (
        os.path.abspath(os.path.expanduser(
                                    args['--input'])))
    args['--logfile'] = (
        os.path.abspath(os.path.expanduser(
                                    args['--logfile'])))
    if args['--in-place']:
        args['--output'] = args['--input']
    else:
        args['--output'] = (
            os.path.abspath(os.path.expanduser(
                                        args['--output'])))
    args['html_suffix'] = '.html'
    args['proprietary_suffixes'] = PROPRIETARY_SUFFIXES
    for suffix in args['proprietary_suffixes']:
        args[suffix] = {}
        args[suffix]['n_encountered'] = 0
        args[suffix]['n_converted'] = 0
        args[suffix]['n_failed'] = 0
        args[suffix]['time_wasted'] = datetime.timedelta(0, 0, 0)
        args[suffix]['old_size'] = 0
        args[suffix]['new_size'] = 0
        args[suffix]['time_delta'] = datetime.timedelta(0, 0, 0)
    args['n_html'] = 0
    args['n_changed'] = 0
    args['current_proprietary_suffix'] = ''
    if args['--format'] == 'webm':
        args['new_suffix'] = '.webm'
        args['command'] =' '.join(("avconv -flags qscale",
                            "-global_quality 1 -i '{}' -y '{}'"))
    elif args['--format'] == 'ogv':
        args['new_suffix'] = '.ogv'
        args['command'] =' '.join(("avconv -flags qscale",
            "-global_quality 1 -i '{}' -acodec libvorbis '{}'"))
    else:
        if args['--verbose']:
            print("'{}' is an unrecognized format. Terminating."
                        .format(args['--format']))
        sys.exit(1)
    if args['--debug']:
        print(args)
    return(args)


def debug(entry, args):
    """Provides debugging notices.
    """
    if args['--debug']:
        print(':'.join(('DBG', entry, )))

def report(entry, args):
    """Provides extra information (verbose mode.)
    """
    if args['--verbose']:
        print(entry)

def log(entry, args):
    """Provides logging to args['--logfile']
    """
    with (open(args['--logfile'], "a")) as f:
        f.write("{0}\n".format(entry))

def status(entry, args):
    """Provides for a file that contains the last thing attempted.
    
    The file name is args['--statusfile']
    It is over written with each entry.
    """
    with (open(args['--statusfile'], "w")) as f:
        f.write("{0}\n".format(entry))

def is_target_video_file(file_name, args):
    """Checks if <file_name> ends in one of the suffixes specified in
    args['proprietary_suffixes'].  If so, returns True after setting
    args['current_proprietary_suffix'].  Otherwise it returns False.
    Clients of this function can decide if they want to reset
    args['current_proprietary_suffix'] to the empty string.
    It is suggested that they do.""" 
    for suffix in args['proprietary_suffixes']:
        if file_name.endswith(suffix):
            args['current_proprietary_suffix'] = suffix
            return True
    return False

def convert_video(source, destination, args):
    """Convert to alternate video format.
    
    Format of source is assumed to be one of the ones listed
    in args['proprietary_suffixes'].
    Format of destination is determined by args['--format'].
    Return code 0 (success) or 1.
    Side effect: logs problems if they occur.
    This depends on the log function.
    """
    
    command_line = shlex.split(args['command']
                            .format(source, destination))
    debug("""Command line being called is:
    {}""".format(" ".join(command_line)),
        args)
    return_code = subprocess.call(command_line)
    if return_code:
        message = ("{:24}: {} => return code >0."
                    .format(datetime.datetime.now(), source))
        log(message, args)
        report(message, args)
    else:
        # The subprocess.call has already moved the data,
        # here we just want to move the metadata.
        shutil.copymode(source, destination, follow_symlinks=False)
    return return_code

def convert_text(text, old, new):
    """Text replacement.

    First and third parameters are strings. 
    The second (middle) parameter is an iterable of strings.
    Any occurrence of any of the strings in the the second parameter
    found in the first parameter is replaced by the third parameter.
    Returns altered text or None if no alterations were done.
    """
    ret = 0
    for target in old:
        if text.find(target) >= 0:
            text = text.replace(target[1:], new[1:])
            ret += 1
    if ret:
        return text

def modify_html(source, destination, args):
    """Modifies the text in .html files.
    
    Changes each instance of '.mp4' in source to the suffix appropriate
    to args['--format'] in destination.
    Returns True if modifications were necessary, False if not.
    If modifications are not necessary, still moves source to
    destination unless its already there or args['--in-place'] is
    set to True (efectively the same thing.)
    """
    with open(source, 'r', encoding=ENCODING) as source_file:
        file_content = source_file.read()
        content = convert_text(file_content, 
                                args['proprietary_suffixes'],
                                args['new_suffix'],)
    if content:
        with open(destination, 'w', 
                    encoding=ENCODING) as destination_file:
            destination_file.write(content)
        shutil.copymode(source, destination, follow_symlinks=False)
        return True
    else:  # file doesn't require changes.
        if args['--in-place'] or os.path.isfile(destination):
            return   # returns None vs True or False
        else:  # Unchanged file needs to be moved over.
            shutil.copy2(source, destination) 
            return False

def get_report(args):
    """Returns a report regarding data aquired during execution
    and stored in args."""
    ret = ("""
Number of html files examined: {}, of which {} were modified. """
                        .format(args['n_html'], args['n_changed']))
    for proprietary_format in args['proprietary_suffixes']:
        size_increase = (args[proprietary_format]['new_size']
                        - args[proprietary_format]['old_size'])
        if size_increase:
            relative_size_increase = (size_increase / 
                            args[proprietary_format]['old_size'])
        else:
            relative_size_increase = 0
        if args[proprietary_format]['n_converted']:
            average_time = (args[proprietary_format]['time_delta'] /
                            args[proprietary_format]['n_converted'])
        else:
            average_time = 0
        if args[proprietary_format]['old_size']:
            time_per_meg_of_original_size = (
                    args[proprietary_format]['time_delta'] /
                    (args[proprietary_format]['old_size'] / 1000000))
        else:
            time_per_meg_of_original_size = 0
#           additional_report += "\n.. so time per meg is meaningless."
        ret = '\n'.join((ret, 
        """{} files encountered: {}, of which {} were converted
                                     but {} failed.
    taking a total time of {} 
        Avg time/file: {}; time/meg of original format: {}.
    Total file space- originals: {:,}, 
                    conversions: {:,}
    for an over all size increase of: {:,}, ({:.1%}.)"""
    .format(proprietary_format,
            args[proprietary_format]['n_encountered'],
            args[proprietary_format]['n_converted'],
            args[proprietary_format]['n_failed'],
            str(args[proprietary_format]['time_delta'])[:-7],
            str(average_time)[:-7],
            str(time_per_meg_of_original_size)[:-7],
            args[proprietary_format]['old_size'],
            args[proprietary_format]['new_size'],
            size_increase,
            relative_size_increase,
            )))
    return ret
        
def traverse_and_change(args):
    """Convert all files found in args['--input']

    Move all files from args['--input'] to args['--output']
    making changes.  args['--input'] must already exit,
    args['--output'] may be the same as args['--input'],
    if not, it may or may not already exist.
    mp4 files will be converted to args['--format'];
    html files will be checked for refs and corrected as need be.
    If destination files are already present in args['--output],
    they will NOT be overwritten UNLESS args['--output'] is the
    same as args['--input']. i.e. Changes are being done in place. 
    If args['--format'] files are found on the input side, this
    will be logged and, if args['--verbose'], a notification sent
    to stdout.
    Depends on log function.
    Returns a final report on what's been done.
    """

    for root, _, files in os.walk(args['--input']):
        message = "Traversing {}".format(root)
        debug(message, args)
        log(message, args)
        source_dir = os.path.abspath(root)
        dest_dir = (source_dir
                    .replace(os.path.abspath(args['--input']),
                            os.path.abspath(args['--output']), 1))

        if not os.path.isdir(dest_dir):
            debug("  Having to create {}".format(dest_dir), args)
            os.mkdir(dest_dir)
            shutil.copymode(source_dir, dest_dir, follow_symlinks=False)
#           shutil.copymode(source_dir, dest_dir)
        for file_name in files:
# $ destination already existed.
# + modified.
# - no need for modification.
            source = os.path.abspath(os.path.join(root, file_name))
            destination = os.path.abspath(
                                os.path.join(dest_dir, file_name))
            debug("    Checking {}".format(file_name), args)
# Deal with html files:
# Algorithm:-----------------------------------------------------------
#                     |   Modified             |   Not Modified        |
# =====================================================================
#      In Place       |  over write source +   |    do nothing -       |
# ---------------------------------------------------------------------
#   Not in place:                                                      |
#      Exists in dest |     do nothing $       |    do nothing $       |
# ----------------------------------------------------------------------
#      Does not exist | write to destination + | copy to destination - |
# ----------------------------------------------------------------------
            if source.endswith(args['html_suffix']):
                debug("      which is an html file.", args)
                args['n_html'] += 1
                html_modified = modify_html(source, destination, args)
# $ destination already existed.
# + modified.
# - no need for modification.
                if html_modified:
                    if args['--in-place']:
                        # overwrite source
                        log("{}: {} +"
                            .format(str(datetime.datetime.now())[:19],
                                    file_name), args)
                        args['n_changed'] += 1
                    else: # not in place
                        if os.path.isfile(destination): # Already done.
                            log("{}: {} $"
                              .format(str(datetime.datetime.now())[:19],
                                        file_name), args)
                        else: # Not in Destination:
                            args['n_changed'] += 1
                            # write to destination already done
                            # by the modify_html function.
                            log("{}: {} +"
                              .format(str(datetime.datetime.now())[:19],
                                        file_name), args)
                else:  # Not modified
                    if args['--in-place']:
                        log("{}: {} -"
                            .format(str(datetime.datetime.now())[:19],
                                    file_name), args)
                    else:  # not in place
                        if os.path.isfile(destination):  # exists in dest
                            log("{}: {} $"
                                .format(str(datetime.datetime.now())[:19],
                                        file_name), args)
                        else:  # Not in destination
                            log("{}: {} -"
                                .format(str(datetime.datetime.now())[:19],
                                        file_name), args)
                            # Source has already been copied to
                            # destination by the modify_html function.
            elif is_target_video_file(source, args):
                debug("      which is a video file.", args)
                # args['current_proprietary_suffix'] is set
                # by is_target_video_file() function.
                args[args['current_proprietary_suffix']]\
                                    ['n_encountered'] += 1
                dest_file = file_name.replace(
                                    args['current_proprietary_suffix'],
                                    args['new_suffix'])
                dest_if_fail = destination
                destination = destination.replace(
                                    args['current_proprietary_suffix'],
                                    args['new_suffix'])
                if os.path.isfile(destination):  # Already converted.
                    log("{}: {} $"
                            .format(str(datetime.datetime.now())[:19],
                                                dest_file), args)
                    continue  
                begin_conversion = datetime.datetime.now()
                return_code = convert_video(source, destination, args)
                end_conversion = datetime.datetime.now()
                conversion_time = end_conversion - begin_conversion
                if return_code:
                    message = ("FAILED ({}) {}"
                                .format(return_code, source))
                    print(message)
                    log(message, args)
                    args[args['current_proprietary_suffix']]\
                        ['time_wasted'] += conversion_time
                    args[args['current_proprietary_suffix']]\
                                        ['n_failed'] += 1
                    if not args['--in-place']:  # Copy unconverted file:
                        if not os.path.isfile(dest_if_fail):
                            shutil.copyfile(source, 
                                            dest_if_fail,
                                            follow_symlinks=False)
                    continue
                else:
                    log("{}: {} => {}"
                            .format(str(datetime.datetime.now())[:19],
                                    file_name,
                                    args['--format']),
                        args)
                    args[args['current_proprietary_suffix']]\
                                        ['n_converted'] += 1
                    args[args['current_proprietary_suffix']]\
                        ['time_delta'] += conversion_time
                    args[args['current_proprietary_suffix']]\
                        ['old_size'] += os.stat(source).st_size
                    args[args['current_proprietary_suffix']]\
                        ['new_size'] += os.stat(destination).st_size
            elif not args['--in-place']: 
                if not (os.path.isfile(destination)  # [1]
                  or os.path.islink(destination)):
                    shutil.copyfile(source, 
                                    destination,
                                    follow_symlinks=False)
            else:
                debug("      which we'll leave as is.",args)
    ret = get_report(args)
    log(ret, args)
    return ret

def main(args):
    if args['--verbose'] or args['--debug']:
        response = input(
        """Root directory of files to be converted is set to..
        {in_dir}
        Output is set to go to..
        {out_dir}
        Format chosen is {form}.
        Log file is set to: {log_file}.
        Status file is set to: {status_file}.
        OK to proceed? (y/n): """.format(in_dir=args['--input'],
                                        out_dir=args['--output'],
                                        form=args['--format'],
                                        log_file=args['--logfile'],
                                        status_file=args['--statusfile'],
                                        ))
        if not response[0] in 'yY':
            print(
    "Re-run the script with desired parameters.")
            sys.exit(0)

    message = ("""
####   Beginning new instance of format_change.py {}"""\
                            .format(str(datetime.datetime.now())[:19]))
    log(message, args)
    if args['--verbose'] or args['--debug']:
        print(message)
    summary_report = traverse_and_change(args)
    if args['--verbose'] or args['--debug']:
        print(summary_report)
    message = ("""
####   Ending current instance of format_change.py {}"""\
                            .format(str(datetime.datetime.now())[:19]))
    log(message, args)
    if args['--verbose'] or args['--debug']:
        print(message)


if __name__ == "__main__":
    print("Running Python3 script: 'format_change.py'.......")
    args = get_args()
    main(args)

# [1]
some_notes = """
There are some problems that arise when dealing with links- in this case
symbolic links.
os.path.isfile(<symlink>) reports on the existence of the target, not the
link itself so if it's a broken link, False will be returned.  In my use
case, it was necessary to add the 'or' and check os.path.islink to avoid
the copyfile raising a file already exists error.
The link appeared broken because it was pointing to a part of the file
system outside of the directories being considered.
os.path.islink(<symlink>) reports what is needed in this situation.
shutil.copy(<symlink>) copies the target of the link, not the link itself.
shutil.copy(<symlink>, follow_symlinks=False) changes the behavior to copy
the link itself which is what was needed in my use case.  Existence of the
target has no bearing.
"""

