## Ask me questions or die!
## Type quit to exit the program.

import query, data
from os.path import isfile
from nltk.tokenize import word_tokenize
from collections import OrderedDict

_header_gpl = """\rChatbots version 0.0.1, Copyright (C) 2015 Amanda Doucette, Alan Zaffetti
Chatbots comes with ABSOLUTELY NO WARRANTY.  This is free software, and you are welcome
to redistribute it under certain conditions.\n"""
_header = "Enter a bot name to begin (type `exit` to quit):"

_data_path = "data/"
_p_parser = open(_data_path + "pickles/parser.p","r")
_bot_name = ""
_fp_bot = None
_parser = None
_brown = None
line = ""

def load_data():
    #global _parser, _brown
    #if _brown == None:
    #    print "Loading corpus words..."
    #    _brown = treebank.words()
    #    _brown = {w.lower() for w in _brown}
    #if _parser == None:
    #    print "Loading sentence parser..."
    #    _parser = pickle.load(_p_parser)
    if _bot_name != "" and data._sents == None:
        data.tokenize_file(_data_path + _bot_name + '.txt')
    return

def ask(line):
    q = query.match_query(line)
    if q == None:
        print "I don't understand the question."
    else:
        print "{"
        print "  key: " + q[0]
        print "  grp: " + str(q[1])
        print "}"
        words = [(w.lower(), w.lower())
                 for x in q[1]
                 for w in word_tokenize(query.strip_punctuation(x))
                 if w.lower() not in query._en_stops]
        words = OrderedDict(words).keys()
        score = data.score(words)
        best = data.get_best(score)
        print "grp_words: %s" % words
        for b in best:
            print "(%.2f) %s" % (b[1]/b[2],' '.join(b[0]))

def converse(line):
    global _bot_name,_fp_bot
    if line == "goodbye":
        print "Goodbye."
        _bot_name = ""
        _fp_bot = None
    else:
        ask(line)

def load_bot(line):
    global _bot_name, _fp_bot
    filename = _data_path + line + ".txt"

    if line == "exit":
        quit()

    ## Test if the file exists.
    if not isfile(filename):
        print "Cannot find bot named %s" % line
    else:
        _bot_name = line.strip()
        _fp_bot = open(filename)
        load_data()
        print "You are now chatting with \"%s\". Say `goodbye` to quit." % line

def parse(sent):
    sent = word_tokenize(sent.lower())
    for i in range(len(sent)):
        if sent[i] not in _brown:
            sent[i] = 'UNKNOWN'
    print sent
    return _parser.parse_one(sent)

def parser_demo():
    global _parser
    print "Starting parser demo. Type `exit` to quit."
    load_data()
    while line != "exit":
        sent = raw_input("> ")
        if sent == "exit":
            return
        parsed = parse(sent)
        print parsed

print _header_gpl
print _header

while True:
    line = raw_input(_bot_name + "#> ")

    ## Try to load a bot by name!
    if _bot_name == "":
        load_bot(line)

    ## Talk to me!
    else:
        converse(line)

