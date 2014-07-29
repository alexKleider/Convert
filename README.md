#mp42ogv.py

This utility accepts a directory tree, beneath which there are assumed 
to be html and mp4 files with the latter being referenced in the former.

All references to files with names ending with '.mp4' contained in files
with the '.html' suffix are renamed such that the '.mp4' is replaced by 
'.ogv'.

All mp4 files are deleted after being converted to ogv (Vorbis for audio
and Theora for video) format.

If all is successful, the result should be transparent. i.e. Most users of
the directory tree will notice no difference.
The motive is to allow access to users unable to play mp4 video; more
specifically, to allow content to be accessible to the OLPC XO laptops.

As of now, `mp42ogv.py` does not exist.
Instead there is `convert2ogv.py3` which converts the ogv files to mp4
and `scan4html.py3` which changes the link references.

