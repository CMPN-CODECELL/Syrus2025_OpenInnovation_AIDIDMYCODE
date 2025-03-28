import os

def create_repo(base_path):
    # Define the directory structure
    structure = {
        "justfair-chatbot": [
            "backend",
            "backend/routes",
            "backend/services",
            "frontend"
        ]
    }

    # Define the files to create
    files = {
        "backend/main.py": "# FastAPI application",
        "backend/database.py": "# DB connection & models",
        "backend/models.py": "# Pydantic schemas",
        "backend/routes/chat.py": "# Chat endpoints",
        "backend/services/rag.py": "# RAG pipeline implementation",
        "backend/services/embeddings.py": "# Text embedding generation",
        "backend/config.py": "# Environment variables",
        "frontend/ChatInterface.jsx": "// React/Vue/Next.js chat UI",
        "docker-compose.yml": "# Containerized deployment",
        "requirements.txt": "# Dependencies",
        ".env": "# Environment variables"
    }

    # Create the directories
    for root, subdirs in structure.items():
        for subdir in subdirs:
            path = os.path.join(base_path, root, subdir)
            os.makedirs(path, exist_ok=True)
            print(f"Directory created: {path}")

    # Create the files with basic comments
    for file_path, content in files.items():
        full_path = os.path.join(base_path, "justfair-chatbot", file_path)
        with open(full_path, "w") as f:
            f.write(content + "\n")
            print(f"File created: {full_path}")

# Replace 'your/desired/path' with the actual path where you want to create the project
create_repo(r"F:\CYRUS\backend")
