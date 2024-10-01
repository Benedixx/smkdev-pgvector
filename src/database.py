import psycopg2
import json

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname= 'smkdev',
            user= 'postgres',
            password= 'admin',
            host= 'localhost', 
            port= '5433'
        )
        self.cursor = self.conn.cursor()
        self.create_extension_if_not_exists()
        self.create_table_if_not_exists()

    def create_extension_if_not_exists(self):
        self.cursor.execute('CREATE EXTENSION IF NOT EXISTS vector;')
        self.conn.commit()

    def create_table_if_not_exists(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id bigserial PRIMARY KEY,
            content TEXT,
            metadata JSONB,
            embedding vector(3072)
        );
        """)
        self.conn.commit()

    def upsert_data(self, data):
        for item in data:
            sql = """
            INSERT INTO documents (content, metadata, embedding)
            VALUES (%s, %s, %s)
            ON CONFLICT (id) 
            DO UPDATE SET content = EXCLUDED.content,
                          metadata = EXCLUDED.metadata,
                          embedding = EXCLUDED.embedding;
            """
            self.cursor.execute(sql, (item['content'], json.dumps(item['metadata']), item['embedding']))
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()
