#!/usr/bin/env bash

eval "$(conda shell.bash hook)"

conda create -n datasets3 python=3.7 -y
conda activate datasets3
pip install allennlp allennlp-models matplotlib gensim
python -m nltk.downloader ptb
python -m spacy download en_core_web_sm
conda deactivate

conda create -n datasets2 python=2.7 -y
conda activate datasets2
pip install tensorflow==1.4 matplotlib gensim
conda deactivate

mkdir -p utils/
wget https://nlp.stanford.edu/software/stanford-parser-full-2013-11-12.zip
unzip stanford-parser-full-2013-11-12.zip
cp stanford-parser-full-2013-11-12/stanford-parser*.jar utils/
rm -rf stanford-parser-full-2013-11-12 stanford-parser-full-2013-11-12.zip
