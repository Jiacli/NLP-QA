#!/usr/bin/env python

import os, sys
import nltk
from nltk.parse import stanford
from nltk.stem.snowball import SnowballStemmer
import nltk.data

# configuration for the stanford parser
os.environ['STANFORD_PARSER'] = '../'
os.environ['STANFORD_MODELS'] = '../'
MODEL_PATH = '../englishPCFG.ser.gz'
parser = stanford.StanfordParser(model_path=MODEL_PATH)
stemmer = SnowballStemmer("english", ignore_stopwords=True)


#sentences = parser.raw_parse("NLP is a great course, we all love it.")
#print sentences
#print sentences[0].pos()
# GUI
#for sentence in sentences:
#    sentence.draw()


# global params
sent_text = []
sent_feat = []
ques_text = []
ques_feat = []

def main(args):

    # Preprocess the input, get sentence representation
    # of the whole article. Extract sentence and question
    # features as stemmed token sequence (uni/bi-gram)
    preprocess(args)








# ---- start of pre-processing function ---------------

def preprocess(args):

    article = args[1]
    questions = args[2]

    # sentence segmentation
    sentences = sent_segment(article)
    for sent in sentences:
        sent_text.append(sent)
        tokens = nltk.word_tokenize(sent)
        tokens = stemming(tokens)
        sent_feat.append(tokens)

    # question feature extraction
    with open(questions) as f:
        for line in map(lambda l:l.strip(), f.readlines()):
            ques_text.append(line)

            # extract question feature (e.g., uni/bi-gram)
            # do tokenization and stemming
            tokens = nltk.word_tokenize(line)
            tokens = stemming(tokens)

            feats = ques_feat_extract(tokens)
            ques_feat.append(feats)

    # result check
    assert len(sent_text) == len(sent_feat)
    assert len(ques_text) == len(ques_feat)

    # the data are loaded in the global variables
    # so there is no return statement

SENT_DETECTOR = 'tokenizers/punkt/english.pickle'

def sent_segment(filename):
    # configure nltk package
    sent_detector = nltk.data.load(SENT_DETECTOR)

    sentences = []
    with open(filename) as f:
        for line in map(lambda x:x.strip(), f.readlines()):
            # for empty lines
            if len(line) == 0:
                continue
            # check invalid line e.g., without any punctuation,
            sents = sent_detector.tokenize(line)
            for sent in sents:
                sentences.append(sent)
    return sentences


def ques_feat_extract(tokens):
    # the tag in dropset will not be considered
    # e.g., which who where when ...
    dropset = set(['.', 'WP', 'WRB', 'WDT', 'WP$'])

    feats = []
    tagged = nltk.pos_tag(tokens)
    #print tagged
    prev_token = ''
    prev_tag = ''
    for idx in xrange(len(tagged)):
        token = tagged[idx][0]
        tag = tagged[idx][1]

        if tag not in dropset:
            feats.append(token)
            if len(prev_token) > 0:
                bifeat = prev_token + ' ' + token
                feats.append(bifeat)
            prev_token = token
            prev_tag = tag
        else:
            prev_token = ''
            prev_tag = ''
    #print feats
    return feats

# list version stemming
def stemming(tokens):
    tokens_stem = []
    for token in tokens:
        try: # in case of special character
            tokens_stem.append(stemmer.stem(token).encode('UTF-8'))
        except Exception, e:
            continue
    return tokens_stem

# ---- end of pre-processing function -----------------

def func_test(args):
    #sentences = sent_segment(args[1])
    #for sent in sentences:
    #    print sent

    #with open(args[1]) as f:
    #    for line in map(lambda l:l.strip(), f.readlines()):
    #        ques_text.append(line)
    #        tokens = nltk.word_tokenize(line)
    #        tokens = stemming(tokens)
    #        #print tokens
    #        ques_feat_extract(tokens)

    preprocess(args)

    print sent_text[0:3]
    print sent_feat[0:3]
    print ques_text[0:3]
    print ques_feat[0:3]

    



if __name__ == '__main__':
    func_test(sys.argv)
    # ./answer article.txt questions.txt
    if len(sys.argv) != 3:
        print 'Usage: python ./answer article.txt questions.txt'
        sys.exit(-1)
    main(sys.argv)
