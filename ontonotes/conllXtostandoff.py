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

# Script to convert a CoNLL X (2006) tabbed dependency tree format
# file into BioNLP ST-flavored standoff and a reconstruction of the
# original text.



import codecs
import os
import re
import sys

# maximum number of sentences to include in single output document
# (if None, doesn't split into documents)
MAX_DOC_SENTENCES = [10]

# whether to output an explicit root note
OUTPUT_ROOT = True
# the string to use to represent the root node
ROOT_STR = 'ROOT'

INPUT_ENCODING = "UTF-8"
OUTPUT_ENCODING = "UTF-8"

output_directory = None

# rewrites for characters appearing in CoNLL-X types that cannot be
# directly used in identifiers in brat-flavored standoff
charmap = {
    '<': '_lt_',
    '>': '_gt_',
    '+': '_plus_',
    '?': '_question_',
    '&': '_amp_',
    ':': '_colon_',
    '.': '_period_',
    '!': '_exclamation_',
}


def maptype(s):
    return "".join([charmap.get(c, c) for c in s])


def tokstr(start, end, ttype, idnum, text):
    # sanity checks
    assert '\n' not in text, "ERROR: newline in entity '%s'" % (text)
    assert text == text.strip(), "ERROR: tagged span contains extra whitespace: '%s'" % (text)
    return "T%d\t%s %d %d\t%s" % (idnum, maptype(ttype), start, end, text)


def depstr(depid, headid, rel, idnum):
    return "R%d\t%s Arg1:T%d Arg2:T%d" % (idnum, maptype(rel), headid, depid)


def output(infn, docnum, sentences):
    global output_directory

    if output_directory is None:
        txtout = sys.stdout
        soout = sys.stdout
    else:
        # add doc numbering if there is a sentence count limit,
        # implying multiple outputs per input
        if MAX_DOC_SENTENCES:
            outfnbase = os.path.basename(infn).rsplit('.', 1)[0] + '-doc-' + str(docnum)
        else:
            outfnbase = os.path.basename(infn).rsplit('.', 1)[0]
        outfn = os.path.join(output_directory, outfnbase)
        txtout = codecs.open(outfn + '.txt', 'w', encoding=OUTPUT_ENCODING)
        soout = codecs.open(outfn + '.ann', 'w', encoding=OUTPUT_ENCODING)

    offset, idnum, ridnum = 0, 1, 1

    doctext = ""

    for si, sentence in enumerate(sentences):
        tokens, deps = sentence

        # store mapping from per-sentence token sequence IDs to
        # document-unique token IDs
        idmap = {}

        # output tokens
        prev_form = None

        if OUTPUT_ROOT:
            # add an explicit root node with seq ID 0 (zero)
            tokens = [('0', ROOT_STR, ROOT_STR)] + tokens

        for ID, form, POS in tokens:

            if prev_form is not None:
                doctext = doctext + ' '
                offset += 1

            # output a token annotation
            print(tokstr(
                offset, offset + len(form), POS, idnum, form), file=soout)
            assert ID not in idmap, "Error in data: dup ID"
            idmap[ID] = idnum
            idnum += 1

            doctext = doctext + form
            offset += len(form)

            prev_form = form

        # output dependencies
        for dep, head, rel in deps:

            # if root is not added, skip deps to the root (idx 0)
            if not OUTPUT_ROOT and head == '0':
                continue

            print(depstr(idmap[dep], idmap[head], rel, ridnum), file=soout)
            ridnum += 1

        if si + 1 != len(sentences):
            doctext = doctext + '\n'
            offset += 1

    print(doctext, file=txtout)


def process(fn):
    docnum = 1
    sentences = []

    with codecs.open(fn, encoding=INPUT_ENCODING) as f:

        tokens, deps = [], []

        lines = f.readlines()

        for ln, l in enumerate(lines):
            l = l.strip()

            # igore lines starting with "#" as comments
            if len(l) > 0 and l[0] == "#":
                continue

            if re.match(r'^\s*$', l):
                # blank lines separate sentences
                if len(tokens) > 0:
                    sentences.append((tokens, deps))
                tokens, deps = [], []

                # limit sentences per output "document"
                if MAX_DOC_SENTENCES and len(sentences) >= MAX_DOC_SENTENCES[0]:
                    output(fn, docnum, sentences)
                    sentences = []
                    docnum += 1

                continue

            # Assume it's a normal line. The format is tab-separated,
            # with ten fields, of which the following are used here
            # (from http://ilk.uvt.nl/conll/):
            # 1 ID     Token counter, starting at 1 for each new sentence.
            # 2 FORM   Word form or punctuation symbol.
            # 5 POSTAG Fine-grained part-of-speech tag
            # 7 HEAD   Head of the current token
            # 8 DEPREL Dependency relation to the HEAD.
            fields = l.split('\t')

            assert len(fields) == 10, "Format error on line %d in %s: expected 10 fields, got %d: %s" % (
                ln, fn, len(fields), l)

            ID, form, POS = fields[0], fields[1], fields[4]
            head, rel = fields[6], fields[7]

            tokens.append((ID, form, POS))
            # allow value "_" for HEAD to indicate no dependency
            if head != "_":
                deps.append((ID, head, rel))

        # process leftovers, if any
        if len(tokens) > 0:
            sentences.append((tokens, deps))
        if len(sentences) > 0:
            output(fn, docnum, sentences)


def main(argv):
    global output_directory

    # Take an optional "-o" arg specifying an output directory for the results
    output_directory = None
    filenames = argv[1:]
    if len(argv) > 2 and argv[1] == "-o":
        output_directory = argv[2]
        print("Writing output to %s" % output_directory, file=sys.stderr)
        filenames = argv[3:]

    if argv[-1].startswith('sent:'):
        MAX_DOC_SENTENCES[0] = int(argv[-1][5:])
        filenames = filenames[:-1]
        print('MAX_DOC_SENTENCES {}'.format(MAX_DOC_SENTENCES))

    fail_count = 0
    for fn in filenames:
        try:
            process(fn)
        except Exception as e:
            m = str(e).encode(OUTPUT_ENCODING)
            print("Error processing %s: %s" % (fn, m), file=sys.stderr)
            fail_count += 1

    if fail_count > 0:
        print("""
##############################################################################
#
# WARNING: error in processing %d/%d files, output is incomplete!
#
##############################################################################
""" % (fail_count, len(filenames)), file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
