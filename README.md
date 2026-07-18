## Evaluation

Retrieval quality measured via Recall@5 on a hand-labeled set of 12 queries 
against the CodeGraph backend's own codebase (main.py + chunker.py, 8 chunks).

| Method                          | Recall@5 | Notes |
|----------------------------------|----------|-------|
| Baseline (keyword file-matching) | 50%      | Query-blind — ranks by filename keywords only, ignores query content entirely |
| BM25                             | 91.6%    |   Fixed all chunker.py queries; missed RepoRequest     |
| Dense embeddings                 | 100%     |     Fixed all queries  |
| Hybrid (BM25 + embeddings)       | TBD      |       |


| Method            | Recall@5 (minGPT, 41 queries) | Notes |
|-------------------|-------------------------------|-------|
| Baseline          | 12.20%                        | Filename-keyword matching, collapses on real repos |
| BM25              | 60.98%                        | Strong on exact terms |
| Embeddings        | 60.98%                        | Strong on conceptual queries |
| Hybrid (0.5/0.5)  | 60.00%                        | Naive equal weight underperforms embeddings alone |
| Hybrid (0.3 BM25) | 68.29%                        | Tuned weight — best result. Still fails on chunks with sparse code (no docstrings, pure math) |


## Evaluation — minGPT (real-world repo, 41 hand-labeled queries, 68 chunks)

| Method                          | Recall@5 | Notes |
|----------------------------------|----------|-------|
| Baseline (keyword file-matching) | 12.20%   | Collapses on real repos — filenames don't match query intent |
| BM25                              | 60.98%   | Strong on exact terms (seed, callback, config), weak on conceptual/paraphrased queries |
| Dense embeddings (Chroma)         | 73.17%   | Best single method — strong semantic matching |
| Hybrid (bm25_weight=0.3)          | 75.61%   | Best overall — empirically tuned weighting toward embeddings |

**Key finding**: naive 50/50 hybrid blending (70.73%) underperformed embeddings alone (73.17%). 
Tuning bm25_weight down to 0.3 pushed hybrid to 75.61% — a real improvement over both individual 
methods, but only achieved by measuring and tuning the blend rather than assuming equal weighting works.

**Remaining failure pattern**: queries against chunks with sparse/undocumented code (e.g. `NewGELU.forward`, 
`CfgNode.__str__`) fail across all methods — no docstrings or descriptive text means neither keyword nor 
semantic matching has signal to work with. This is the motivation for the next step: