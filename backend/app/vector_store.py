import chromadb
from app.embeddings import get_embedding

# persistantclient tell the chroma to save the data in this folder to disk, so we can reuse it later
client = chromadb.PersistentClient(path="./chroma_data")

# collection (table)

collection = client.get_or_create_collection( name = "code_chunks") # it will check if the collection exists, if not it will create it

# Indexing phase: here we will take the chunks from chunk_file_list and add them .
# this will only be done once, and then we can reuse the collection for retrieval

def index_chunks(chunks):
    # data for indexing
    ids = []
    metadatas = []
    embeddings = []
    documents = []

    for c in chunks:
        chunk_id = f"{c['file_path']}::{c['symbol_name']}"
        ids.append(chunk_id)
        metadatas.append({
            "file_path": c["file_path"],
            "symbol_name": c["symbol_name"] or "",
            "type": c["type"]
        })
        embeddings.append(get_embedding(c["code"]))
        documents.append(c["code"])

    collection.add(
        ids=ids,
        metadatas=metadatas,
        embeddings=embeddings,
        documents=documents
    )
    print(f"Indexed {len(chunks)} chunks into Chroma.")


# this querying phase where this runs everytime user make a query, and it will return the top_k most relevant chunks based on the query embedding
def vector_retrieval(query, chunks = None, top_k = 5): # just to keep the shape

    query_embedding = get_embedding(query) # create embedding for the query
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    retrieved = []
    for i in range(len(results["ids"][0])):
        retrieved.append({
            "file_path": results["metadatas"][0][i]["file_path"],
            "symbol_name": results["metadatas"][0][i]["symbol_name"] or None,
            "code": results["documents"][0][i]
        })

    return retrieved
