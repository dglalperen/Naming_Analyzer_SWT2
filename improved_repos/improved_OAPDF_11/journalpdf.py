#! /usr/bin/env python

import os
import sys
import glob
import time
import re
import requests
import urllib.parse
import json

requests.packages.urllib3.disable_warnings()


def decompose_suffix(suffix):
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
    """Quote the doi name for a file name"""
    return urllib.parse.quote(doi, safe='+/()').replace('/', '@')


def unquote_file_doi(doi):
    """Unquote the doi name for a file name"""
    return urllib.parse.unquote(doi.replace('@', '/'))


def max_issn(issns):
    max_issn = "0000-0000"
    max_num = 0
    for i in range(len(issns)):
        if issns[i] > max_issn:
            max_issn = issns[i]
            max_num = i
            continue
    return issns[max_num]


def get_pdf_dir(doi):
    """Get only the larger issn, should normal doi"""
    # try:
    r = requests.get('https://api.crossref.org/works/' + doi)
    j = json.loads(r.text)
    item = j['message']
    volume = item.get('volume', '0')
    issue = item.get('issue', '0')
    issn = max_issn(item.get('ISSN', ['9999-9999']))
    return issn + os.sep + volume + os.sep + issue + os.sep
    # except:
    #     return ""


for f in glob.iglob('10.*/10.*.pdf'):
    paths = os.path.split(f)
    doi = unquote_file_doi(os.path.splitext(paths[1])[0]).strip()
    os.renames(f, paths[0] + os.sep + get_pdf_dir(doi) + paths[1])#! /usr/bin/env python

import os
import sys
import glob
import time
import re
import requests
import urllib.parse
import json

requests.packages.urllib3.disable_warnings()


def decompose_suffix(suffix):
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
    """Quote the doi name for a file name"""
    return urllib.parse.quote(doi, safe='+/()').replace('/', '@')


def unquote_file_doi(doi):
    """Unquote the doi name for a file name"""
    return urllib.parse.unquote(doi.replace('@', '/'))


def max_issn(issns):
    max_issn = "0000-0000"
    max_num = 0
    for i in range(len(issns)):
        if issns[i] > max_issn:
            max_issn = issns[i]
            max_num = i
            continue
    return issns[max_num]


def get_pdf_dir(doi):
    """Get only the larger issn, should normal doi"""
    # try:
    r = requests.get('https://api.crossref.org/works/' + doi)
    j = json.loads(r.text)
    item = j['message']
    volume = item.get('volume', '0')
    issue = item.get('issue', '0')
    issn = max_issn(item.get('ISSN', ['9999-9999']))
    return issn + os.sep + volume + os.sep + issue + os.sep
    # except:
    #     return ""


for f in glob.iglob('10.*/10.*.pdf'):
    paths = os.path.split(f)
    doi = unquote_file_doi(os.path.splitext(paths[1])[0]).strip()
    os.renames(f, paths[0] + os.sep + get_pdf_dir(doi) + paths[1])