from src.database import Database
from src.utils import Utils

class Retrievers :
    def __init__(self):
        self.db = Database()
        self.utils = Utils()
        
    def retrieve_knowledge(self, query: str, top_k: int = 5):
        query_embedding = self.utils.get_embedding(query)
        
        self.db.cursor.execute(f"""
        SELECT content, metadata, embedding <=> %s::vector AS similarity
        FROM documents
        ORDER BY similarity ASC
        LIMIT {top_k};
        """, (query_embedding,))
        
        results = self.db.cursor.fetchall()
        knowledge = []
        for result in results:
            content, metadata, similarity = result
            similarity = 1 - similarity
            knowledge.append({
            'content': content,
            'metadata': metadata,
            'similarity': similarity
            })
        return knowledge