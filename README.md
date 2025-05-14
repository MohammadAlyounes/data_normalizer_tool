# Invoice Data Normalizer API Documentation.

A FastAPI application that normalizes messy invoice data with inconsistent formatting. The API accepts JSON files with invoice data and returns a standardized format.

## Features

* Normalizes invoice data keys to consistent format
* Standardizes dates to ISO format (YYYY-MM-DD)
* Cleans up currency fields to numeric values
* Handles both single invoices and invoice collections

## Project Structure
.

├── Dockerfile                # Docker configuration

├── api.py                    # FastAPI application entry point

├── invoice_normalizer.py     # Invoice data normalization logic

├── requirements.txt          # Python dependencies

├── test_invoice.json         # Example invoice for testing

├── normalized_invoices.json  # Output of invoice after parsing

└── README.md                 # This documentation

## Running the Application

1. Clone this repository
2. Build the Docker image:
Change dir to cloned project folder and from CMD run docker build -t invoice-normalizer .
3. Run the Docker container: docker run -p 8000:8000 invoice-normalizer
4. Access the Interactive API documentation is available at: Swagger UI: http://localhost:8000/docs. Then choose the post endpoint /normalize and upload your invoice as JSON



## Suggestion for better performance:

* Use fuzzy match search for key parameters in invoice data for more matching possibilities.

  ![sample_input](https://github.com/user-attachments/assets/7eb7eccf-b223-4fc6-903d-60370e513e8d)

