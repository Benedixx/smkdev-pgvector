import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class RequestLLM :
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    def request(self, prompt: list) :
        completions = self.client.chat.completions.create(
            model="gpt-4o",
            messages=prompt
        )
        
        return completions.choices[0].message.content