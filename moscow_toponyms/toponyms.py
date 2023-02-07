import os
import csv 
import pandas as pd
import pymorphy2
import spacy
from natasha import (Segmenter, MorphVocab, NewsEmbedding, NewsMorphTagger,
                     NewsSyntaxParser, NewsNERTagger, Doc)
# moving up one directory 
os.chdir("..")
# for spacy
nlp = spacy.load("ru_core_news_sm")
nlp.max_length = 20000000
# for pymorphy2
morph = pymorphy2.MorphAnalyzer()
# for natasha
segmenter = Segmenter()
morph_vocab = MorphVocab()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)

# black_list = []
# names_black_list = []


def black_lists_constructor():
    black_list = []
    names_black_list = []
    with open('data/black_list.csv', 'r') as read_obj:
        b_list = csv.reader(read_obj)
        list_of_csv = list(b_list)

    for i in list_of_csv:
        loc = ''.join(i).lower()
        black_list.append(loc)

    with open('data/names_rus.csv', 'r') as f:
        n_list = csv.reader(f)
        list_of_names = list(n_list)

    for i in list_of_names:
        loct = ''.join(i).lower()
        names_black_list.append(loct)

    return black_list names_black_list

def read(file):
    with open(file) as text:
        book = text.read()
    return book

def spacy(text):
    spacy_dict = {}
    spacy_names = {}

    doc_spacy = nlp(text)

    for ent in doc_spacy.ents:
        if ent.label_ == 'LOC':
            twice_lem = morph.parse(i)[0]
            spacy_dict[ent.start_char] = twice_lem.normal_form
        elif ent.label_ == 'PER':
            spacy_names[ent.start_char] = ent.lemma_
    return spacy_dict, spacy_names

def natasha(text):  
    natasha_dict = {}
    natasha_names = {}
                      
    doc_natasha = Doc(text)
    doc_natasha.segment(segmenter)
    doc_natasha.tag_morph(morph_tagger)
    doc_natasha.parse_syntax(syntax_parser)
    doc_natasha.tag_ner(ner_tagger)

    for span in doc_natasha.spans:
        if span.type == 'LOC':
            span.normalize(morph_vocab)
            natasha_dict[span.start] = span.normal
        elif span.type == 'PER':
            span.normalize(morph_vocab)
            natasha_names[span.start] = (span.normal)

    return natasha_dict, natasha_names

def merging_blacklists(spacy_names, natasha_names):
    extracted_names = []
    for i in spacy_names.keys():
        position = i
        if position in natasha_names.keys():
            if natasha_names[position] not in extracted_names:
                extracted_names.append(natasha_names[position])

    full_black_list = black_list + names_black_list + extracted_names
    return full_black_list

def inner_merging_filtering(full_black_list, spacy_dict, natasha_dict):
    pre_final_spacy = {}
    pre_final_natasha = {}
    for i in spacy_dict.keys():
        position = i
        if position in natasha_dict.keys():
            loc_n = natasha_dict[position]
            loc_s = spacy_dict[position] # (the spelling can differ from loc_n after lemmatization)
            if loc_n not in full_black_list:
                pre_final_natasha[position] = loc_n
            if loc_s not in full_black_list:
                pre_final_spacy[position] = loc_s
    
    final_result = {}
    for i in pre_final_spacy.keys():
        position = i
        if position in pre_final_natasha.keys():
            location = pre_final_natasha[position]
            if location in final_result.keys():
                final_result[location] +=1
            else:
                final_result[location] = 1
    final = pd.DataFrame.from_dict(final_result) 
    final.to_csv ('mos_toponims.csv', index=False)
