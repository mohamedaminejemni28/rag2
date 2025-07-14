from rag_pipeline import creer_agent_rag_faiss
import os
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

agent = creer_agent_rag_faiss()

query = "Quels services ont des offres spéciales ?"
response = agent.invoke(query)

print("\n Réponse de l'agent :")
print(response["result"])


