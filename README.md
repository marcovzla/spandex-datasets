# Datasets

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

The reference for the datasets in the `ontonotes` directory:

    @inproceedings{pradhan-etal-2013-towards,
        title = "Towards Robust Linguistic Analysis using {O}nto{N}otes",
        author = {Pradhan, Sameer  and
        Moschitti, Alessandro  and
        Xue, Nianwen  and
        Ng, Hwee Tou  and
        Bj{\"o}rkelund, Anders  and
        Uryupina, Olga  and
        Zhang, Yuchen  and
        Zhong, Zhi},
        booktitle = "Proceedings of the Seventeenth Conference on Computational Natural Language Learning",
        month = aug,
        year = "2013",
        address = "Sofia, Bulgaria",
        publisher = "Association for Computational Linguistics",
        url = "https://aclanthology.org/W13-3516",
        pages = "143--152",
    }

The reference for SemEval-2010 Task 8:

    @inproceedings{hendrickx-etal-2010-semeval,
        title = "{S}em{E}val-2010 Task 8: Multi-Way Classification of Semantic Relations between Pairs of Nominals",
        author = "Hendrickx, Iris  and
        Kim, Su Nam  and
        Kozareva, Zornitsa  and
        Nakov, Preslav  and
        {\'O} S{\'e}aghdha, Diarmuid  and
        Pad{\'o}, Sebastian  and
        Pennacchiotti, Marco  and
        Romano, Lorenza  and
        Szpakowicz, Stan",
        booktitle = "Proceedings of the 5th International Workshop on Semantic Evaluation",
        month = jul,
        year = "2010",
        address = "Uppsala, Sweden",
        publisher = "Association for Computational Linguistics",
        url = "https://aclanthology.org/S10-1006",
        pages = "33--38",
    }

The reference for the `openie` dataset:

    @inproceedings{stanovsky-dagan-2016-creating,
        title = "Creating a Large Benchmark for Open Information Extraction",
        author = "Stanovsky, Gabriel  and
        Dagan, Ido",
        booktitle = "Proceedings of the 2016 Conference on Empirical Methods in Natural Language Processing",
        month = nov,
        year = "2016",
        address = "Austin, Texas",
        publisher = "Association for Computational Linguistics",
        url = "https://aclanthology.org/D16-1252",
        doi = "10.18653/v1/D16-1252",
        pages = "2300--2305",
    }
