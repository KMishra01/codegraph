import ast

def chunk_python_file(file_path, content):
    """
    Splits a Python file into chunks, one per top-level function or class.
    Falls back to the whole file as one chunk if parsing fails.
    """
    chunks = []

    try:
        tree = ast.parse(content)
    except SyntaxError:
        # If the file can't be parsed, just return it as one chunk
        return [{
            "file_path": file_path,
            "symbol_name": None,
            "type": "file",
            "code": content
        }]

    lines = content.splitlines()

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            start = node.lineno - 1          # ast line numbers are 1-indexed
            end = node.end_lineno            # inclusive end line
            chunk_code = "\n".join(lines[start:end])

            chunks.append({
                "file_path": file_path,
                "symbol_name": node.name,
                "type": "function" if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) else "class",
                "code": chunk_code
            })

    # If no functions/classes found (e.g. just top-level code), fall back
    if not chunks:
        chunks.append({
            "file_path": file_path,
            "symbol_name": None,
            "type": "file",
            "code": content
        })

    return chunks

def chunk_file_list(files_data):
    
    # Takes a list of {file_path, content} dicts and returns a flat list of chunks
    # across all files.
    
    all_chunks = []
    for f in files_data:
        chunks = chunk_python_file(f["file_path"], f["content"])
        all_chunks.extend(chunks)
    return all_chunks