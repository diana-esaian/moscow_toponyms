# Moscow Toponym Extractor
> This module contains an extractor of Moscow toponyms from Russian texts using such Python libraries as [SpaCy](https://github.com/explosion/spaCy), [Natasha](https://github.com/natasha/natasha), and [PyMorphy2](https://github.com/pymorphy2/pymorphy2). 

Returned attributes for extracted Moscow toponym:

-   `toponym` - toponym in an inflected form   (e.g., _Кремле_)
-   `lemmatized_toponym` - toponym in the base form (e.g., _Кремль_)
-   `start_char` - start character index (_79_)
-   `stop_char` - end character index (_85_)

## Installation
1. Install the package using pip:
```sh
pip install moscow-toponyms
```
2. Download _ru_core_news_sm_
```sh
pip install https://github.com/explosion/spacy-models/releases/download/ru_core_news_sm-3.1.0/ru_core_news_sm-3.1.0.tar.gz
```

## Quick start
```python
>>> from moscow_toponyms import QuickExtract
>>> text = "Однажды весною, в час небывало жаркого заката, в Москве, на Патриарших прудах, появились два гражданина."
>>> toponyms = QuickExtract(text)
>>> toponyms.extract(text)
```

## Usage
```python
>>> from moscow_toponyms import ExtractMosToponyms
>>> text = "Однажды весною, в час небывало жаркого заката, в Москве, на Патриарших прудах, появились два гражданина."
>>> extract_toponyms = ExtractMosToponyms(text)
```
Using SpaCy extract toponyms and their position in a text, lemmatize extracted toponyms using PyMorphy2:
```python
>>> spacy_extracted = extract_toponyms.spacy_extract()
>>> spacy_dict = spacy_extracted[0]
>>> spacy_names = spacy_extracted[1]
```
Using Natasha extract toponyms and their position in a text:
```python
>>> natasha_extractor = extract_toponyms.natasha_extract()
>>> natasha_dict = natasha_extractor[0]
>>> natasha_names = natasha_extractor[1]
``` 
Add the extracted names to the existing black list for cleaner output:
```python
>>> black_list = extract_toponyms.merging_blacklists(spacy_names, natasha_names)
```
Final 
``` python
>>> final_results = extract_toponyms.inner_merging_filtering(black_list, spacy_dict, natasha_dict)
>>> print(final_results)
```
