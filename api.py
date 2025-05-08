from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
import json
import uvicorn
from io import BytesIO
from typing import Dict, Any, List, Optional
import invoice_normalizer
from invoice_normalizer import normalize_invoice_data

app = FastAPI(title="Invoice Data Normalizer API")

@app.get("/")
def read_root():
    return {"message": "Invoice Data Normalizer API",
            "usage": "POST /normalize with a JSON file"}


@app.post("/normalize")
async def normalize_invoice(file: UploadFile = File(...)):
    """
    Normalize invoice data from a JSON file.

    - Upload a JSON file with inconsistently formatted invoice data
    - Returns a normalized version with standardized keys, dates, and currency values
    """
    if file.content_type != "application/json":
        raise HTTPException(status_code=400, detail="Only JSON files are supported")

    try:
        # Read file content
        contents = await file.read()
        invoice_data = json.loads(contents)

        # Process as a list of invoices or a single invoice
        normalized_data = normalize_invoice_data(invoice_data)

        return normalized_data

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error normalizing data: {str(e)}")


if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
