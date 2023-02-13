from toponyms import *

def main(book):
    spacy_extractor = spacy_extract(book)
    spacy_dict = spacy_extractor[0]
    spacy_names = spacy_extractor[1]

    natasha_extractor = natasha_extract(book)
    natasha_dict = natasha_extractor[0]
    natasha_names = natasha_extractor[1]

    black_list = merging_blacklists(spacy_names, natasha_names)
    final_results = inner_merging_filtering(black_list, spacy_dict, natasha_dict)
    return final_results

if __name__ == "__main__":
    book = input()
    main(book)
