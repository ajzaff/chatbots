## Ask me questions or die!
## Type quit to exit the program.

import pickle, nltk
from os.path import isfile
from nltk.tokenize import word_tokenize

_header_gpl = """\rChatbots version 0.0.1, Copyright (C) 2015 Amanda Doucette, Alan Zaffetti
Chatbots comes with ABSOLUTELY NO WARRANTY.  This is free software, and you are welcome
to redistribute it under certain conditions.\n"""
_header = "Enter a bot name to begin (type `exit` to quit):"

_data_path = "data/"
_p_parser = open(_data_path + "pickles/parser.p","rb")
_bot_name = ""
_fp_bot = None
_parser = None
line = ""

def parse(sent):
    sent = word_tokenize(sent)
    brown = nltk.corpus.brown.words()
    for i, word in enumerate(sent):
        if word not in brown:
            sent[i] = 'UNKNOWN'
    return _parser.parse_one(sent)

def parser_demo():
    global _parser
    print "Starting parser demo. Type `exit` to quit."
    if _parser == None:
        print "Loading sentence parser..."
        _parser = pickle.load(_p_parser)
    while line != "exit":
        sent = raw_input("> ")
        if sent == "exit":
            return
        parsed = parse(sent)
        print parsed

print _header_gpl
print _header

while line != "exit":
    line = raw_input(_bot_name + "#> ")

    if line == "demo":
        parser_demo()
        continue

    ## Try to load a bot by name.
    if _bot_name == "":
        filename = _data_path + line + ".txt"

        ## Test if the file exists.
        if not isfile(filename):
            print "Cannot find bot named %s" % line
        else:
            if _parser == None:
                print "Loading sentence parser..."
                _parser = pickle.load(_p_parser)
            print "You are now chatting with %s. Say `goodbye` to quit." % line
            _bot_name = line.strip()
            _fp_bot = open(filename)

    else:
        if line == "goodbye":
            print "Goodbye."
            _bot_name = ""
            _fp_bot = None