#Convert

Current work (as of Feb 2014) has been to convert code to use docopt
and to support conversion to webm as well as ogv.
Already completed is convert_mp4.py (a rename of convert2ogv.py.)
and scan4html.py


In early Sept 2014, both modules (convert2ogv.py and scan4html.py) were
combined into mod_copy.py.  The former two have been 'upgraded' to
support command line arguments (with docopt) rather than having them
hard coded. The same has yet to be done for mod_copy.  Until this is 
done, the following documentation applies:


Declared within the code (of mod_copy) are two directories: one exists-
the source, the other will be created- the destination.

All files with names ending in '.html' will be examined for occurances of 
the string'mp4' and any found will be changed to 'ogv'.
All files with names ending in '.mp4' will be converted and renamed to end
in '.ogv'.  
All files whether modified or not, will be copied, preserving permissions,
to the destination directory.
Each action is logged to a file called 'log.log'.

This project was motivated by the following:
At the June (or was it May?) meeting of olpcSF.org, Bruce Baike introduced
us to Rachel [1]. Rachel is a content server running on a Raspberry Pi [2] 
with a 32 GB SD card.  Amongst other things, it provides many if not all of
the Khan videos but unfortunately they are all provided in mp4 format which
the OLPC XO laptop can not play.

Running these scripts against the /var/www directory found on the second
partition of Rachel's SD card makes Rachel useful to XO laptop clients.
It's recognized that we'll probably need a higher capacity SD card since the
converted files are likely to be considerably bigger.  A 64 GB card
should do the trick. Stay tuned.


For historical reasons, the text of the original README file follows:
"""
These utilities accept a directory tree, beneath which there are assumed 
to be html and mp4 files with the latter being referenced in the former.

All references to files with names ending with '.mp4' contained in files
with the '.html' suffix are renamed such that the '.mp4' is replaced by 
'.ogv'.  This is done by scan4html.py

All mp4 files are deleted after being converted to ogv (Vorbis for audio
and Theora for video) format.  This is done by convert2ogv.py.

If all is successful, the result should be transparent. i.e. Most users of
the directory tree will notice no difference.
The motive is to allow access to users unable to play mp4 video; more
specifically, to allow content to be accessible to the OLPC XO laptops.

Some thought has been given to the possibility of using scan4html.py and
convert2ogv.py as modules to support a mp42ogv.py script which will perform
both tasks.  As of now, there hasn't been the interest in moving forward
with this.  

Glen Jarvis has become a useful critic and collaborator and has introduced
the use of pylint.  The situation is a little complicated by the fact these
scripts have been written in Python 3 but I can't get the appropriate
version of pylint to work on my system.  Except for criticism of 'input' vs
'raw_input', this doesn't seem to be too much of a problem.
"""

