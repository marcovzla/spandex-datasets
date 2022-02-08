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

import argparse
import os


def get_location_and_remove(sent, sub_str):
    loc = sent.find(sub_str)
    sent = sent.replace(sub_str, '')
    return loc, sent


if __name__ == '__main__':
    parser = argparse.ArgumentParser('convert raw data into brat format')
    parser.add_argument('--inp', type=str, required=True, help='input file')
    parser.add_argument('--out', type=str, required=True, help='output file')
    args = parser.parse_args()

    num_sent_per_doc = 100

    with open(args.inp, 'r') as fin:
        ndoc = 0
        ns = 0
        while True:
            sent = fin.readline().strip()
            if sent is None or sent == '':
                break

            if ns % num_sent_per_doc == 0:
                ndoc += 1
                if ns > 0:
                    doc_out.close()
                    ann_out.close()
                doc_out = open(os.path.join(args.out, '{}.txt'.format(ndoc)), 'w')
                ann_out = open(os.path.join(args.out, '{}.ann'.format(ndoc)), 'w')
                ns = 0
                sent_offseet = 0
                entity_ind, rel_ind = 1, 1

            rel = fin.readline().strip()
            _ = fin.readline()
            _ = fin.readline()

            sid, sent = sent.split('\t')
            sent = sent[1:-1]  # remove "
            e1_start, sent = get_location_and_remove(sent, '<e1>')
            e1_end, sent = get_location_and_remove(sent, '</e1>')
            e1 = sent[e1_start:e1_end]
            e2_start, sent = get_location_and_remove(sent, '<e2>')
            e2_end, sent = get_location_and_remove(sent, '</e2>')
            e2 = sent[e2_start:e2_end]
            if e2_start <= e1_end:
                raise Exception('e1 should be before e2')

            doc_out.write('{}\n'.format(sent))

            k1, k2 = 'T{}'.format(entity_ind), 'T{}'.format(entity_ind + 1)
            ann_out.write('{}\t{} {} {}\t{}\n'.format(
                k1, 'mention', e1_start + sent_offseet, e1_end + sent_offseet, e1))
            ann_out.write('{}\t{} {} {}\t{}\n'.format(
                k2, 'mention', e2_start + sent_offseet, e2_end + sent_offseet, e2))
            ann_out.write('{}\t{} {} {}\n'.format(
                'R{}'.format(rel_ind), rel, 'Arg1:{}'.format(k1), 'Arg2:{}'.format(k2)))

            sent_offseet += len(sent) + 1
            entity_ind += 2
            rel_ind += 1
            ns += 1
