#! /usr/bin/env python

#### Usage:
# put this script in a repository root directory 
# It will scan the whole subdir pdf and generate html link for it in "html" and "pages" subdirectory

# Update: 2016.1.19 3:26AM

import os
import sys
import glob
import re
import requests
import urllib2

# User link for repository
user_link = "https://github.com/oapdf1/"
# Setup the doilink dir

# doilink dir is for doilink saving
doilink_dir = "../doilink/"
out_doilink_dir = doilink_dir + "pages/"

# oapdfdir="../doilink/"
oapdf_dir = "_pages/"
out_dir = "pages/"
if oapdf_dir:
    out_dir = oapdf_dir + out_dir
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

# Force rewrite the existing file
force = False
combine = False
# Default method
post_combine = True

if len(sys.argv) > 1:
    if sys.argv[1] == 'f':
        force = True
        post_combine = False
    elif sys.argv[1] == 'c':
        combine = True
        post_combine = False
    elif sys.argv[1] == 'n':
        post_combine = False

now_dir = os.path.basename(os.path.abspath(os.path.curdir))
p = re.compile(r"<title>.*?</title>")
pl = re.compile(r'(?<=<a href=\")http.*?(?=\">)')
ph = re.compile(r"</head>")

########## Function


def doi_decompose(suffix):
    lens = len(suffix)
    if lens <= 5:
        return ""
    layer = (lens - 1) / 5
    dir_url = ""
    for i in range(layer):
        ## In window, dir name can't end at '.'
        dir_url += suffix[i * 5:(i + 1) * 5].rstrip('.') + "/"
    return dir_url


def quote_file_DOI(doi):
    '''Quote the doi name for a file name'''
    return urllib2.quote(doi, '+/()').replace('/', '@')


def unquote_file_DOI(doi):
    '''Unquote the doi name for a file name'''
    return urllib2.unquote(doi.replace('@', '/'))


def decompose_DOI(doi, url=False, out_dir=False, out_list=False, length=5):
    '''Decompose doi to a list or a url needed string.
    Only decompose the quoted suffix and prefix will be reserved.
    Note that dir name can't end with '.', so the right ends '.' will be delete here.
    Note that only support standard doi name, not prefix@suffix!
    If error, return "".

    Default, decompose to a dir name (related to doi).
    If url, output url string (containing quoted doi name)
    If out_dir, output string for directory of doi
    If out_list, output to a list including quoted doi'''
    doi_split = doi.split('/', 1)
    if len(doi_split) != 2:
        print "Error Input DOI:", doi.encode('utf-8')
        return ""
    prefix = doi_split[0]
    suffix = quote_file_DOI(doi_split[1])
#! /usr/bin/env python

#### Usage:
# put this script in a repository root directory 
# It will scan the whole subdir pdf and generate html link for it in "html" and "pages" subdirectory

# Update: 2016.1.19 3:26AM

import os
import sys
import glob
import re
import requests
import urllib2

# User link for repository
user_link = "https://github.com/oapdf1/"
# Setup the doilink dir

# doilink dir is for doilink saving
doilink_dir = "../doilink/"
out_doilink_dir = doilink_dir + "pages/"

# oapdfdir="../doilink/"
oapdf_dir = "_pages/"
out_dir = "pages/"
if oapdf_dir:
    out_dir = oapdf_dir + out_dir
# if (not os.path.exists("html")): os.makedirs("html")
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

# Force rewrite the existing file
force = False
combine = False
# Default method
post_combine = True

if len(sys.argv) > 1:
    if sys.argv[1] == 'f':
        force = True
        post_combine = False
    elif sys.argv[1] == 'c':
        combine = True
        post_combine = False
    elif sys.argv[1] == 'n':
        post_combine = False

now_dir = os.path.basename(os.path.abspath(os.path.curdir))
p = re.compile(r"<title>.*?</title>")
pl = re.compile(r'(?<=<a href=\")http.*?(?=\">)')
ph = re.compile(r"</head>")

########## Function


def doi_decompose(suffix):
    lens = len(suffix)
    if lens <= 5:
        return ""
    layer = (lens - 1) / 5
    dir_url = ""
    for i in range(layer):
        ## In window, dir name can't end at '.'
        dir_url += suffix[i * 5:(i + 1) * 5].rstrip('.') + "/"
    return dir_url


def quote_file_DOI(doi):
    '''Quote the doi name for a file name'''
    return urllib2.quote(doi, '+/()').replace('/', '@')


def unquote_file_DOI(doi):
    '''Unquote the doi name for a file name'''
    return urllib2.unquote(doi.replace('@', '/'))


def decompose_DOI(doi, url=False, out_dir=False, out_list=False, length=5):
    '''Decompose doi to a list or a url needed string.
    Only decompose the quoted suffix and prefix will be reserved.
    Note that dir name can't end with '.', so the right ends '.' will be delete here.
    Note that only support standard doi name, not prefix@suffix!
    If error, return "".

    Default, decompose to a dir name (related to doi).
    If url, output url string (containing quoted doi name)
    If out_dir, output string for directory of doi
    If out_list, output to a list including quoted doi'''
    doisplit = doi.split('/', 1)
    if len(doisplit) != 2:
        print "Error Input DOI:", doi.encode('utf-8')
        return ""
    prefix = doisplit