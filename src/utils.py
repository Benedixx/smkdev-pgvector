import os
from openai import OpenAI
from pypdf import PdfReader
from dotenv import load_dotenv

load_dotenv()

class Utils:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
    def read_pdf(self, path):
        content = []
        pdf = PdfReader(path)
        print(f'reading {os.path.basename(path)}')
        for i in range(len(pdf.pages)):
            content.append({
                'content': pdf.pages[i].extract_text(),
                'metadata': {'page': i + 1, 'filename': os.path.basename(path)}
            })
        return content

    def text_splitter(self, text, chunk_size):
        words = text.split()
        return [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
    
    def get_embedding(self, text):
        response = self.client.embeddings.create(model='text-embedding-3-large', input=text, encoding_format='float')
        return response.data[0].embedding

    def create_embedding(self, content):
        print('creating embeddings')
        for i in range(len(content)):
            response = self.get_embedding(content[i]['content'])
            content[i]['embedding'] = response
        
        return content
