# -*- coding: utf-8 -*-
import sys
import os
import re
from os import listdir
from os.path import isfile, join, isdir
import tesseract # see https://code.google.com/p/python-tesseract/
import cv2.cv as cv # see http://opencv.org/downloads.html (2.4.9)
import logging
import time
import multiprocessing as mp



def make_raw_ocr(imagefile):
    """Run raw OCR on imagefile using wordlist encanced with music terminology."""

    try:
        if imagefile.endswith("_clean.jpg") and not isfile(imagefile.replace("_clean.jpg","_rawocr.txt")):
            print("Imagefile: %s" % imagefile)

            # set up tesseract
            api = tesseract.TessBaseAPI()

            # set path to tessdata folder (end with /), language
            api.Init("./tessdata/","swe")
            api.SetVariable("load_freq_dawg", "1")
            api.SetVariable("load_system_dawg", "1")

            # custom words in swe.user-words
            api.SetVariable("user_words_suffix", "user-words")

            # limit recognized chars for improved precision
            api.SetVariable("tessedit_char_whitelist", """1234567890abcdeéfghijklmnopqrstuvwxyzöäåABCDEFGHIJKLMNOPQRSTUVWXYZÖÄÅ&"-=.,:;!?[]()""")
            api.SetPageSegMode(tesseract.PSM_AUTO)

            # load image
            image=cv.LoadImage(imagefile, cv.CV_LOAD_IMAGE_GRAYSCALE)
            tesseract.SetCvImage(image,api)

            # get filename to use for raw ocr output.
            textfile = imagefile.replace("_clean.jpg","_rawocr.txt")

            text=api.GetUTF8Text()

            # write text result if confidence score ok
            confidence=api.MeanTextConf()
            print("Length: %s, Confidence score: %s" % (len(text), confidence))

            if confidence > 30 and len(text) > 10:
                with open(textfile, 'wb') as outfile:
                    outfile.write(text)
                    print("Wrote raw ocr to: %s" % textfile)
                # clean up OCR and write cleaned file
                clean_raw_ocr(textfile)

            else:
                print("Confidence score too low.")

            api.End()

        else:
            print("Skipping %s" % imagefile)
            return


    except KeyboardInterrupt:
        print("Abort by user")
        sys.exit()
    except:
        # :-(
        print("Error: %s" % sys.exc_info()[0])



def clean_raw_ocr(fname):
    """Clean the raw ocr output"""

    with open(fname, 'r') as f:
        text = f.read()

    with open(fname.replace("_rawocr.txt", "_cleanocr.txt"), 'wb') as outfile:
        outfile.write(clean_OCR(text))

    print("Clean OCR file %s" % fname.replace("_rawocr.txt", "_cleanocr.txt"))



def clean_OCR(text):
    """Various cleaning of raw OCR output"""
    text = text.strip()

    text = fix_leading_nonalpha(text)

    text = fix_first_line_spacing(text)

    text = fix_dash_linebreaks(text)

    return text


def fix_dash_linebreaks(text):
    return re.sub("(\w)-\n","\\1",text, re.UNICODE)


def fix_leading_nonalpha(text):
    #clean leading non alpha chars
    return re.sub("^[^a-zA-ZåäöÅÄÖ0-9]*","",text, re.UNICODE)


def fix_first_line_spacing(text):
    # collapse spaced name on first line
    lines = text.split("\n")
    first_line = lines[0]
    while re.match("[a-zA-Z0-0öäåÖÄÅ] ", first_line, re.UNICODE):
        first_line = re.sub("([a-zA-Z0-0öäåÖÄÅ]) ", "\\1", first_line, re.UNICODE)

    # combine
    lines[0] = first_line
    text = "\n".join(lines)

    return text




if __name__ == '__main__':
    """Run Tesseract on all <file>_clean.jpg files in startdir

    Uses Pythons multiprocessing to OCR files with Tesseract. Output is stored
    in <file>_rawocr.txt and end result after minor cleanup in
    <file>_cleanocr.txt.
    """


    startdir = sys.argv[1] # abspath
    print("Working on %s" % startdir)

    # iterate over files
    for fdir in listdir(startdir):
        if isdir(join(startdir,fdir)):
            basepath = join(startdir, fdir)
            print("Entering %s" % basepath)

            imgfiles = [join(basepath,f) for f in listdir(join(startdir,fdir)) if isfile(join(basepath,f))]

            pool = mp.Pool()
            pool.map(make_raw_ocr, imgfiles)
