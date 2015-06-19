#Convert

format_change.py is a utility created for the pupose of replacing
proprietary video format fiiles with equivalent unrestricted formats.

To date, .mp4 and .flv video file conversions are supported.
Support is included for conversion to either .webm or .ogv.

Try:
./format_change.py -h
for usage information.

This project was motivated by the following:
At the June (or was it May?) 2014 meeting of olpcSF.org, Bruce Baike
introduced us to Rachel [1]. Rachel is a content server running on a
Raspberry Pi [2] with a 32 GB SD card.  Amongst other things, it provides
many if not all of the Khan videos but unfortunately they are all provided
in mp4 format which the OLPC XO laptop can not play.  There is other
content provided in .flv format.

We have migrated the project to the Banana Pi and to the Raspberry Pi B2.

Running these scripts against the /var/www directory found on the second
partition of Rachel's SD card makes Rachel useful to XO laptop clients.
Because both .ogv and .webm files are considerably bigger in size than
.mp4 files (this proves not to be the case for .flv files,) the converted
version of Rachel requires a 64 GB SD card, rather than 32.


