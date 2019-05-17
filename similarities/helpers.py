from nltk.tokenize import sent_tokenize

def lines(a, b):
    """Return lines in both a and b"""
    #take in string input a and split
    list_a = set()
    list_b = set()

    z = []

    list_a = a.splitlines()
    list_a = set(list_a)

    list_b = b.splitlines()
    list_b = set(list_b)

    z = list(list_a & list_b)
    return z 


def sentences(a, b):
    """Return sentences in both a and b"""
    sentence = []

    sent_a = set()
    sent_a = sent_tokenize(a)
    sent_b = set()
    sent_b = sent_tokenize(b)

    sent_a = set(sent_a)
    sent_b = set(sent_b)

    sentence = list(sent_a & sent_b)
    return sentence


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    return list(set(list_1(a, n)).intersection(list_1(b,n)))

def list_1(a, n):
    
    return [a[i: i + n] for i in range(len(a) - (n - 1))]
    

