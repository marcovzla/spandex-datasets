#!/usr/bin/env bash
set -e

datafile=treebank_3_LDC99T42.tgz

if [ ! -f $datafile ]; then
    echo "file not found: $datafile"
    exit 1
fi

eval "$(conda shell.bash hook)"
conda activate datasets3
# clone TreebankPreprocessing repo
git clone https://github.com/hankcs/TreebankPreprocessing.git
# copy stanford parser to TreebankPreprocessing
cp ../utils/stanford-parser*.jar TreebankPreprocessing/
# copy treebank to nltk's data directory
tar xzvf $datafile
cp -R treebank_3/parsed/mrg/wsj/ $HOME/nltk_data/corpora/ptb/WSJ
cp -R treebank_3/parsed/mrg/brown/ $HOME/nltk_data/corpora/ptb/BROWN
# rename all files to uppercase
find $HOME/nltk_data/corpora/ptb/WSJ -depth -exec rename 's/(.*)\/([^\/]*)/$1\/\U$2/' {} \;
find $HOME/nltk_data/corpora/ptb/BROWN -depth -exec rename 's/(.*)\/([^\/]*)/$1\/\U$2/' {} \;
# preprocess treebank
cd TreebankPreprocessing
python ptb.py --output ../bracketed
python ptb.py --task pos --output ../pos
python tb_to_stanford.py --input ../bracketed --lang en --output ../conllx
cd ..
# convert constituency trees
mkdir -p brat/bracketed/train
mkdir -p brat/bracketed/dev
mkdir -p brat/bracketed/test
python bracketed2brat.py --inp bracketed/train.txt --out brat/bracketed/train
python bracketed2brat.py --inp bracketed/dev.txt --out brat/bracketed/dev
python bracketed2brat.py --inp bracketed/test.txt --out brat/bracketed/test
# convert dependency trees
mkdir -p brat/conllx/train
mkdir -p brat/conllx/dev
mkdir -p brat/conllx/test
python conllXtostandoff.py -o brat/conllx/train conllx/train.conllx
python conllXtostandoff.py -o brat/conllx/dev conllx/dev.conllx
python conllXtostandoff.py -o brat/conllx/test conllx/test.conllx
# convert pos tags
mkdir -p brat/pos/train
mkdir -p brat/pos/dev
mkdir -p brat/pos/test
python tsv2brat.py --inp pos/train.tsv --out brat/pos/train/
python tsv2brat.py --inp pos/dev.tsv --out brat/pos/dev/
python tsv2brat.py --inp pos/test.tsv --out brat/pos/test/

conda deactivate

cp README.spandex-datasets.md brat/bracketed
cp README.spandex-datasets.md brat/conllx
cp README.spandex-datasets.md brat/pos
