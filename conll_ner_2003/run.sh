#!/usr/bin/env bash
set -e

git clone https://github.com/glample/tagger.git

mkdir -p brat/train
mkdir -p brat/dev
mkdir -p brat/test

eval "$(conda shell.bash hook)"
conda activate datasets3

# conll02tostandoff.py is adapted from https://github.com/nlplab/brat
python conll02tostandoff.py -o brat/train tagger/dataset/eng.train
python conll02tostandoff.py -o brat/dev tagger/dataset/eng.testa
python conll02tostandoff.py -o brat/test tagger/dataset/eng.testb

conda deactivate

cp README.spandex-datasets.md brat/
