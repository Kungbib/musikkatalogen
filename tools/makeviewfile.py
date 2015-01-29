# -*- coding: utf-8 -*-
import sys
import os
import re
from os import listdir
from os.path import isfile, join, isdir
import time
import multiprocessing as mp


def make_viewfile(fname):

    viewfile = fname.replace(".jpg", "_view500.jpg")

    # skip if exists
    if not isfile(viewfile):
        os.system("convert %s -resize 500 %s" % (fname, viewfile))
        print("Wrote %s" % viewfile)
    else:
        print("Skipped %s" % fname)


if __name__ == '__main__':
    """Generate 500px wide preview files

    Files will not be overwritten. New files created in source folder with
    "_view500" in filename.

    Requires a local installation of Imagemagick (convert command).

    Example use: python makeviewfile.py /my/folder/path
    """

    startdir = sys.argv[1] # abspath
    print "Working on %s" % startdir

    # iterate over files
    for fdir in listdir(startdir):
        if isdir(join(startdir,fdir)):
            basepath = join(startdir, fdir)
            print("Entering %s" % basepath)

            imgfiles = [join(basepath,f) for f in listdir(join(startdir,fdir)) if f.endswith(".jpg") and (not "view500" in f) and (not "_clean" in f)]

            print("\n\nFilecount %s" % len(imgfiles))

            pool = mp.Pool()
            pool.map(make_viewfile, imgfiles)
