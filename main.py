# This is a sample Python script.

import shutil
import os


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def readCorpus(dir):
    doc_id = 1
    o = open(dir + "/intermediate/output.tsv", "w")
    for f in os.listdir(dir):
        if f.endswith(".txt"):
            f1 = open(dir + "/" + f)
            for line in f1:
                tokens = line.split(" ")
                for t in tokens:
                    o.write(t.lower() + "\t" + str(doc_id) + "\n")
            f1.close()
            doc_id = doc_id + 1
    o.close()


def sort(dir):
    f = open(dir + "/intermediate/output.tsv")
    o = open(dir + "/intermediate/output_sorted.tsv", "w")
    # initialize an empty list of pairs of
    # tokens and their doc_ids
    pairs = []
    for line in f:
        line = line[:-1]
        split_line = line.split("\t")
        y = (split_line[0], split_line[1])
        pairs.append(y)
    sorted_pairs = sorted(pairs, key=lambda x: (x[0], x[1]))
    for sp in sorted_pairs:
        o.write(sp[0] + "\t" + sp[1] + "\n")
    o.close()


def constructPostings(dir):
    # read the file containing the stored pairs
    f = open(dir + "/intermediate/output_sorted.tsv")

    sorted_pairs = []

    postings = {}  # initialize our dictionary of terms
    doc_freq = {}  # document frequency for each term

    for line in f:
        line = line[:-1]
        split_line = line.split("\t")
        pairs = (split_line[0], split_line[1])
        sorted_pairs.append(pairs)
    for pairs in sorted_pairs:
        if pairs[0] not in postings:
            postings[pairs[0]] = []
            postings[pairs[0]].append(pairs[1])
        else:
            len_postings = len(postings[pairs[0]])
            if len_postings >= 1:
                # check for duplicates
                if pairs[1] != postings[pairs[0]][len_postings - 1]:
                    postings[pairs[0]].append(pairs[1])

    for token in postings:
        doc_freq[token] = len(postings[token])

    print(postings)
    print(doc_freq)


# starting the indexing process
def index(dir):
    # reads the corpus and
    # creates an intermediary file
    # containing token and doc_id pairs.
    readCorpus(dir)
    sort(dir)
    constructPostings(dir)


# Code starts here
if __name__ == '__main__':
    index('corpus/')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
