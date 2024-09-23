from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import re
import random
from uuid import uuid4
from pydantic import BaseModel
from fastapi.responses import StreamingResponse, FileResponse
import pdfkit
import sqlite3
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

origins = [  
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000/",
    "*",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],   
)

# Load paths from .env file
DATABASE_PATH = os.getenv("DATABASE_PATH", "/default/path/to/database.sqlite")
OUTPUT_PATH = os.getenv("OUTPUT_PATH", "output/")

#  extracts mpesa messages from all messages and categorize based on groceries etc
# def get_mpesa_message():
#     df = pd.read_excel("/Users/munanuman/Documents/sch/iMessage-Data.xlsx")
#     df = df[df['User_ID']=="MPESA"]

def get_db_connection():
    """
    Returns an SQLite connection using the specified DATABASE_PATH from environment.
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        return conn
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {e}")

def get_mpesa_message():
    """
    Extracts M-Pesa messages from the database and categorizes them.
    """
    try:
        conn = get_db_connection()
        query = """
            SELECT message, date FROM Messages WHERE user_id = 'MPESA';
        """
        df = pd.read_sql_query(query, conn)
        conn.close()

        # Randomly assign categories to the messages
        random.seed(30)
        df['category'] = [random.choice(["Grocery", "Travelling", "Miscellaneous", "House expenses"]) for _ in range(len(df))]
        df = df[['message', 'date', 'category']]

        return df
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving M-Pesa messages: {e}")

#analyze mpesa message structure and categorize on structure
def monance_data(messages):
    """
    Analyze M-Pesa message structure and categorize based on the structure.
    Returns:
        monance (dict): A dictionary of categorized transactions.
        payments (list): A list of payment amounts.
        transactions (list): A list of transaction costs.
    """
    monance = {}
    payments = []
    transactions = []
    dates_list = list(messages['date'])
    category_list = list(messages['category'])

    for message, date, category in zip(messages['message'], dates_list, category_list):

        if isinstance(message, str):
            m = message.split()[2:]

            # Check if the message contains "sent"
            if m[1] == "sent":
                # search for the user in the message
                user_match = re.search(r"sent to ([\w\s]+?)\s\d", message)
                
                if user_match:
                    user = user_match.group(1)
                    payment = float(m[0][3:].replace(',', ''))
                    payments.append(payment)
                    
                    transaction_cost_match = re.search(r'Transaction cost, Ksh([\d,.]+)', message)
                    
                    if transaction_cost_match:
                        transaction_cost = float(transaction_cost_match.group(1).replace(',', '').rstrip('.'))
                        transactions.append(transaction_cost)
                    else:
                        transaction_cost = 0.0
                    
                    UUID = str(uuid4())[:18].upper()
                    monance[UUID] = {
                        'payment': payment, 
                        'user': user, 
                        'date': date, 
                        'transaction_cost': transaction_cost, 
                        'category': category
                    }
                
            # Check if the message contains "paid"
            elif m[1] == "paid":
                user_match = re.search(r"paid to ([\w\s]+)\.", " ".join(m[:9]))
                
                if user_match:
                    user = user_match.group(1)
                    payment = float(m[0][3:].replace(',', ''))
                    payments.append(payment)
                    
                    transaction_cost_match = re.search(r'Transaction cost, Ksh([\d,.]+)', message)
                    
                    if transaction_cost_match:
                        transaction_cost = float(transaction_cost_match.group(1).replace(',', '').rstrip('.'))
                        transactions.append(transaction_cost)
                    else:
                        transaction_cost = 0.0
                    
                    UUID = str(uuid4())[:18].upper()
                    monance[UUID] = {
                        'payment': payment, 
                        'user': user, 
                        'date': date,
                        'transaction_cost': transaction_cost, 
                        'category': category
                    }

    return monance, payments, transactions

@app.get("/")
async def root(dateq: str = "", category: str = "", pdf: str = ""):
    """
    API root endpoint to retrieve and filter M-Pesa messages, with optional PDF generation.
    Query Params:
        dateq (str): Optional date filter in 'YYYY-MM-DD' format.
        category (str): Optional category filter (e.g., Grocery, Travelling).
        pdf (str): If provided, generates and returns a PDF file of the filtered transactions.
    """
    try:
        messages = get_mpesa_message()

        # Apply date filter if provided
        if dateq:
            messages["date"] = pd.to_datetime(messages["date"])
            messages = messages[messages['date'] >= pd.to_datetime(dateq)]

        # Apply category filter if provided
        if category:
            messages = messages[messages['category'] == category]

        monance, payments, transactions = monance_data(messages)
        response = {
            "messages": monance,
            "total_transactions": sum(transactions),
            "total_payments": sum(payments),
            "total_expense": sum(payments + transactions)
        }

        # Generate and return PDF if requested
        if pdf:
            df = pd.DataFrame(monance).T
            output_html_path = os.path.join(OUTPUT_PATH, "monance.html")
            output_pdf_path = os.path.join(OUTPUT_PATH, "monance.pdf")
            df.to_html(output_html_path)
            pdfkit.from_file(output_html_path, output_pdf_path)
            return FileResponse(output_pdf_path, media_type="application/pdf", filename="downloadfile.pdf")

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")