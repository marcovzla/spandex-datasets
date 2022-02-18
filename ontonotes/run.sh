#!/usr/bin/env bash
set -e

eval "$(conda shell.bash hook)"

# prepare ontonotes according to https://cemantix.org/data/ontonotes.html
tar xzvf ontonotes-release-5.0_LDC2013T19.tgz
wget https://github.com/ontonotes/conll-formatted-ontonotes-5.0/archive/refs/tags/v12.tar.gz
tar xzvf v12.tar.gz
conda activate datasets2
./skeleton2conll.sh -D ontonotes-release-5.0/data/files/data conll-formatted-ontonotes-5.0-12/conll-formatted-ontonotes-5.0
conda deactivate

mkdir -p brat/pos/train
mkdir -p brat/pos/dev
mkdir -p brat/pos/test

conda activate datasets3
python conll2brat.py --inp conll-formatted-ontonotes-5.0-12/conll-formatted-ontonotes-5.0/data/train/data/ --out brat/pos/train/ --filter conll12_ids/train.id
python conll2brat.py --inp conll-formatted-ontonotes-5.0-12/conll-formatted-ontonotes-5.0/data/development/data/ --out brat/pos/dev/ --filter conll12_ids/development.id
python conll2brat.py --inp conll-formatted-ontonotes-5.0-12/conll-formatted-ontonotes-5.0/data/test/data/ --out brat/pos/test/ --filter conll12_ids/test.id
conda deactivate
