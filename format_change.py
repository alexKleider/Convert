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
    format_change.py [options] --in_place

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
  --in_place    Make changes to the source directory rather than 
                              creating a new one.

This script traverses the IN_DIR directory (or current working
directory if none is provided) looking for html and mp4 files.
If OUT_DIR is specified, another directory structure is created
incorporating the changes, leaving the original unchanged.
If --in_place is specified, original files are modified.
The content of all html files are examined and any references to '.mp4'
are changed to the suffix appropriate to the FORMAT specified.
All mp4 files are converted into the FORMAT specified.
The only two formats currently supported are webm and ogv.
If not specified, FORMAT defaults to webm.

format_change.py combines the functionality of both convert_mp4.py and
scan4html.py into one script.  It supports preservation of the original
directory, not provided in the other two scripts.

Recently added functionality which provides converson times
and comparison of file size before and after conversion.
"""

import os
import sys
import shlex
import shutil
import datetime
import subprocess
from docopt import docopt
import spot

OLD_SUFFIX = '.mp4'
ENCODING = "latin-1"

def get_args():
    """Sets and returns globals (as a dictionary.)
    
    Use docopt to collect command line arguments, 
    and sets up other globals.
    Causes termination if invalid format is given.
    """
    args = docopt(__doc__, version=spot.VERSION)
    args['--input'] = (
        os.path.abspath(os.path.expanduser(
                                    args['--input'])))
    args['--logfile'] = (
        os.path.abspath(os.path.expanduser(
                                    args['--logfile'])))
    if args['--in_place']:
        args['--output'] = args['--input']
    else:
        args['--output'] = (
            os.path.abspath(os.path.expanduser(
                                        args['--output'])))
    args['html_suffix'] = '.html'
    args['old_suffix'] = OLD_SUFFIX
    if args['--format'] == 'ogv':
        args['new_suffix'] = '.ogv'
        args['command'] =' '.join(("avconv -flags qscale",
            "-global_quality 1 -i {} -acodec libvorbis {}"))
    elif args['--format'] == 'webm':
        args['new_suffix'] = '.webm'
        args['command'] =' '.join(("avconv -flags qscale",
                            "-global_quality 1 -i {} -y {}"))
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

def convert_video(source, destination, args):
    """Convert to alternate video format.
    
    Format of source is assumed to be mp4.
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
        message = ("{}: {} => return code >0."
                    .format(datetime.datetime.now()[:24], source))
        log(message, args)
        report(message, args)
    else:
        shutil.copymode(source, destination, follow_symlinks=False)
#       shutil.copymode(source, destination)
    return return_code

def convert_text(text, old, new):
    """Text replacement.

    All three parameters are strings. 
    Any occurrence of the second parameter in the first
    is replaced by the third.
    Returns altered text or None if no alterations were done.
    """
    if text.find(old) >= 0:
        return text.replace(old[1:], new[1:])

def modify_html(source, destination, args):
    """Modifies the text in .html files.
    
    Changes each instance of '.mp4' in source to the suffix appropriate
    to args['--format'] in destination.
    Returns True if modifications were necessary, False if not.
    If modifications are not necessary, still moves source to
    destination.
    """
    with open(source, 'r', encoding=ENCODING) as source_file:
        file_content = source_file.read()
        content = convert_text(file_content, 
                                args['old_suffix'],
                                args['new_suffix'],)
    if content:
        with open(destination, 'w', 
                    encoding=ENCODING) as destination_file:
            destination_file.write(content)
        shutil.copymode(source, destination, follow_symlinks=False)
        return True
    else:  # file doesn't require changes.
        if args['--in_place'] or os.path.isfile(destination):
            return   # returns None vs True or False
        else:  # Unchanged file needs to be moved over.
            shutil.copy2(source, destination) 
            return False
        
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
    final_report = ("""
Completed with {n_files} files checked:
    Attempted {n_videos} video conversions, {n_failed} failed.
    {n_html} html files encountered, {n_changed} required changing.
    Time to convert {n_converted_videos} videos: {time_taken}.
    Total of sizes of all input video files: {mp4_size}
                  of all output video files: {new_format_size}
    for an average time per file: {time_per_file}
     time per megabite of source: {time_per_meg}.
    Extra disk space required: {size_diff}, {percent_diff}%.""")

    n_files = 0     # $ destination already existed.
    n_videos = 0     # + modified.
    n_failed = 0    # - no need for modification.
    time_taken = datetime.timedelta(0, 0, 0)
    mp4_size = 0
    new_format_size = 0
    n_html = 0
    n_changed = 0

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
            source = os.path.abspath(os.path.join(root, file_name))
            destination = os.path.abspath(
                                os.path.join(dest_dir, file_name))
            debug("    Checking {}".format(file_name), args)
            n_files += 1
            if source.endswith(args['html_suffix']):
                debug("      which is an html file.", args)
                n_html += 1
                html_modified = modify_html(source, destination, args)
                if html_modified == None:  # source != dest & dest exists.
                    log("{}: {} $"
                        .format(str(datetime.datetime.now())[:19],
                                file_name), args)
                elif html_modified:
                    log("{}: {} +"
                        .format(str(datetime.datetime.now())[:19],
                                file_name), args)
                    n_changed += 1
                else:
                    log("{}: {} -"
                        .format(str(datetime.datetime.now())[:19],
                                file_name), args)
            elif source.endswith(args['old_suffix']):
                debug("      which is a video file.", args)
                n_videos += 1
                dest_file = file_name.replace(
                                    args['old_suffix'],
                                    args['new_suffix'])
                destination = destination.replace(
                                    args['old_suffix'],
                                    args['new_suffix'])
                if os.path.isfile(destination):  # Already converted.
                    log("{}: {} $".\
                                format(str(datetime.datetime.now())[:19],
                                                dest_file), args)
                    continue  
                begin_conversion = datetime.datetime.now()
                return_code = convert_video(source, destination, args)
                end_conversion = datetime.datetime.now()
                log("{}: {} => {}"
                        .format(str(datetime.datetime.now())[:19],
                                file_name,
                                args['--format']),
                    args)
                if return_code:
                    message = ("!!!!!!!!!Return_code is {}."
                                        .format(return_code))
                    print(message)
                    log(message, args)
                    n_failed += 1
                    continue
                else:
                    time_taken += end_conversion - begin_conversion
                    mp4_size += os.stat(source).st_size
                    new_format_size += os.stat(destination).st_size

            elif not args['--in_place']: 
                if not (os.path.isfile(destination)  # [1]
                  or os.path.islink(destination)):
                    shutil.copyfile(source, 
                                    destination,
                                    follow_symlinks=False)
            else:
                debug("      which we'll leave as is.",args)


    n_converted_videos = n_videos - n_failed
    time_per_file = time_taken / n_converted_videos
    time_per_meg = time_taken / (mp4_size / 1000000)
    size_diff = new_format_size - mp4_size
    percent_diff = size_diff / mp4_size * 100

    return final_report.format(n_files = n_files, 
                            n_videos = n_videos, 
                            n_failed = n_failed, 
                            n_html = n_html,
                            n_changed = n_changed,
                            n_converted_videos = n_converted_videos,
                            time_taken = time_taken,
                            mp4_size = mp4_size,
                            new_format_size = new_format_size,
                            time_per_file = time_per_file,
                            time_per_meg = time_per_meg,
                            size_diff = size_diff,
                            percent_diff = percent_diff
                            )

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

