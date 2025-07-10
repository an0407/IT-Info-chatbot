from uuid import uuid4
import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS

CHROMA_PATH = "chroma_db"
CONTENT_DIR = "app/utils"

class ChromaService:
    def __init__(self):
        self.embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
        self.chroma_path = CHROMA_PATH
        self.vectorstore = None

    def load_text_documents(self) -> list[Document]:
        documents = []
        for root, _, files in os.walk(CONTENT_DIR):
            for file in files:
                if file.endswith(".txt"):
                    path = os.path.join(root, file)
                    with open(path, "r", encoding="utf-8") as f:
                        text = f.read()
                        documents.append(Document(page_content=text, metadata={"source": file}))
        return documents

    def build_vector_store(self):
        print('loading documents')
        # documents = self.load_text_documents()
        # document = documents[0]
        print('\nText Loader')
        documents = TextLoader('app/utils/gullivers_travels.txt', encoding='utf-8').load()
        # print("\n Splitting documents")
        # text_splitter = CharacterTextSplitter(chunk_size = 1000, chunk_overlap = 100)
        # documents = text_splitter.split_documents(raw_document)
        if not documents:
            print("No .txt documents found to index.")
            return {'response' : 'No .txt documents found to index'}

        print('creating vectorstore')
        # text_splitter = CharacterTextSplitter(chunk_size = 1000, chunk_overlap = 0)
        # documents = text_splitter.split_documents(docs)
        self.vectorstore = FAISS.from_documents(documents, HuggingFaceEmbeddings())

        print(f"Stored {len(documents)} documents in Chroma at '{self.chroma_path}'")
        return self.vectorstore

    # def load_vector_store(self) -> Chroma:
    #     if not self.vectorstore:
    #         self.vectorstore = Chroma(
    #             collection_name='anush_details',
    #             persist_directory=self.chroma_path,
    #             embedding_function=self.embedding_model
    #         )
    #     return self.vectorstore

    def query_docs(self, query: str, k: int) -> list[str]:
        print(f"[ QUERY] Searching for: '{query}'")

        # vectordb = self.load_vector_store()
        print(self.vectorstore)
        print('[DEBUG] Similarity Search')
        docs = self.vectorstore.similarity_search(query)
        print('\nFInished similarity search\n')

        if not docs:
            print("[ RAG] No relevant documents found.")
            return []

        print(docs)

        return [doc.page_content for doc in docs]