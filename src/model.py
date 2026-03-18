from pydantic import BaseModel, Field

class invoice_data(BaseModel):
    INVOICE_NUMBER: str = Field(..., description="INVOICE_NUMBER")
    INVOICE_DATE: str = Field(..., description="INVOICE_DATE，format: YYYY-MM-DD or DD/MM/YYYY")
    DUE_DATE: str = Field(..., description="DUE_DATE，format: YYYY-MM-DD or DD/MM/YYYY")
    VENDOR_NAME: str = Field(..., description="VENDOR_NAME")
    TOTAL_AMOUNT: float = Field(..., description="TOTAL_AMOUNT")
    
class InvoiceRequest(BaseModel):
    input_text: str
    
