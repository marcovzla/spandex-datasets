#!/usr/bin/env bash

pip install allennlp allennlp-models matplotlib gensim
# download other requirements
python -m nltk.downloader ptb
python -m spacy download en_core_web_sm
