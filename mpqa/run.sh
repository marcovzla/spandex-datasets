#!/usr/bin/env bash

# download the code and dataset
git clone https://github.com/amarasovic/naacl-mpqa-srl4orl.git

eval "$(conda shell.bash hook)"
conda activate datasets2

wget https://nlp.stanford.edu/data/glove.6B.zip
unzip glove.6B.zip
python glove-gensim.py
mkdir -p embeddings/glove
mv glove_model.txt embeddings/glove/glove_100_w2vformat.txt

# generate data (0 fold of 4 cv)
cp my_main.py naacl-mpqa-srl4orl/.
pushd naacl-mpqa-srl4orl
mkdir prep
python my_main.py --adv_coef 0.0 --model fs --exp_setup_id new --n_layers_orl 0 --begin_fold 0 --end_fold 4 --window_size 0
popd

conda deactivate
conda activate datasets3

# convert preprocessed data to brat format
mkdir -p brat/train
mkdir -p brat/dev
mkdir -p brat/test

python pkl2brat.py --inp naacl-mpqa-srl4orl/prep/train.pkl:naacl-mpqa-srl4orl/prep/vocab.pkl --out brat/train
python pkl2brat.py --inp naacl-mpqa-srl4orl/prep/dev.pkl:naacl-mpqa-srl4orl/prep/vocab.pkl --out brat/dev
python pkl2brat.py --inp naacl-mpqa-srl4orl/prep/test.pkl:naacl-mpqa-srl4orl/prep/vocab.pkl --out brat/test

conda deactivate
