
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, chain
from dotenv import load_dotenv
import os
import json
import spacy
load_dotenv()

from src.prepare_data import few_shot_examples
from src.model import invoice_data

# 1. in-order to present the demo, I have to use online LLM to process the pipeline. In the real case, we will use local LLM.
llm = init_chat_model(
        "gemini-2.5-flash",               
        model_provider="google_genai",
        google_api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0.0,
        max_output_tokens=8192,
        #  thinking_level="low"（new attribute in new version）
    )

from pathlib import Path

# 1. this file's path
current_script = Path(__file__).resolve()

# 2. get this file's directory (src/)
current_dir = current_script.parent

# 3. look for parent directory (project/)
parent_dir = current_dir.parent

# 4. get target file path (config.ini in project/)
target_file = parent_dir / "invoice_ner" / "model-best"

nlp = spacy.load(target_file)
def extract_invoice_entities(text: str) -> dict:
    doc = nlp(text)
    result = {}
    for ent in doc.ents:
        # ex: INVOICE_NUMBER, TOTAL_AMOUNT...
        result[ent.label_] = ent.text.strip()
    return result

system_prompt = """
        You are a professional invoice extraction assistant. Only output valid JSON, no explanations.

        extract the following fields from the invoice text：
        - INVOICE_NUMBER
        - INVOICE_DATE (YYYY-MM-DD or DD/MM/YYYY) 
        - DUE_DATE (YYYY-MM-DD or DD/MM/YYYY)
        - VENDOR_NAME
        - TOTAL_AMOUNT

        Extract the fields from the human input invoice text

        """
        
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
        ("human", "Examples: {examples}. Extract the fields from the following invoice text: {input_text}")
])

def pipeline(input_text):
    
    # 2. chain
    chain = (
        # assign data to the prompt, and convert dict to json string
        RunnablePassthrough.assign(
            examples = lambda x: json.dumps(x["examples"], ensure_ascii=False, indent=2),
            input_text=lambda x: json.dumps(x["metrics"], ensure_ascii=False, indent=2)
        )
        | prompt
        | llm.with_structured_output(invoice_data)
    )


    model_result = chain.invoke({"examples": extract_invoice_entities(input_text), "metrics": input_text})
    
    return model_result.model_dump()

