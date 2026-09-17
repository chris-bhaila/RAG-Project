import os

from langchain_community.vectorstores import FAISS # pyright: ignore[reportMissingImports]
from services.models import model_provider
from config.config import settings as config
from loguru import logger # pyright: ignore[reportMissingImports]

class Vectorstore:

    def __init__(self):
        self.embeddings = model_provider.embedding_model(config.EMBEDDING_MODEL)
        self.vector_store = (FAISS.load_local(config.VECTOR_STORE, self.embeddings, allow_dangerous_deserialization=True)
                             if os.path.exists(config.VECTOR_STORE)
                             else None)

    def create_vector_store(self, chunks, store_name):
        self.vector_store = FAISS.from_documents(chunks, self.embeddings)
        self.vector_store.save_local(store_name)
        logger.success(f"Vector store '{store_name}' created and saved successfully!")

    def retrieve_docs(self, user_ques, k=3):
        if not self.vector_store:
            logger.error("Vector store not initialized!")
            return ""
        retrieval_docs = self.vector_store.similarity_search(user_ques, k=k)
        return "\n\n".join(
            doc.page_content for doc in retrieval_docs
        )

store = Vectorstore()