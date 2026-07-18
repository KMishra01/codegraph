from app.chunking import chunk_file_list
from app.code_loader import load_repo_files
from app.vector_store import index_chunks

if __name__ == "__main__":
    # Step 1: read all .py files from the cloned minGPT repo
    files = load_repo_files("repos/minGPT")

    # Step 2: chunk them using our AST-based chunker
    chunks = chunk_file_list(files)
    print(f"Chunked {len(chunks)} pieces.")

    # Debug: check chunk 19 BEFORE we try to index anything
    print("Chunk at index 19:")
    print(chunks[19])

    # Step 3: embed every chunk ONCE and store permanently in Chroma
    print("Indexing into Chroma — this calls Ollama once per chunk, may take a minute...")
    index_chunks(chunks)