# This is a sample Python script.

import shutil
import os


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# reads the corpus and
# creates an intermediary file
# containing token and doc_id pairs.

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


# sorts (token, doc_id) pairs
# by token first and then doc_id
def sort(dir):
    f = open(dir + "/intermediate/output.tsv")
    o = open(dir + "/intermediate/output_sorted.tsv", "w")

    # initialize an empty list of pairs of
    # tokens and their doc_ids
    pairs = []

    for line in f:
        line = line[:-1]
        split_line = line.split("\t")
        pair = (split_line[0], split_line[1])
        pairs.append(pair)

    # sort (token, doc_id) pairs by token first and then doc_id
    sorted_pairs = sorted(pairs, key=lambda x: (x[0], x[1]))

    # write sorted pairs to file
    for sp in sorted_pairs:
        o.write(sp[0] + "\t" + sp[1] + "\n")
    o.close()

# converts (token, doc_id) pairs
# into a dictionary of tokens
# and an adjacency list of doc_id
def constructPostings(dir):
    # open file to write postings
    o1 = open(dir + "/intermediate/postings.tsv", "w")

    postings = {}  # initialize our dictionary of terms
    doc_freq = {}  # document frequency for each term

    # read the file containing the sorted pairs
    f = open(dir + "/intermediate/output_sorted.tsv")

    # initialize sorted pairs
    sorted_pairs = []

    # read sorted pairs
    for line in f:
        line = line[:-1]
        split_line = line.split("\t")
        pairs = (split_line[0], split_line[1])
        sorted_pairs.append(pairs)

    # construct postings from sorted pairs
    for pairs in sorted_pairs:
        if pairs[0] not in postings:
            postings[pairs[0]] = []
            postings[pairs[0]].append(pairs[1])
        else:
            len_postings = len(postings[pairs[0]])
            if len_postings >= 1:
                # check for duplicates
                # assuming the doc_ids are sorted
                # the same doc_ids will appear
                # one after another and detected by
                # checking the last element of the postings
                if pairs[1] != postings[pairs[0]][len_postings - 1]:
                    postings[pairs[0]].append(pairs[1])

    # update doc_freq which is the size of postings list
    for token in postings:
        doc_freq[token] = len(postings[token])

    print(postings)
    print(doc_freq)

    # write postings and document frequency to file

    for token in postings:
        o1.write(token+"\t"+str(doc_freq[token])+"\t"+str(postings[token])+"\n")
    o1.close()


# starting the indexing process
def index(dir):
    # reads the corpus and
    # creates an intermediary file
    # containing token and doc_id pairs.
    readCorpus(dir)

    # sorts (token, doc_id) pairs
    # by token first and then doc_id
    sort(dir)

    # converts (token, doc_id) pairs
    # into a dictionary of tokens
    # and an adjacency list of doc_id
    constructPostings(dir)


# Code starts here
if __name__ == '__main__':
    index('corpus/')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
