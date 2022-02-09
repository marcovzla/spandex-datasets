#!/usr/bin/env python

# Copyright (c) 2020, Zhengbao Jiang
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from typing import Dict, List, Tuple
import argparse
import os
from tqdm import tqdm


if __name__ == '__main__':
    parser = argparse.ArgumentParser('convert tsv format into brat format')
    parser.add_argument('--inp', type=str, required=True, help='input file')
    parser.add_argument('--out', type=str, required=True, help='output file')
    args = parser.parse_args()

    num_sent_per_doc = 50

    doc_id, sent_count, sent_offset, spanid = 1, 0, 0, 1
    token_li, pos_li = [], []
    txt_file = ann_file = None
    with open(args.inp, 'r') as fin:
        for l in fin:
            l = l.strip()
            if l == '':  # end of the sentence
                sent = ' '.join(token_li)
                txt_file.write('{}\n'.format(sent))
                end = sent_offset - 1
                for token, pos in zip(token_li, pos_li):
                    start, end = end + 1, end + 1 + len(token)  # space
                    ann_file.write('{}\t{} {} {}\t{}\n'.format('T{}'.format(spanid), pos, start, end, token))
                    spanid += 1
                sent_offset += len(sent) + 1  # newline
                sent_count += 1
                token_li, pos_li = [], []

                if sent_count >= num_sent_per_doc:
                    doc_id += 1
                    sent_count, sent_offset, spanid = 0, 0, 1
                    txt_file.close()
                    ann_file.close()
                    txt_file, ann_file = None, None
                continue

            # word
            if txt_file is None:
                txt_file = open(os.path.join(args.out, '{}.txt'.format(doc_id)), 'w')
                ann_file = open(os.path.join(args.out, '{}.ann'.format(doc_id)), 'w')
            token, pos = l.split('\t')
            token_li.append(token)
            pos_li.append(pos)

        if txt_file and not txt_file.closed:  # final close
            txt_file.close()
            ann_file.close()
