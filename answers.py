from nltk import pos_tag

def when(query, sentence):
    sent = pos_tag(sentence)
    numpos = []
    for i in range(len(sent)):
        if sent[i][1] == 'CD':
            numpos = numpos + [i]
