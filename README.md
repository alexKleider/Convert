#mp42ogv

These utilities accepts a directory tree, beneath which there are assumed 
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
with this.  What has been done is described next.

Glen Jarvis has become a useful critic and collaborator and has introduced
the use of pylint.  The situation is a little complicated by the fact these
scripts have been written in Python 3 but I can't get the appropriate
version of pylint to work on my system.  Except for criticism of 'input' vs
'raw_input', this doesn't seem to be too much of a problem.
Beware that the code has NOT been tested since modification to 'make'
pylint less displeased:-)


