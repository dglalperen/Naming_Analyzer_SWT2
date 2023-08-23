```python
#! /usr/bin/env python

import os
import sys
import glob
import time
import re
import urllib2
import json

username = "oapdf1"
doilinkdir = '../doilink'

working_dir = os.path.abspath('.')
now_dir = os.path.basename(os.path.abspath(os.path.curdir))


def doi_decompose(suffix):
    length = len(suffix)
    if length <= 5:
        return ""
    layer = (length - 1) // 5
    dir_url = ""
    for i in range(layer):
        # In Windows, directory name can't end with '.'
        dir_url += suffix[i * 5:(i + 1) * 5].rstrip('.') + "/"
    return dir_url


def quote_file_doi(doi):
    '''Quote the doi name for a file name'''
    return urllib2.quote(doi, '+/()').replace('/', '@')


def unquote_file_doi(doi):
    '''Unquote the doi name for a file name'''
    return urllib2.unquote(doi.replace('@', '/'))


def is_oapdf(doi, check=False):
    '''Check if the doi is in OAPDF library'''
    if check and "/" not in doi and "@" in doi:
        doi = unquote_file_doi(doi)
    try:  # urllib may be faster than requests
        r = urllib2.urlopen("http://oapdf.github.io/doilink/pages/" + doi_decompose(doi, url=True) + ".html")
        return r.code == 200
    except:
        return False


out_dict = {"owner": username, "repo": now_dir}
file_move = {}
file_count = 0
ig = glob.iglob("10.*/10.*.pdf")
for file in ig:
    file_size = os.path.getsize(file)
    file_move[file] = file_size
    file_count += 1

file_move_file_name = {}
for key, value in file_move.items():
    file_name = os.path.split(key)[1]
    file_move_file_name[file_name] = value
    sout = file_move_file_name

out_dict['total'] = file_count
out_dict['items'] = file_move_file_name

file = open(doilinkdir + os.sep + now_dir + "@" + username + ".json", 'w')
file.write(json.dumps(out_dict))
file.close()

file_move.clear()
file_move_file_name.clear()
```
``````python
#! /usr/bin/env python

import os
import sys
import glob
import time
import re
import urllib2
import json

username = "oapdf1"
doilinkdir = '../doilink'

working_dir = os.path.abspath('.')
now_dir = os.path.basename(os.path.abspath(os.path.curdir))


def decompose_doi(suffix):
    lens = len(suffix)
    if lens <= 5:
        return ""
    layer = (lens - 1) // 5
    dir_url = ""
    for i in range(layer):
        # In Windows, directory name can't end with '.'
        dir_url += suffix[i * 5:(i + 1) * 5].rstrip('.') + "/"
    return dir_url


def quote_file_doi(doi):
    '''Quote the doi name for a file name'''
    return urllib2.quote(doi, '+/()').replace('/', '@')


def unquote_file_doi(doi):
    '''Unquote the doi name for a file name'''
    return urllib2.unquote(doi.replace('@', '/'))


def is_oapdf(doi, check=False):
    '''Check if the doi is in OAPDF library'''
    if check and "/" not in doi and "@" in doi:
        doi = unquote_file_doi(doi)
    try:  # urllib may be faster than requests
        r = urllib2.urlopen("http://oapdf.github.io/doilink/pages/" + decompose_doi(doi, url=True) + ".html")
        return r.code == 200
    except:
        return False


out_dict = {"owner": username, "repo": now_dir}
file_move = {}
file_count = 0
ig = glob.iglob("10.*/10.*.pdf")
for f in ig:
    file_size = os.path.getsize(f)
    file_move[f] = file_size
    file_count += 1

file_move_fname = {}
for k, v in file_move.items():
    file_name = os.path.split(k)[1]
    file_move_fname[file_name] = v
    sout = (file_move_fname)

out_dict['total'] = file_count
out_dict['items'] = file_move_fname

f = open(doilinkdir + os.sep + now_dir + "@" + username + ".json", 'w')
f.write(json.dumps(out_dict))
f.close()

file_move.clear()
file_move_fname.clear()
```
```