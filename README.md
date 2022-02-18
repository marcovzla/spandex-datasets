# Datasets

8 datasets consisting of annotations of 10 tasks are included in this repository.

| Dataset             | Task    | Task code     | Dir                      |
|---------------------|---------|---------------|--------------------------|
| Wet Lab Protocols   | NER     | wlp           | data/wlp                 |
|                     | RE      | wlp           | data/wlp                 |
| CoNLL-2003          | NER     | ner           | data/semeval_2014/       |
| SemEval-2010 Task 8 | RE      | rc            | data/semeval_2010_task8/ |
| OntoNotes 5.0       | Coref.  | coref         | data/conll_coref_2012/   |
|                     | SRL     | srl           | data/conll_srl_2012/     |
|                     | POS     | pos_conll     | data/conll_pos_2012/     |
|                     | Dep.    | dp_conll      | data/conll_dep_2012/     |
|                     | Consti. | consti_conll  | data/conll_consti_2012/  |
| Penn Treebank       | POS     | pos           | data/ptb_pos/            |
|                     | Dep.    | dp            | data/ptb/                |
|                     | Consti. | consti        | data/ptb_consti/         |
| OIE2016             | OpenIE  | oie           | data/openie/             |
| MPQA 3.0            | ORL     | orl           | data/mpqa/               |
| SemEval-2014 Task 4 | ABSA    | semeval14_st2 | data/semeval_2014/       |

Follow the instructions in `run.sh` in each dataset directory to download and preprocess the datasets into BRAT format.

# References

This repository is based on the work described in:

    @inproceedings{jiang-etal-2020-generalizing,
        title = "Generalizing Natural Language Analysis through Span-relation Representations",
        author = "Jiang, Zhengbao  and
        Xu, Wei  and
        Araki, Jun  and
        Neubig, Graham",
        booktitle = "Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics",
        month = jul,
        year = "2020",
        address = "Online",
        publisher = "Association for Computational Linguistics",
        url = "https://aclanthology.org/2020.acl-main.192",
        doi = "10.18653/v1/2020.acl-main.192",
        pages = "2120--2133",
        abstract = "Natural language processing covers a wide variety of tasks predicting syntax, semantics, and information content, and usually each type of output is generated with specially designed architectures. In this paper, we provide the simple insight that a great variety of tasks can be represented in a single unified format consisting of labeling spans and relations between spans, thus a single task-independent model can be used across different tasks. We perform extensive experiments to test this insight on 10 disparate tasks spanning dependency parsing (syntax), semantic role labeling (semantics), relation extraction (information content), aspect based sentiment analysis (sentiment), and many others, achieving performance comparable to state-of-the-art specialized models. We further demonstrate benefits of multi-task learning, and also show that the proposed method makes it easy to analyze differences and similarities in how the model handles different tasks. Finally, we convert these datasets into a unified format to build a benchmark, which provides a holistic testbed for evaluating future models for generalized natural language analysis.",
    }
