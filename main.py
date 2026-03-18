# This is the fastapi app that serves the invoice data extraction model.

from fastapi import FastAPI, HTTPException
from src.LLM_pipeline_spaCy import pipeline
from src.model import InvoiceRequest
import uvicorn

app = FastAPI()

@app.get("/")
async def read_root():
    
    
    return {"message": "this is root page"}

# get one invoice extraction
@app.post("/invoice")
async def read_item(request: InvoiceRequest):
    try:
        result = pipeline(request.input_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)



