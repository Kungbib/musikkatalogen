# -*- coding: utf-8 -*-
import sys
import os
from os import listdir
from os.path import isfile, join, isdir
import multiprocessing as mp


def process_it(fh):
    if fh.endswith(".jpg") and (not "_clean" in fh) and (not "_view500" in fh):

        imagefile = fh
        cleanfile = fh.replace(".jpg", "_clean.jpg")

        if not isfile(cleanfile):
            os.system("convert '%s' -chop 0x170 -blur 1x65535 -contrast -normalize -despeckle -despeckle -sharpen 1 -posterize 3 '%s'" % (imagefile, cleanfile))
            print("Created: %s" % cleanfile)
        else:
            print("Skipping: %s" % cleanfile)



if __name__ == '__main__':
    """Generate a cleaned image for OCR processing

    Processes all files in subfolders given a starting path. Output files are
    saved to the same folder and appended with "_clean" in the filename.
    Existing files will not be overwritten.

    Requires a local installation of Imagemagick (convert command).
    See process_it for imagemagick parameters (the convert command).

    Example use: python makecleanimg.py /my/folder/path
    """

    startdir = sys.argv[1] # abspath
    print("Working on %s" % startdir)


    # iterate over files
    for fdir in listdir(startdir):
        if isdir(join(startdir,fdir)):
            basepath = join(startdir, fdir)

            imgfiles = [join(basepath,f) for f in listdir(join(startdir,fdir)) if isfile(join(basepath,f))]

            pool = mp.Pool()
            pool.map(process_it, imgfiles)

