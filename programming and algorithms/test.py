from os import listdir
import re
import csv
import slate3k as slate
from gensim.summarization import keywords

# Input.
folder = 'assets/task2/'
n_terms = 5


# Rough cleanup.
def cleanup(pages):
    for i, page in enumerate(pages):
        page = re.sub(r'\\[a-z]*', '', page)
        page = re.sub(r'^.{0,20}$', '', page)
        pages[i] = page

    print(pages)
    return pages


# Process keywords.
def get_keywords(pages, n_terms=5):
    keyword_list = {};
    for key, page in enumerate(pages):
        words = keywords(page, words=n_terms, lemmatize=True, scores=False,
                         pos_filter='NN').split('\n')
        words.sort()
        keyword_list[key] = words
    return keyword_list


# Load all pdf files.
files = [f for f in listdir(folder) if f.endswith('.pdf')]

# Create dict of content.
data = {}
for file in files:
    record = {}
    with open(folder + file, 'rb') as fh:
        doc = slate.PDF(fh)
        record['npages'] = len(doc)
        record['pages'] = cleanup(doc)
        record['keywords'] = get_keywords(record['pages'], n_terms)
    data[file] = record

# Format for csv.
res = []
for filename in data:
    for page_n in data[filename]['keywords']:
        for term in data[filename]['keywords'][page_n]:
            res.append([term, filename, page_n + 1])

# Write to csv.
with open('assets/task2.csv', 'w') as fh:
    fields = ['term', 'file', 'page']
    writer = csv.DictWriter(fh, fieldnames=fields)
    writer.writeheader()
    for record in res:
        writer.writerow({
            'term': record[0],
            'file': record[1],
            'page': record[2],
        })

print(f'Saved {len(res)} records to "assets/task2.csv".')