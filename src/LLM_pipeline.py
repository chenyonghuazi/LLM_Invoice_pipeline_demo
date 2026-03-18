
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, chain
from dotenv import load_dotenv
import os
import json

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


example_output = {"INVOICE_NUMBER": "CA-001", "INVOICE_DATE": "2019-01-29", "DUE_DATE": "2019-04-26", "VENDOR_NAME": "Yukon Packing", "TOTAL_AMOUNT": 152.25}

system_prompt = """
        You are a professional invoice extraction assistant. Only output valid JSON, no explanations.

        extract the following fields from the invoice text：
        - INVOICE_NUMBER
        - INVOICE_DATE (YYYY-MM-DD or DD/MM/YYYY) 
        - DUE_DATE (YYYY-MM-DD or DD/MM/YYYY)
        - VENDOR_NAME
        - TOTAL_AMOUNT


        example1：
        input_text：{example1_input_text}
        output：{example_output}
        
        example2：
        input_text：{example2_input_text}
        output：{example2_output}
        
        example3：
        input_text：{example3_input_text}
        output：{example3_output}
        
        example4：
        input_text：{example4_input_text}
        output：{example4_output}
        
        example5：
        input_text：{example5_input_text}
        output：{example5_output}


        Extract the fields from the human input invoice text

        """
        
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
        ("human", "Extract the fields from the following invoice text: {input_text}")
])

def pipeline(input_text):
    
    # 2. chain
    chain = (
        # assign data to the prompt, and convert dict to json string
        RunnablePassthrough.assign(
            example1_input_text=lambda _: few_shot_examples[0]['input_text'],
            example_output=lambda _: json.dumps(few_shot_examples[0]['output'], ensure_ascii=False, indent=2),
            example2_input_text=lambda _: few_shot_examples[1]['input_text'], 
            example2_output=lambda _: json.dumps(few_shot_examples[1]['output'], ensure_ascii=False, indent=2),
            example3_input_text=lambda _: few_shot_examples[2]['input_text'],
            example3_output=lambda _: json.dumps(few_shot_examples[2]['output'], ensure_ascii=False, indent=2),
            example4_input_text=lambda _: few_shot_examples[3]['input_text'],
            example4_output=lambda _: json.dumps(few_shot_examples[3]['output'], ensure_ascii=False, indent=2),
            example5_input_text=lambda _: few_shot_examples[4]['input_text'],
            example5_output=lambda _: json.dumps(few_shot_examples[4]['output'], ensure_ascii=False, indent=2),
            input_text=lambda x: json.dumps(x["metrics"], ensure_ascii=False, indent=2)
        )
        | prompt
        | llm.with_structured_output(invoice_data)
    )


    model_result = chain.invoke({"metrics": input_text})
    
    return model_result.model_dump()

