test_set = [
    {"query": "how does the app clone a github repo", "correct_chunks": ["main.py::analyze_repo"]},
    {"query": "where does the code talk to the local llm", "correct_chunks": ["main.py::analyze_code_with_ollama"]},
    {"query": "how are python files read from the cloned repo", "correct_chunks": ["main.py::get_all_files"]},
    {"query": "what happens when analyze-repo is called with a url", "correct_chunks": ["main.py::analyze_repo"]},
    {"query": "where is the request body for the api defined", "correct_chunks": ["main.py::RepoRequest"]},
    {"query": "how does the app split a file into functions and classes", "correct_chunks": ["chunker.py::chunk_python_file"]},
    {"query": "what happens if a python file has a syntax error during parsing", "correct_chunks": ["chunker.py::chunk_python_file"]},
    {"query": "how do multiple files get chunked at once", "correct_chunks": ["chunker.py::chunk_file_list"]},
    {"query": "what's the root health check endpoint", "correct_chunks": ["main.py::home"]},
    {"query": "how is the prompt built for the llm", "correct_chunks": ["main.py::analyze_code_with_ollama"]},
    {"query": "where are error responses returned to the client", "correct_chunks": ["main.py::analyze_repo"]},
    {"query": "how does ast get used to parse code", "correct_chunks": ["chunker.py::chunk_python_file"]},
]