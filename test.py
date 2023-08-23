from rate_repository import split_into_chunks
from utils import clone_repo

dir = './repos/oapdf1/OAPDF_11/gendoipage.py'
print('start cloning')

with open(dir, "r") as f:
    code_snippet = f.read()
test = split_into_chunks(code_snippet, 6000)

print(test)

