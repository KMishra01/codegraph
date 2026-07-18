from app.chunking import chunk_file_list
from app.code_loader import load_repo_files
from app.retrieval import bm25_retrieval, embedding_retrieval, hybrid_retrieval
from evaluation.messy_eval import test_set


def chunk_id(chunk):
    return f"{chunk['file_path']}::{chunk['symbol_name']}"


def baseline_retrieval(query, chunks, top_k=5):
    priority_keywords = ["main", "app", "server", "route", "api", "model"]
    important = [c for c in chunks if any(k in c["file_path"].lower() for k in priority_keywords)]
    others = [c for c in chunks if c not in important]
    return (important + others)[:top_k]


def evaluate_recall_at_5(retrieval_function, chunks):
    hits = 0
    details = []

    for item in test_set:
        results = retrieval_function(item["query"], chunks, top_k=5)
        retrieved_ids = [chunk_id(r) for r in results]

        hit = any(correct in retrieved_ids for correct in item["correct_chunks"])
        hits += int(hit)

        details.append({
            "query": item["query"],
            "hit": hit
        })

    return hits / len(test_set), details


if __name__ == "__main__":
    files = load_repo_files("repos/minGPT")
    chunks = chunk_file_list(files)
    print(f"Total chunks: {len(chunks)}\n")

    for name, fn in [
        ("Baseline", baseline_retrieval),
        ("BM25", bm25_retrieval),
        ("Embeddings", embedding_retrieval),
        ("Hybrid (0.3)", lambda q, c, top_k: hybrid_retrieval(q, c, top_k, bm25_weight=0.3)),
    ]:
        score, details = evaluate_recall_at_5(fn, chunks)
        print(f"{name} Recall@5: {score:.2%}")
        for d in details:
            status = "✅" if d["hit"] else "❌"
            print(f"  {status} {d['query']}")
        print()