from fastapi import FastAPI,File, UploadFile, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import re
import random
from uuid import uuid4
from pydantic import BaseModel
from fastapi.responses import StreamingResponse, FileResponse
import pdfkit


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

# extracts mpesa messages from all messages and categorize based on groceries etc
def get_mpesa_message():
    df = pd.read_excel("/Users/munanuman/Documents/sch/iMessage-Data.xlsx")
    df = df[df['User_ID']=="MPESA"]

    random.seed(30)
    df['category'] = [random.choice( ["Grocery", "Travelling", "Miscellaneous", "House expenses"]) for _ in range(len(df))]
    df = df[['Message', 'Date', 'category']]

    return df

#analyze mpesa message structure and categorize on structure
def monance_data(messages):

    monance = {}
    payments = []
    transactions = []
    dates_list = list(messages['Date'])
    category_list = list(messages['category'])

    for message, date, category in zip(messages['Message'], dates_list, category_list):

        if isinstance(message, str):
            m = message.split()[2:]

            if m[1] == "sent":
                user = re.search(r"sent to ([\w\s]+?)\s\d", message).group(1)
                payment = float(m[0][3:].replace(',', ''))
                payments.append(payment)
                
                transaction_cost_match = re.search(r'Transaction cost, Ksh([\d,.]+)', message)
                
                if transaction_cost_match:
                    transaction_cost = float(transaction_cost_match.group(1).replace(',', '').rstrip('.'))
                    transactions.append(transaction_cost)
                    
                else:
                    transaction_cost = 0.0
                UUID = str(uuid4())[:18].upper()
                monance[UUID] = {'payment': payment, 'user': user, 'date': date, 'transaction_cost': transaction_cost, 'category': category}

            elif m[1] == "paid":
                user = re.search(r"paid to ([\w\s]+)\.", " ".join(m[:9])).group(1)
                payment = float(m[0][3:].replace(',', ''))
                payments.append(payment)
                
                transaction_cost_match = re.search(r'Transaction cost, Ksh([\d,.]+)', message)
                
                if transaction_cost_match:
                    transaction_cost = float(transaction_cost_match.group(1).replace(',', '').rstrip('.'))
                    transactions.append(transaction_cost)
                else:
                    transaction_cost = 0.0
                UUID = str(uuid4())[:18].upper()
                monance[UUID] = {'payment': payment, 'user': user, 'date': date,'transaction_cost': transaction_cost, 'category': category}#extract 

    return monance, payments, transactions


#api based on request 
@app.get("/")
async def root(dateq: str = "", category: str ="", pdf: str = ""):
    messages = get_mpesa_message()

    if dateq:
        messages["Date"] = pd.to_datetime(messages["Date"])
        messages = messages[messages['Date'] >= pd.to_datetime(dateq)]
    
    if category:
        messages = messages[messages['category'] == category]

    monance, payments, transactions = monance_data(messages)
    response = {
        "messages": monance,
        "total_transactions": sum(transactions),
        "total_payments": sum(payments),
         "total_expense": sum(payments + transactions)
    }
    if pdf:
        df=pd.DataFrame(monance).T
        df.to_html("output/monance.html")
        pdfkit.from_file("output/monance.html", "output/monance.pdf")
        return FileResponse("output/monance.pdf", media_type= "application/pdf" , filename="downloadfile.pdf")
        
    return response