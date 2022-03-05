#!/usr/bin/env bash
set -e

datafile=SemEval2010_task8_all_data.zip

if [ ! -f $datafile ]; then
    echo "file not found: $datafile"
    exit 1
fi

# download data from google drive
# gdown.pl "https://drive.google.com/file/d/0B_jQiLugGTAkMDQ5ZjZiMTUtMzQ1Yy00YWNmLWJlZDYtOWY1ZDMwY2U4YjFk/view?usp=sharing" SemEval2010_task8_all_data.zip
unzip $datafile

mkdir -p brat/train
mkdir -p brat/dev
mkdir -p brat/test

eval "$(conda shell.bash hook)"
conda activate datasets3
python raw2brat.py --inp SemEval2010_task8_all_data/SemEval2010_task8_training/TRAIN_FILE.TXT --out brat/train/
python raw2brat.py --inp SemEval2010_task8_all_data/SemEval2010_task8_testing_keys/TEST_FILE_FULL.TXT --out brat/test
python split.py --inp brat/train/ --out brat/dev/ --ratio 0.2
conda deactivate

README.spandex-datasets.md brat/
