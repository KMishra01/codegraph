import ast

MAX_CHUNK_SIZE = 2000  # characters


def get_code(lines, node):
    start = node.lineno - 1
    end = node.end_lineno
    return "\n".join(lines[start:end])


def get_class_header(lines, node):
    """
    Returns just the class signature + docstring (if any) —
    NOT the full body, since methods are chunked separately.
    Avoids duplicating every method's code inside the class chunk too.
    """
    header_end = node.body[0].lineno - 1 if node.body else node.lineno
    # If the first body item is a docstring, include it
    if node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant):
        header_end = node.body[0].end_lineno
    return "\n".join(lines[node.lineno - 1:header_end])


def split_large_function(lines, node, file_path, symbol_name):
    """
    If a single function/method's code exceeds MAX_CHUNK_SIZE,
    split it into smaller sub-chunks along statement boundaries
    (never mid-statement), each labeled with a part number.
    """
    sub_chunks = []
    current_lines = []
    current_start = node.lineno

    for stmt in node.body:
        stmt_code = "\n".join(lines[stmt.lineno - 1:stmt.end_lineno])
        current_lines.append(stmt_code)
        current_size = sum(len(s) for s in current_lines)

        if current_size > MAX_CHUNK_SIZE:
            sub_chunks.append({
                "file_path": file_path,
                "symbol_name": f"{symbol_name} (part {len(sub_chunks) + 1})",
                "type": "function_part",
                "code": "\n".join(current_lines)
            })
            current_lines = []

    if current_lines:
        sub_chunks.append({
            "file_path": file_path,
            "symbol_name": f"{symbol_name} (part {len(sub_chunks) + 1})",
            "type": "function_part",
            "code": "\n".join(current_lines)
        })

    # If it only ever produced ONE part, just return it as the normal whole function
    if len(sub_chunks) == 1:
        sub_chunks[0]["symbol_name"] = symbol_name
        sub_chunks[0]["type"] = "function"

    return sub_chunks


def chunk_python_file(file_path, content):
    """
    Splits a Python file into chunks: functions, classes (header only),
    and methods (ClassName.method). Any individual function/method that's
    still too large gets recursively split into statement-bounded sub-chunks.
    Falls back to the whole file as one chunk if parsing fails.
    """
    chunks = []

    try:
        tree = ast.parse(content)
    except SyntaxError:
        return [{
            "file_path": file_path,
            "symbol_name": None,
            "type": "file",
            "code": content
        }]

    lines = content.splitlines()

    def add_function_chunk(node, symbol_name):
        code = get_code(lines, node)
        if len(code) > MAX_CHUNK_SIZE:
            chunks.extend(split_large_function(lines, node, file_path, symbol_name))
        else:
            chunks.append({
                "file_path": file_path,
                "symbol_name": symbol_name,
                "type": "function",
                "code": code
            })

    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            # Class chunk = signature + docstring only, not the full body
            chunks.append({
                "file_path": file_path,
                "symbol_name": node.name,
                "type": "class",
                "code": get_class_header(lines, node)
            })

            for child in node.body:
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    add_function_chunk(child, f"{node.name}.{child.name}")

        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            add_function_chunk(node, node.name)

    if not chunks:
        chunks.append({
            "file_path": file_path,
            "symbol_name": None,
            "type": "file",
            "code": content
        })

    return chunks


def chunk_file_list(files_data):
    """
    Takes a list of {file_path, content} dicts and returns a flat list of chunks
    across all files.
    """
    all_chunks = []
    for f in files_data:
        chunks = chunk_python_file(f["file_path"], f["content"])
        all_chunks.extend(chunks)
        
    all_chunks = [c for c in all_chunks if c["code"].strip()]

    return all_chunks