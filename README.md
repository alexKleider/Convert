#Convert

Work to convert code to 
  1. use docopt and to 
  2. support conversion to webm as well as ogv
has been completed.

Code that uses docopt supports the -h/--help option
and the --version option.

convert2ogv.py was renamed convert_mp4.py.
mod_copy.py no longer exists (deprecated in favour of format_change.py.)

All files with names ending in '.html' will be examined for occurances of 
the string'.mp4' and any found will be changed to the suffix appropriate
for the format selected.
All files with names ending in '.mp4' will be converted and renamed to end
in the suffix appropriate for the format selected. Only ogv and webm are
supported, webm is the default.

This project was motivated by the following:
At the June (or was it May?) 2014 meeting of olpcSF.org, Bruce Baike
introduced us to Rachel [1]. Rachel is a content server running on a
Raspberry Pi [2] with a 32 GB SD card.  Amongst other things, it provides
many if not all of the Khan videos but unfortunately they are all provided
in mp4 format which the OLPC XO laptop can not play.
We are now migrating the project to the Banana Pi.

Running these scripts against the /var/www directory found on the second
partition of Rachel's SD card makes Rachel useful to XO laptop clients.
It's recognized that we'll probably need a higher capacity SD card since the
converted files are likely to be considerably bigger.  A 64 GB card
should do the trick. Stay tuned.


