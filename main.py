import os
from shutil import copyfileobj
from src.ingestion import Ingestion
from src.prompt import BasePrompt
from src.request_llm import RequestLLM
from src.retrievers import Retrievers
from pydantic import BaseModel
from fastapi import FastAPI, UploadFile, File, HTTPException

app = FastAPI(title='Dasar RAG dengan PGVector')

class QueryModel(BaseModel):
    query: str
    
class IngestModel(BaseModel):
    file: UploadFile
    
class GenerateModel(BaseModel):
    text: str
    top_k: int = 5
    
@app.post('/ingest')
async def ingest(file: UploadFile = File(...)):
    try:
        # validate file
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail='File must be a PDF')
        
        temp_path = 'temp'
        image_path = os.path.join(temp_path, file.filename)
        # write file to temp directory
        with open(image_path, 'wb') as buffer:
            copyfileobj(file.file, buffer)
    except Exception as e: 
        raise HTTPException(status_code=500, detail=str(e))
    
    ingestion = Ingestion()
    ingestion.upsert_data(image_path)
    ingestion.close()
    
    # clean up
    os.remove(image_path)
    
    return {'status': 'success', 'message': 'Data stored successfully'}


@app.post('/retrieve-knowledge')
async def retrieve(query_model: QueryModel):
    retriever = Retrievers()
    result = retriever.retrieve_knowledge(query_model.query)
    
    return {'status': 'success', 'message': 'Data retrieved successfully', 'data': result}

@app.post('/generate-rag')
async def generate(generate_model: GenerateModel):
    retriever = Retrievers()
    base_prompt = BasePrompt()
    request = RequestLLM()
    node_knowledge = retriever.retrieve_knowledge(generate_model.text, generate_model.top_k)
    prompt = base_prompt.message(generate_model.text, node_knowledge)
    result = request.request(prompt)
    
    return {'status': 'success', 'message': 'RAG generated successfully', 'data': result}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=4444, log_level="info", reload=True)
