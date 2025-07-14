# app/rag_pipeline.py

import os
from utils import excel_to_documents

# ✅ Nouveaux imports recommandés par LangChain v0.2+
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline
from langchain.chains import RetrievalQA


from langchain.chains import RetrievalQA
from langchain_core.language_models import BaseLanguageModel
from langchain_community.vectorstores import FAISS
from langchain_community.llms import HuggingFaceHub  # ou un autre LLM

def construire_rag_chain(index_path: str = "index/faiss_index") -> RetrievalQA:
    # 1. Embeddings (doivent correspondre à ceux utilisés lors de la construction)
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    # 2. Rechargement de l’index FAISS
    print("[INFO] Chargement de l’index FAISS local...")
    index = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)

    # 3. Création du retriever
    retriever = index.as_retriever(search_type="similarity", k=3)

    # 4. Chargement du LLM (ici HuggingFaceHub ou autre)
    print("[INFO] Chargement du modèle de langage (LLM)...")
    llm = HuggingFaceHub(
        repo_id="google/flan-t5-base",  # Tu peux changer par un autre modèle supporté
        model_kwargs={"temperature": 0.1, "max_length": 512}
    )

    # 5. Création de la chaîne RAG
    rag_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )

    print("[✅] Chaîne RAG construite avec succès.")
    return rag_chain
