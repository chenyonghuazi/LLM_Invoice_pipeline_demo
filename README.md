# Invoice Extraction API

Based on FastAPI + trained spaCy NER + LangChain + LLM invoice's pipe extraction/automation

Support labels：Invoice No、Invoice Date 、Invoice Due Date、Vendor name、Total Amount

Goal：Highly accurate invoice's pipe extraction/automation (demo)

## Test in Docker


```bash


# 1. docker build
docker build -t <image-name> .
# 2. docker run (will create a new container)
docker run -d -p 8000:8000 <container-id>

# 3. Json example
{

    "input_text":"INVOICE Yukon Packing 443 Maple Avenue Ontaro, NT BAM 387 BILL TO SHIP TO INVOICE # CA-001 Alferd Griner Packer Alferd Griner Packer INVOICE DATE 29/01/2019 765 Polar Ave 185 Red River Ave PO.# 1630/2019 Vancouver; AB T4 Burnaby, NT 281 DUE DATE 26/04/2019 QTY DESCRIPTION UNIT PRICE AMOUNT Smoked chinook salmon fillet 100.00 100.00 Maple bacon doughnuts 15.00 30.00 Poutine curds 5.00 15.00 Sublotal 145.00 GST 5.0% 7.25 TOTAL S152.25 2 A8h TERMS & CONDITIONS Payment is due within 15 days Jhank ycu] Please make cheques payable to: Yukon Packing Bear"
}

# 4. open browser
Post request with Json to http://localhost:8000/invoice 

```

## Test in just python

```bash
python3 main.py

```

## Test in Cloud FastAPI server

```bash

# API
https://invoice-pipeline-demo.onrender.com/invoice

# Json in post request
{

    "input_text":"INVOICE Yukon Packing 443 Maple Avenue Ontaro, NT BAM 387 BILL TO SHIP TO INVOICE # CA-001 Alferd Griner Packer Alferd Griner Packer INVOICE DATE 29/01/2019 765 Polar Ave 185 Red River Ave PO.# 1630/2019 Vancouver; AB T4 Burnaby, NT 281 DUE DATE 26/04/2019 QTY DESCRIPTION UNIT PRICE AMOUNT Smoked chinook salmon fillet 100.00 100.00 Maple bacon doughnuts 15.00 30.00 Poutine curds 5.00 15.00 Sublotal 145.00 GST 5.0% 7.25 TOTAL S152.25 2 A8h TERMS & CONDITIONS Payment is due within 15 days Jhank ycu] Please make cheques payable to: Yukon Packing Bear"
}
```