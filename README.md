## Evaluation

Retrieval quality measured via Recall@5 on a hand-labeled set of 12 queries 
against the CodeGraph backend's own codebase (main.py + chunker.py, 8 chunks).

| Method                          | Recall@5 | Notes |
|----------------------------------|----------|-------|
| Baseline (keyword file-matching) | 50%      | Query-blind — ranks by filename keywords only, ignores query content entirely |
| BM25                             | 91.6%    |   Fixed all chunker.py queries; missed RepoRequest     |
| Dense embeddings                 | 100%     |     Fixed all queries  |
| Hybrid (BM25 + embeddings)       | TBD      |       |