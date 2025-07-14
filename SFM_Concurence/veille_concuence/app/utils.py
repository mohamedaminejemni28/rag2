import pandas as pd
from langchain_core.documents import Document

def excel_to_documents(excel_path: str) -> list:
    df = pd.read_excel(excel_path)
    documents = []
    for i, row in df.iterrows():
        text = "\n".join([f"{col}: {row[col]}" for col in df.columns if pd.notna(row[col])])
        doc = Document(page_content=text, metadata={"row_index": i})
        documents.append(doc)
    return documents
