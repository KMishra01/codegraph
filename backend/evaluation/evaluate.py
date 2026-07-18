from evaluation.eval_set import test_set
from app.retrieval import bm25_retrieval, embedding_retrieval, hybrid_retrieval
def chunk_id(chunk):
    """Turns a chunk dict into the same 'file.py::symbol' string format used in eval_set.py"""
    return f"{chunk['file_path']}::{chunk['symbol_name']}"

def evaluate_recall_at_5(retrieval_function, chunks):
    """
    retrieval_function: a function that takes (query, chunks, top_k) and returns a list of chunk dicts
    chunks: the full list of chunks to search over
    """
    hits = 0
    details = []

    for item in test_set:
        results = retrieval_function(item["query"], chunks, top_k=5)
        retrieved_ids = [chunk_id(r) for r in results]

        hit = any(correct in retrieved_ids for correct in item["correct_chunks"])
        hits += int(hit)

        details.append({
            "query": item["query"],
            "correct": item["correct_chunks"],
            "retrieved": retrieved_ids,
            "hit": hit
        })

    recall_at_5 = hits / len(test_set)
    return recall_at_5, details

def baseline_retrieval(query, chunks, top_k=5):
    """
    Baseline: ignores the query entirely, just returns chunks from files
    matching hardcoded keywords. This mirrors the original pick_important_files logic.
    """
    priority_keywords = ["main", "app", "server", "route", "api", "model"]

    important = [c for c in chunks if any(k in c["file_path"].lower() for k in priority_keywords)]
    others = [c for c in chunks if c not in important]

    return (important + others)[:top_k]

if __name__ == "__main__":
    from app.chunking import chunk_file_list

    with open("main.py", "r") as f:
        main_content = f.read()
    with open("app/chunking.py", "r") as f:
        chunker_content = f.read()

    files = [
        {"file_path": "main.py", "content": main_content},
        {"file_path": "app/chunking.py", "content": chunker_content},
    ]

    chunks = chunk_file_list(files)
    print(f"Total chunks: {len(chunks)}")

    score, details = evaluate_recall_at_5(baseline_retrieval, chunks)
    print(f"\nBaseline Recall@5: {score:.2%}\n")

    for d in details:
        status = "✅" if d["hit"] else "❌"
        print(f"{status} {d['query']}")

    bm25_score, bm25_details = evaluate_recall_at_5(bm25_retrieval, chunks)
    print(f"\nBM25 Recall@5: {bm25_score:.2%}\n")

    for d in bm25_details:
        status = "✅" if d["hit"] else "❌"
        print(f"{status} {d['query']}")

    embedding_score, embedding_details = evaluate_recall_at_5(embedding_retrieval, chunks)
    print(f"\nEmbedding Recall@5: {embedding_score:.2%}\n")

    for d in embedding_details:
        status = "✅" if d["hit"] else "❌"
        print(f"{status} {d['query']}")

    hybrid_score, hybrid_details = evaluate_recall_at_5(hybrid_retrieval, chunks)
    print(f"\nHybrid Recall@5: {hybrid_score:.2%}\n")

    # for d in hybrid_details:
    #     status = "✅" if d["hit"] else "❌"
    #     print(f"{status} {d['query']}")