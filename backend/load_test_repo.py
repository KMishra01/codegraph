from app.chunking import chunk_file_list
from app.code_loader import load_repo_files
if __name__ == "__main__":
    files = load_repo_files("repos/minGPT")
    print(f"Total files: {len(files)}")

    chunks = chunk_file_list(files)
    print(f"Total chunks: {len(chunks)}")

    for c in chunks:
        print(c["type"], "-", c["file_path"], "::", c["symbol_name"])