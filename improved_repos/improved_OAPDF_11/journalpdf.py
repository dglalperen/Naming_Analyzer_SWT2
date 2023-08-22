****
Proposed Changes:

1. Line 3: Remove unnecessary import statements and organize them according to PEP 8 guidelines.
2. Line 4: Remove unnecessary import statement as it is not used in the code.
3. Lines 7-22: Rename the function "doidecompose" to "decompose_doi" for clarity and consistency. Update variable names to be more descriptive and follow the snake_case naming convention.
4. Lines 25-27: Rename the function "quotefileDOI" to "quote_file_doi" for clarity and consistency.
5. Lines 30-32: Rename the function "unquotefileDOI" to "unquote_file_doi" for clarity and consistency.
6. Lines 35-44: Rename the function "maxissn" to "get_max_issn" for clarity and consistency. Update variable names to be more descriptive and follow the snake_case naming convention.
7. Lines 47-55: Rename the function "getpdfdir" to "get_pdf_dir" for clarity and consistency. Update comments to be capitalized and follow the sentence case convention. Update variable names to be more descriptive and follow the snake_case naming convention.
8. Lines 59-63: Rename the variable "f" to "file_path" for clarity.
9. Lines 64-65: Rename the variable "doi" to "quoted_doi" for clarity. Update comments to be capitalized and follow the sentence case convention.
10. Line 66: Use os.path.join instead of string concatenation for better cross-platform compatibility.

These changes enhance the clarity, descriptiveness, and consistency of the code. They also align with PEP 8 guidelines for Python code.
****