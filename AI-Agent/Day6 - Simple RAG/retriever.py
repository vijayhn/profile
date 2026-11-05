from pathlib import Path

def load_documents():
    documents={}
    folder=Path("knowledge")
    for file in folder.glob("*.txt"):
        documents[file.name]=file.read_text(encoding="utf-8")
    return documents

def retriever(question):
    result = load_documents()
    question_lower=question.lower()
    for filename,content in result.items():
        if question_lower in content.lower():
            return filename,content 
    return None,None
