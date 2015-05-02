import re
from nltk import word_tokenize, pos_tag
from nltk.corpus import stopwords

_en_stops = stopwords.words(fileids='english')

##################
## Query frames ##
##################

_r_queries = {
    "decision_past_have":
        re.compile(r"^have you (.+)$",flags=re.IGNORECASE),
    "decision_past_did":
        re.compile(r"^did you (.+)$",flags=re.IGNORECASE),
    "decision_pres_are":
        re.compile(r"^are you (.+)$",flags=re.IGNORECASE),
    "temporal_past_were":
        re.compile(r"^when were you (.+)$")
}

def match_query(query):
    for key in _r_queries:
        m = _r_queries[key].match(query)
        if m:
            return key, m.groups()
    return None

print match_query("Are you President of the United States")

def tag_query(query):
    query = word_tokenize(query.lower())
    return pos_tag(query)

def filter_tagged_stops(tagged_query):
    return [(w,T) for w,T in tagged_query if w not in _en_stops]