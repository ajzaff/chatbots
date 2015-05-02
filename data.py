from nltk.tokenize import sent_tokenize, word_tokenize
import unicodedata

sents = []

def tokenize(file):
    global sents
    f = open(file, 'r')
    text = unicode(f.read(), errors='ignore')

    unicodedata.normalize('NFKD', text).encode('ascii','ignore')
    sents = sent_tokenize(text)
    sents = [word_tokenize(sent) for sent in sents]
    sents = [([w.lower() for w in sent], 0) for sent in sents]
    return sents

def f1(words, text):
    for i in range(len(text)):
        for word in words:
            if word in text[i][0]:
                text[i] = (text[i][0], (text[i][1])+1)
    text = [sent for sent in text if sent[1] != 0]
    return text

def f2(words, text):
    s = []
    for sent in text:
        total = 0
        for word1 in words:
            for word2 in words:
                if(word1 in sent[0] and word2 in sent[0]):
                    pos1 = sent[0].index(word1)
                    pos2 = sent[0].index(word2)
                    dist = abs(pos1-pos2)
                    total = total + dist
        s = s + [(sent[0], sent[1], total)]
    return s

obama = 'data/obama.txt'

s = tokenize(obama)
x = f1(['president', 'united', 'states'], s)
y = f2(['president', 'united', 'states'], x)
print y