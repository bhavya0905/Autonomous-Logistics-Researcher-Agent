from memory.vector_db import VectorDB

class KnowledgeStore:
    """
    Responsible for storing already-chunked documents into the vector database.
    Acts as the ingestion layer between the research pipeline and the vector DB.
    """

    def __init__(self):
        self.vector_db = VectorDB()

    def store_document(self, chunks: list[dict]) -> None:
        """
        Store pre-chunked documents into the vector database.

        Expected chunk format:
        [
            {
                "text": "...",
                "metadata": {
                    "title": "...",
                    "url": "...",
                    "section": "optional"
                }
            }
        ]
        """

        if not chunks:
            print("[KnowledgeStore] No chunks to store.")
            return

        try:
            self.vector_db.add_document(chunks)

            print(f"[KnowledgeStore] Stored {len(chunks)} chunks.")

        except Exception as e:
            print(f"[KnowledgeStore] Failed storing document: {e}")