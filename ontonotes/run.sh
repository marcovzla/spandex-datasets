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

# conll_pos_2012

mkdir -p brat/conll_pos_2012/train
mkdir -p brat/conll_pos_2012/dev
mkdir -p brat/conll_pos_2012/test

conda activate datasets3
python conll2brat_pos.py --inp conll-formatted-ontonotes-5.0-12/conll-formatted-ontonotes-5.0/data/train/data/ --out brat/conll_pos_2012/train/ --filter conll12_ids/train.id
python conll2brat_pos.py --inp conll-formatted-ontonotes-5.0-12/conll-formatted-ontonotes-5.0/data/development/data/ --out brat/conll_pos_2012/dev/ --filter conll12_ids/development.id
python conll2brat_pos.py --inp conll-formatted-ontonotes-5.0-12/conll-formatted-ontonotes-5.0/data/test/data/ --out brat/conll_pos_2012/test/ --filter conll12_ids/test.id
conda deactivate

# conll_srl_2012

mkdir -p brat/conll_srl_2012/train
mkdir -p brat/conll_srl_2012/dev
mkdir -p brat/conll_srl_2012/test

conda activate datasets3
python conll2brat_srl.py --inp conll-formatted-ontonotes-5.0-12/conll-formatted-ontonotes-5.0/data/train/data/ --out brat/conll_srl_2012/train/ --filter conll12_ids/train.id
python conll2brat_srl.py --inp conll-formatted-ontonotes-5.0-12/conll-formatted-ontonotes-5.0/data/development/data/ --out brat/conll_srl_2012/dev/ --filter conll12_ids/development.id
python conll2brat_srl.py --inp conll-formatted-ontonotes-5.0-12/conll-formatted-ontonotes-5.0/data/test/data/ --out brat/conll_srl_2012/test/ --filter conll12_ids/test.id
conda deactivate
