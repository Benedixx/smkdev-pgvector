from src.database import Database
from src.utils import Utils

class Ingestion:
    def __init__(self):
        self.db = Database()
        self.util = Utils()

    def ingest_data(self, pdf_path, chunk_size=20):
        content = self.util.read_pdf(pdf_path)
        splitted_content = []

        for item in content:
            chunks = self.util.text_splitter(item['content'], chunk_size)
            for chunk in chunks:
                splitted_content.append({'content': chunk, 'metadata': item['metadata']})

        return self.util.create_embedding(splitted_content)

    def upsert_data(self, pdf_path):
        content = self.ingest_data(pdf_path)
        self.db.upsert_data(content)

    def close(self):
        self.db.close()
