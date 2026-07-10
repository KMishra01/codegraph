from fastapi import FastAPI
from pydantic import BaseModel
from git import Repo
import os

import requests


app = FastAPI()

# Root route
@app.get("/")
def home():
    return {"message": "CodeGraph backend running"}

# Request body structure
class RepoRequest(BaseModel):
    repo_url: str

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

        if not files:
            return {"error": "No Python files found"}

        sample_files = files[:2]

        combined_code = ""
        for f in sample_files:
            content = f["content"][:3000]
            combined_code += f"\n\nFILE: {f['file_path']}\n{content}"

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
                            "file_path": file_path,
                            "content": content
                        })
                except:
                    pass

    return files_data


def analyze_code_with_ollama(code):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": f"Explain this codebase clearly:\n{code}",
                "stream": False
            }
        )

        data = response.json()
        return data.get("response", "No response from model")

    except Exception as e:
        return f"Ollama error: {str(e)}"