import os

def load_repo_files(folder_path):
    """
    Walks a folder and reads all .py files.
    Returns a list of {file_path, content} dicts, same format as before.
    """
    files_data = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        files_data.append({
                            "file_path": os.path.relpath(file_path, folder_path),
                            "content": content
                        })
                except:
                    pass

    return files_data