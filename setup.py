import os
from setuptools import setup

def long_desc():
    with open(os.path.join(os.path.dirname(__file__), "README.md")) as readme:
        long = readme.read()
        return long
setup(
    name="moscow_toponyms",
    version="0.0.7",
    author="Diana Esaian",
    author_email="diana.esaian@gmail.com",
    description="Moscow toponyms extractor for Russian texts",
    long_description=long_desc(),
    long_description_content_type="text/markdown",
    url="https://github.com/diana-esaian/moscow_toponyms",
    classifiers=[
        "License :: OSI Approved :: MIT License",     "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3",
        "Natural Language :: Russian",
        "Topic :: Text Processing"
    ],
    python_requires='>=3.6',
    license="MIT",
    packages=['moscow_toponyms'],
    install_requires=[
        'spacy >= 3.0.9',
        'natasha>=1.5.0',
        'pymorphy2 >= 0.9.1',
        'pymorphy2-dicts >= 2.4.393442.3710985'
    ],
    dependency_links = ['git+https://github.com/explosion/spacy-models/releases/download/ru_core_news_sm-3.1.0/ru_core_news_sm-3.1.0.tar.gz'],
    include_package_data=True,
    zip_safe=False
)
