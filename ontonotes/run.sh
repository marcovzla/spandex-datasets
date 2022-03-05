#!/usr/bin/env bash
set -e

eval "$(conda shell.bash hook)"

datafile=ontonotes-release-5.0_LDC2013T19.tgz

if [ ! -f $datafile ]; then
    echo "file not found: $datafile"
    exit 1
fi

# prepare ontonotes according to https://cemantix.org/data/ontonotes.html
tar xzvf $datafile
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

# conll_coref_2012

mkdir -p brat/conll_coref_2012/train
mkdir -p brat/conll_coref_2012/dev
mkdir -p brat/conll_coref_2012/test

conda activate datasets2
./compile_coref_data.sh ontonotes-release-5.0
conda deactivate

mkdir conll
mv *.english.v4_gold_conll conll

conda activate datasets3
python conll2brat_coref.py --inp conll/train.english.v4_gold_conll --out brat/conll_coref_2012/train
python conll2brat_coref.py --inp conll/dev.english.v4_gold_conll --out brat/conll_coref_2012/dev
python conll2brat_coref.py --inp conll/test.english.v4_gold_conll --out brat/conll_coref_2012/test
conda deactivate

# conll_dep_2012

conda activate datasets3

mkdir bracketed
python conll2tree.py --inp conll-formatted-ontonotes-5.0-12/conll-formatted-ontonotes-5.0/data/train/data/ --out bracketed/train.txt --filter conll12_ids/train.id
python conll2tree.py --inp conll-formatted-ontonotes-5.0-12/conll-formatted-ontonotes-5.0/data/development/data/ --out bracketed/dev.txt --filter conll12_ids/development.id
python conll2tree.py --inp conll-formatted-ontonotes-5.0-12/conll-formatted-ontonotes-5.0/data/test/data/ --out bracketed/test.txt --filter conll12_ids/test.id

mkdir conllx
java -cp ../utils/stanford-parser.jar -mx1g edu.stanford.nlp.trees.EnglishGrammaticalStructure -basic -keepPunct -conllx -treeFile bracketed/train.txt > conllx/train.conllx
java -cp ../utils/stanford-parser.jar -mx1g edu.stanford.nlp.trees.EnglishGrammaticalStructure -basic -keepPunct -conllx -treeFile bracketed/dev.txt > conllx/dev.conllx
java -cp ../utils/stanford-parser.jar -mx1g edu.stanford.nlp.trees.EnglishGrammaticalStructure -basic -keepPunct -conllx -treeFile bracketed/test.txt > conllx/test.conllx

mkdir -p brat/conll_dep_2012/train
mkdir -p brat/conll_dep_2012/dev
mkdir -p brat/conll_dep_2012/test

python conllXtostandoff.py -o brat/conll_dep_2012/train conllx/train.conllx sent:50
python conllXtostandoff.py -o brat/conll_dep_2012/dev conllx/dev.conllx sent:50
python conllXtostandoff.py -o brat/conll_dep_2012/test conllx/test.conllx sent:50

conda deactivate

# conll_const_2012

conda activate datasets3

mkdir -p brat/conll_const_2012/train
mkdir -p brat/conll_const_2012/dev
mkdir -p brat/conll_const_2012/test

python bracketed2brat.py --inp bracketed/train.txt --out brat/conll_const_2012/train --num_sent 50
python bracketed2brat.py --inp bracketed/dev.txt --out brat/conll_const_2012/dev --num_sent 50
python bracketed2brat.py --inp bracketed/test.txt --out brat/conll_const_2012/test --num_sent 50

conda deactivate

cp README.spandex-datasets.md brat/conll_const_2012
cp README.spandex-datasets.md brat/conll_coref_2012
cp README.spandex-datasets.md brat/conll_dep_2012
cp README.spandex-datasets.md brat/conll_pos_2012
cp README.spandex-datasets.md brat/conll_srl_2012
