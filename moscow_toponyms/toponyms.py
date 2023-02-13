import os 
import json
import pandas as pd
import pymorphy2
import spacy
from natasha import (Segmenter, MorphVocab, NewsEmbedding, NewsMorphTagger,
                     NewsSyntaxParser, NewsNERTagger, Doc)
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

BASE_DIR = os.path.dirname(__file__)

def spacy_extract(text):
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

def natasha_extract(text):  
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
            natasha_dict[span.start] = [span.normal, span.stop, span.text]  
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
    with open(os.path.join(BASE_DIR, 'black_list.json')) as f:
        black_list = json.load(f)
    full_black_list = black_list + extracted_names
    return full_black_list

def inner_merging_filtering(full_black_list, spacy_dict, natasha_dict):
    pre_final_spacy = {}
    pre_final_natasha = {}
    for i in spacy_dict.keys():
        position = i
        if position in natasha_dict.keys():
            loc_n = natasha_dict[position][0]
            loc_s = spacy_dict[position] # (the spelling can differ from loc_n after lemmatization)
            if loc_n not in full_black_list:
                pre_final_natasha[position] = [loc_n, natasha_dict[position][1], natasha_dict[position][2]]  
            if loc_s not in full_black_list:
                pre_final_spacy[position] = loc_s
    
    final_result = []
    for i in pre_final_spacy.keys():
        position = i
        if position in pre_final_natasha.keys():
            location_org = pre_final_natasha[position][2]
            location_lem = pre_final_natasha[position][0]
            start_value = position
            stop_value = pre_final_natasha[position][1]
            final_tuple = (location_org, location_lem, start_value, stop_value)
            final_result.append(final_tuple)
    return final_result
