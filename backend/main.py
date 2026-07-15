from fastapi import FastAPI
from pydantic import BaseModel
from git import Repo
import os

import requests

# from chunker import chunk_python_file
from chunker import chunk_file_list


app = FastAPI()

# Root route
@app.get("/")
def home():
    return {"message": "CodeGraph backend running"}

# Request body structure
class RepoRequest(BaseModel):
    repo_url: str


def pick_important_files(files):
    priority_keywords = ["main", "app", "server", "route", "api", "model"]

    important = []
    others = []

    for f in files:
        if any(keyword in f["file_path"].lower() for keyword in priority_keywords):
            important.append(f)
        else:
            others.append(f)

    return important[:5] + others[:3]

# Analyze repo endpoint
@app.post("/analyze-repo")
def analyze_repo(request: RepoRequest):
    try:
        repo_url = request.repo_url

        repo_name = repo_url.split("/")[-1].replace(".git", "")
        clone_path = f"repos/{repo_name}"

        if not os.path.exists("repos"):
            os.makedirs("repos")

        if not os.path.exists(clone_path):
            Repo.clone_from(repo_url, clone_path)

        files = get_all_files(clone_path)
        print(f"Cloning repo: {repo_url}")
        print(f"Total files found: {len(files)}")

        if not files:
            return {"error": "No Python files found"}

        chunks = chunk_file_list(files)
        print(f"Total chunks created: {len(chunks)}")

        combined_code = ""
        for c in chunks:
            label = f"{c['file_path']} :: {c['symbol_name']}" if c['symbol_name'] else c['file_path']
            combined_code += f"\n\nFILE: {label}\n{c['code']}"


        result = analyze_code_with_ollama(combined_code)
        return {"analysis": result}

    except Exception as e:
        return {"error": str(e)}
    
def get_all_files(folder_path):
    files_data = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)

            # only read code files (for now keep it simple)
            if file.endswith(".py"):
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


def analyze_code_with_ollama(code):

    prompt = f"""
You are a senior software engineer.

Analyze this codebase and explain:

1. What the project does (simple explanation)
2. Main components (files and their roles)
3. How the parts connect
4. Key functions or classes
5. Overall architecture

Keep it clear and beginner-friendly.

Code:
{code}
"""
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            }
        )
        if response.status_code != 200:
            return f"Error: {response.text}"

        data = response.json()
        return data.get("response", "No response from model")

    except Exception as e:
        return f"Ollama error: {str(e)}"
    




