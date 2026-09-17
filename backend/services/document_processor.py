from langchain_community.document_loaders import PyPDFLoader # pyright: ignore[reportMissingImports]
from langchain_text_splitters import RecursiveCharacterTextSplitter # pyright: ignore[reportMissingImports]
from loguru import logger # pyright: ignore[reportMissingImports]

class DocumentProcessor:

    @staticmethod
    def load_and_split_documents(path:str, chunk_size=500, chunk_overlap=50):
        docs = PyPDFLoader(path).load()
        logger.info("Document loaded successfully!")
        logger.info(f"Number of pages in the document: {len(docs)}")
        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        chunks = splitter.split_documents(docs)
        logger.info("Document split into chunks successfully!")
        logger.info(f"Number of chunks created: {len(chunks)}")
        return chunks