#!/usr/bin/env python

import shutil
from pathlib import Path

datasets = {
    'const_ptb': Path('ptb/brat/bracketed'),
    'dep_ptb': Path('ptb/brat/conllx'),
    'pos_ptb': Path('ptb/brat/pos'),
    'ner': Path('conll_ner_2003/brat'),
    'orl': Path('mpqa/brat'),
    'coref': Path('ontonotes/brat/conll_coref_2012'),
    'const_conll': Path('ontonotes/brat/conll_const_2012'),
    'dep_conll': Path('ontonotes/brat/conll_dep_2012'),
    'pos_conll': Path('ontonotes/brat/conll_pos_2012'),
    'srl': Path('ontonotes/brat/conll_srl_2012'),
    'oie': Path('openie/brat'),
    'rc': Path('semeval_2010_task8/brat'),
    'wlp': Path('wlp/WLP-Dataset'),
}

outdir = Path('datasets')
outdir.mkdir()

for name, path in datasets.items():
    if not path.exists():
        print(f'dataset {name} not found at {path}')
        continue
    print(f'collecting {name}')
    shutil.copytree(path, outdir/name)

print('packaging datasets')
archive_name = shutil.make_archive('datasets', 'zip', outdir)

print('deleting files')
shutil.rmtree(outdir)

print(f'saved archive at {archive_name}')
