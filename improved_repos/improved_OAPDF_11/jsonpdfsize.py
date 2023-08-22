```python
import os
import sys
import glob
import time
import re
import urllib.request
import json

username = "oapdf1"
doilinkdir = '../doilink'

working_dir = os.path.abspath('.')
now_dir = os.path.basename(os.path.abspath(os.getcwd()))

def doi_decompose(suffix):
    length = len(suffix)
    if length <= 5:
        return ""
    layer = (length - 1) // 5
    dir_url = ""
    for i in range(layer):
        dir_url += suffix[i*5:(i+1)*5].rstrip('.') + "/"
    return dir_url

def quote_file_doi(doi):
    """Quote the doi name for a file name."""
    return urllib.request.quote(doi, safe='+/()').replace('/', '@')

def unquote_file_doi(doi):
    """Unquote the doi name for a file name."""
    return urllib.request.unquote(doi.replace('@', '/'))

def is_oapdf(doi, check=False):
    """Check if the doi is in the OAPDF library."""
    if check and "/" not in doi and "@" in doi:
        doi = unquote_file_doi(doi)
    try:
        with urllib.request.urlopen("http://oapdf.github.io/doilink/pages/" + doi_decompose(doi, url=True) + ".html") as r:
            return r.code == 200
    except:
        return False

out_dict = {"owner": username, "repo": now_dir}
f_move = {}
f_count = 0
ig = glob.iglob("10.*/10.*.pdf")
for f in ig:
    f_size = os.path.getsize(f)
    f_move[f] = f_size
    f_count += 1

f_move_fname = {}
for k, v in f_move.items():
    fname = os.path.split(k)[1]
    f_move_fname[fname] = v

out_dict['total'] = f_count
out_dict['items'] = f_move_fname

with open(doilinkdir + os.sep + now_dir + "@" + username + ".json", 'w') as f:
    f.write(json.dumps(out_dict))

f_move.clear()
f_move_fname.clear()
```

Explanation of changes made:

- Imported `urllib.request` instead of `urllib2` as `urllib2` was removed in Python 3.
- Renamed variables `workingdir` and `nowdir` to `working_dir` and `now_dir` respectively to follow the snake_case naming convention.
- Renamed functions `doidecompose`, `quotefileDOI`, `unquotefileDOI`, and `is_oapdf` to `doi_decompose`, `quote_file_doi`, `unquote_file_doi`, and `is_oapdf` respectively to follow the snake_case naming convention.
- Used a more descriptive variable name `dir_url` instead of `dirurl` in the `doi_decompose` function.
- Updated the use of `urllib.quote` and `urllib.unquote` to `urllib.request.quote` and `urllib.request.unquote` respectively.
- Added a docstring to the functions `quote_file_doi` and `unquote_file_doi`.
- Added a docstring to the `is_oapdf` function and updated the check for the doi being in the OAPDF library.
- Renamed variables `outdict`, `fmove`, `fcount`, `ig`, and `fmovefname` to `out_dict`, `f_move`, `f_count`, `ig`, and `f_move_fname` respectively to follow the snake_case naming convention.
- Added a `with` statement when opening the file to ensure it is properly closed.