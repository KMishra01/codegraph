from app.vector_store import vector_retrieval

results = vector_retrieval("how does causal self attention work", top_k=5)
for r in results:
    print(r["file_path"], "::", r["symbol_name"])