from nltk import pos_tag, word_tokenize
import re, string

months = r'(january|february|march|april|may|june|july|august|september|november|october|december|jan|feb|mar|apr|may|jun|jul|aug|sept|oct|dec)'

def when(query, sentence):
    sent = pos_tag(sentence)
    query = word_tokenize(query)
    numpos = []
    monthpos = []
    querypos = []
    for i in range(len(sent)):
        if sent[i][1] == 'CD':
            numpos = numpos + [i]
        if re.findall(months, sent[i][0]) != []:
            monthpos = monthpos + [i]
        for q in query:
            if sent[i][0] == q:
                querypos = querypos + [i]
    if len(numpos) == 0:
        return None
    elif len(numpos) == 1:
        if len(monthpos) > 0:
            return sent[monthpos[0]][0] + " " + sent[numpos[0]][0]
        else:
            return sent[numpos[0]][0]
    else:
        nums = []
        for n in numpos:
            dist = 0
            for q in querypos:
                if n < q:
                    dist = 500000
                else:
                    dist = dist + (n-q)
            nums = nums + [(n, dist)]
        min = nums[0]
        for num in nums:
            if num[1] < min[1]:
                min = num
        if len(monthpos) == 0:
            return sent[min[0]][0]
        elif len(monthpos) == 1:
            return sent[monthpos[0]][0] + " " + sent[min[0]][0]
        else:
            m = monthpos[0]
            for month in monthpos:
                if abs(month-min[0]) < abs(m-min[0]):
                    m = month
            return sent[m][0] + " " + sent[min[0]][0]


def decision(query, sentence):
    sent = string.join(sentence);
    n = r'( not | no |n\'t |\'nt)'
    if len(re.findall(n, sent)) == 0:
        return "Yes"
    else:
        return "No"

print when("born", word_tokenize("i was born in july in 1995"))

print when("became president", word_tokenize("i became president in 2012 and was born in 1960"))

print when("died", word_tokenize("i was born in march of 1850 and died in may 1940"))

print decision("president", word_tokenize("barack obama is president"))

print decision("president", word_tokenize("barack obama is not president"))

