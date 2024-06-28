# Monance: M-Pesa Transaction Analysis

Monance is a FastAPI application that analyzes M-Pesa transaction messages and provides useful insights about your spending habits. 
It categorizes transactions into different categories like Grocery, Travelling, Miscellaneous, and House expenses.

## Features

- Extract M-Pesa transaction messages from an Excel file or from the Sqlite database
- Categorize transactions based on a predefined set of categories
- Analyze transaction details like user, payment amount, transaction cost, and date
- Generate a PDF report of the transactions
  
## Instructions:

Replace 'your_file.xlsx' with the actual file path of your Excel file containing MPesa transaction data or configure sqlite to the Mpesa transactions details.
Make sure you have the necessary Python libraries installed, including pandas.
Run the script to extract and analyze MPesa transaction data.

## Installation

1. Clone the repository:
 git clone https://github.com/Munanom/MPESA-Budget-and-Analysis-System.git

2. Navigate to the project directory:
cd MPESA-Budget-and-Analysis-System

3. Create a virtual environment (optional but recommended):
python3 -m venv env
source env/bin/activate  # On Windows, use env\Scripts\activate

4. Install the required dependencies:
pip install -r requirements.txt

## Usage

1. Make sure you have an Excel file containing M-Pesa transaction messages in the format required by the application.
Update the file path in the `get_mpesa_message` function in `api.py` to point to your Excel file.

3. Run the FastAPI application:
uvicorn api:app --reload
4. Access the API at `http://localhost:8000/`.

5. You can filter the transactions by date and category using the following query parameters:
   - `dateq`: Filter transactions on or after the specified date (e.g., `http://localhost:8000/?dateq=2023-05-01`)
   - `category`: Filter transactions by category (e.g., `http://localhost:8000/?category=Grocery`)

6. To generate a PDF report of the transactions, append `?pdf=true` to the URL (e.g., `http://localhost:8000/?pdf=true`). The PDF file will be downloaded to the `output` directory.

## Dependencies

The main dependencies used in this project are:

- FastAPI
- Pandas
- Pydantic
- pdfkit

For a complete list of dependencies, see the `requirements.txt` file.

## Contributing

Contributions are welcome! If you find any issues or want to add new features, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
