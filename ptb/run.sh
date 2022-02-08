#!/usr/bin/env bash
set -e

# clone TreebankPreprocessing repo
git clone https://github.com/hankcs/TreebankPreprocessing.git
# get stanford parser and copy it to TreebankPreprocessing
wget https://nlp.stanford.edu/software/stanford-parser-full-2013-11-12.zip
unzip stanford-parser-full-2013-11-12.zip
cp stanford-parser-full-2013-11-12/stanford-parser*.jar TreebankPreprocessing/
# copy treebank to nltk's data directory
tar xzvf treebank_3_LDC99T42.tgz
cp -R treebank_3/parsed/mrg/wsj/ $HOME/nltk_data/corpora/ptb/WSJ
cp -R treebank_3/parsed/mrg/brown/ $HOME/nltk_data/corpora/ptb/BROWN
# rename all files to uppercase
find $HOME/nltk_data/corpora/ptb/WSJ -depth -exec rename 's/(.*)\/([^\/]*)/$1\/\U$2/' {} \;
find $HOME/nltk_data/corpora/ptb/BROWN -depth -exec rename 's/(.*)\/([^\/]*)/$1\/\U$2/' {} \;
# preprocess treebank
cd TreebankPreprocessing
python ptb.py --output ../text
python ptb.py --task pos --output ../pos
python tb_to_stanford.py --input ../text --lang en --output ../conllx
cd ..
