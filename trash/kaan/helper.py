import os
import re

def find_py_files_in_dir(dir_path):
    # find all python files in a given directory
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.py'):
                yield os.path.join(root, file)

def find_term_in_file(file_path, term):
    # search for a term in a given python file
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    if re.search(r'\b' + re.escape(term) + r'\b', content):
        return True
    return False


if __name__ == "__main__":
    dir_path = "./httpolice-master"
    term = 'Upgrade'
    for file_path in find_py_files_in_dir(dir_path):
        if find_term_in_file(file_path, term):
            print(f"Term '{term}' found in: {file_path}")

    from wordsegment import load, segment
    import nltk
    from nltk.corpus import words
    from nltk.stem import WordNetLemmatizer

    load()
    # Create a set of English words for later use
    english_words = set(words.words())
    word = 'pygments'
    word = word.lower()
    lemmatizer = WordNetLemmatizer()

    word = lemmatizer.lemmatize(word)
    if word in english_words:
        print('ist englisch')
    print(segment(word))

