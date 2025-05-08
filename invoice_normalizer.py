# The file used to normalize and parsing the keys and values of input invoice data.

import json
import sys
import re
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define key mapping dictionary
KEY_MAPPINGS = {
    # Invoice number variations
    'inv_no': 'invoice_number',
    'invoice_no': 'invoice_number',
    'InvoiceNumber': 'invoice_number',
    'invoice_num': 'invoice_number',
    'inv_id': 'invoice_number',

    # Date variations
    'inv_date': 'invoice_date',
    'date': 'invoice_date',
    'InvoiceDate': 'invoice_date',
    'issue_date': 'invoice_date',

    # Amount variations
    'amt': 'amount',
    'total': 'amount',
    'InvoiceAmount': 'amount',
    'invoice_amt': 'amount',
    'price': 'amount',

    # Customer variations
    'cust': 'customer',
    'client': 'customer',
    'CustomerName': 'customer',
    'buyer': 'customer',

    # Add more mappings as needed
}


def normalize_keys(invoice_data):
    """Normalize inconsistent key names to standard format"""
    normalized = {}
    for key, value in invoice_data.items():
        # Get standardized key or use lowercase version of original
        normalized_key = KEY_MAPPINGS.get(key, key.lower())
        normalized[normalized_key] = value
    return normalized


def normalize_date(date_str):
    """Parse and standardize different date formats to YYYY-MM-DD"""
    if not date_str or not isinstance(date_str, (str, int)):
        return None

    # Convert to string if it's a number
    date_str = str(date_str).strip()

    # Try common date formats
    formats = [
        '%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y',
        '%d-%m-%Y', '%m-%d-%Y', '%d.%m.%Y',
        '%b %d, %Y', '%d %b %Y', '%B %d, %Y',
        '%Y/%m/%d', '%d %B %Y'
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).strftime('%Y-%m-%d')
        except ValueError:
            continue

    # Try to extract date with regex if standard formats fail
    # This handles cases like "Jan. 25th, 2025" or "2023-5-7"
    date_pattern = r'(\d{1,4})[/.-](\d{1,2})[/.-](\d{1,4})'
    match = re.search(date_pattern, date_str)
    if match:
        parts = [int(part) for part in match.groups()]

        # Figure out which part is the year
        if parts[0] > 1000:  # First part is year (2023-05-07)
            try:
                return f"{parts[0]:04d}-{parts[1]:02d}-{parts[2]:02d}"
            except ValueError:
                pass
        elif parts[2] > 1000:  # Last part is year (07-05-2025)
            try:
                return f"{parts[2]:04d}-{parts[1]:02d}-{parts[0]:02d}"
            except ValueError:
                pass

    logging.warning(f"Could not parse date: {date_str}")
    return date_str


def normalize_amount(amount_val):
    """Clean up currency fields by removing symbols and standardizing format"""
    if amount_val is None:
        return None

    # If already a number, return as float
    if isinstance(amount_val, (int, float)):
        return float(amount_val)

    amount_str = str(amount_val).strip()
    if not amount_str:
        return None

    # Remove currency symbols, commas, and spaces
    # This handles $1,234.56, EUR 1.234,56, 1 234,56 €, etc.
    cleaned = re.sub(r'[^\d.,]', '', amount_str)

    # Handle European decimal format (replace comma with period if needed)
    if ',' in cleaned and '.' not in cleaned:
        cleaned = cleaned.replace(',', '.')
    elif ',' in cleaned and '.' in cleaned:
        # Both comma and period exist - assume comma is thousand separator
        cleaned = cleaned.replace(',', '')

    try:
        return float(cleaned)
    except ValueError:
        logging.warning(f"Could not parse amount: {amount_val}")
        return amount_val


def process_invoice(invoice):
    """Apply all normalization functions to a single invoice"""
    # First normalize keys
    normalized = normalize_keys(invoice)

    # Process specific fields
    if 'invoice_date' in normalized:
        normalized['invoice_date'] = normalize_date(normalized['invoice_date'])

    if 'due_date' in normalized:
        normalized['due_date'] = normalize_date(normalized['due_date'])

    if 'amount' in normalized:
        normalized['amount'] = normalize_amount(normalized['amount'])

    if 'tax' in normalized:
        normalized['tax'] = normalize_amount(normalized['tax'])

    if 'subtotal' in normalized:
        normalized['subtotal'] = normalize_amount(normalized['subtotal'])

    return normalized


def normalize_invoice_data(input_data):
    """Process a list of invoices or a single invoice"""
    if isinstance(input_data, list):
        return [process_invoice(invoice) for invoice in input_data]
    elif isinstance(input_data, dict):
        return process_invoice(input_data)
    else:
        logging.error(f"Unexpected data format: {type(input_data)}")
        return input_data