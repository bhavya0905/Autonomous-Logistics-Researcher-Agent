import hashlib
import chromadb
from chromadb.utils import embedding_functions
from config.settings import get_settings
from langchain_text_splitters import RecursiveCharacterTextSplitter


class VectorDB:

    def __init__(self):
        settings = get_settings()

# text splitter for chunking documents
        self.text_splitter = RecursiveCharacterTextSplitter(
             chunk_size=500,
             chunk_overlap=100
)

# persistent vector database
        self.client = chromadb.PersistentClient(
            path=settings.VECTOR_DB_PATH
)

# embedding model
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
             model_name=settings.EMBEDDING_MODEL
)

# collection
        self.collection = self.client.get_or_create_collection(
            name="logistics_knowledge",
            embedding_function=self.embedding_function
)   
    def add_document(self, text: str, metadata: dict | None = None) -> None:

        chunks = self.text_splitter.split_text(text)

        for chunk in chunks:

             doc_id = hashlib.md5(chunk.encode("utf-8")).hexdigest()

             existing = self.collection.get(ids=[doc_id])

             if existing["ids"]:
                  continue

        self.collection.add(
            ids=[doc_id],
            documents=[chunk],
            metadatas=[metadata] if metadata else None
        )    
    
            

    def search(self, query: str, n_results: int = 3):

        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )

        return results["documents"]