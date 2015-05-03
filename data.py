from __future__ import division
import unicodedata,re,query,math
from nltk.tokenize import sent_tokenize, word_tokenize

_sents = None
_r_citations = re.compile(r'\[\d+\]|\[citation needed\]')

def filter_citations(str):
    return re.sub(_r_citations,'',str)

def tokenize_file(file):
    global _sents
    f = open(file, 'r')
    text = unicode(f.read(), errors='ignore')
    unicodedata.normalize('NFKD', text).encode('ascii','ignore')
    _sents = [query.strip_punctuation(filter_citations(sent)) for sent in sent_tokenize(text)]
    _sents = [[w.lower() for w in word_tokenize(sent)] for sent in _sents]

def token_map():
    return [(sent,0) for sent in _sents]

def f1(words):
    text = token_map()
    for i in range(len(text)):
        for word in words:
            if word in text[i][0]:
                text[i] = (text[i][0], (text[i][1])+1)
    text = [sent for sent in text if sent[1] != 0]
    return text

def f2(words, text):
    s = []
    for sent in text:
        sent_words = [w for w in words if w in sent[0]]
        if len(sent_words) <= 1:
            s = s + [(sent[0], sent[1], 1e2)]
        else:
            total = 0
            for word1 in sent_words:
                for word2 in sent_words:
                    if word1 != word2:
                        pos1 = sent[0].index(word1)
                        pos2 = sent[0].index(word2)
                        dist = abs(pos1-pos2)
                        total = total + math.log(1+dist)
            s = s + [(sent[0], sent[1], total)]
    return s

def score(words):
    return f2(words, f1(words))

def get_best(scores, n=3):
    sorted_scores = sorted(scores, key=lambda x:x[1]/x[2], reverse=True)
    return sorted_scores[:n]

"""obama = 'data/obama.txt'
tokenize_file(obama)
words = ['president', 'united', 'states']
x = f1(words)
y = f2(words, x)

best = get_best(score(words,s))

for b in best:
    print b"""