import streamlit as st
import pandas as pd
import os

# Files
FILEPATH_CATEGORIES = 'data/expense_categories.txt'
FILEPATH_INVOICES = 'data/invoices.csv'
FILEPATH_CLIENTS = 'data/clients.csv'
FILEPATH_EXPENSES = 'data/expenses.csv'

# Function to add a new expense record to the expenses.csv file
def add_expense(filepath, total_amount, date, seller, description, payment_method, invoice_number, tax_info, category, currency):
    # Check if the expenses.csv file exists, if not, create it
    if not os.path.exists(filepath):
        with open(filepath, 'w') as f:
            f.write(
                'Total Amount;Date;Seller or Vendor;Description;Payment Method;Invoice or Receipt Number;Tax Information;Category;Currency\n')

    # Append the new expense data to the expenses.csv file
    with open(filepath, 'a') as f:
        f.write(
            f'{total_amount};{date};{seller};{description};{payment_method};{invoice_number};{tax_info};{category};{currency}\n')

# Create a Streamlit app
st.title('Expense Receipts')

# Create a form to collect expense details
with st.form('Expense Form', clear_on_submit=True):
    total_amount = st.number_input('Total Amount', value=0.0, step=1.0, min_value=0.0) * -1
    date = st.date_input('Date')
    seller = st.text_input('Seller or Vendor')
    description = st.text_area('Description')
    payment_method = st.selectbox('Payment Method', ['Cash', 'Credit Card', 'Check', 'Online Payment'])
    invoice_number = st.text_input('Invoice or Receipt Number')
    tax_info = st.text_input('Tax Information')
    category = st.text_input('Category')
    currency = st.text_input('Currency', value='USD')

    submit_button = st.form_submit_button('Submit')

# Handle form submission
if submit_button:
    # Add the expense to the CSV file
    add_expense(FILEPATH_EXPENSES, total_amount, date, seller, description, payment_method, invoice_number, tax_info, category, currency)
    st.success('Expense added successfully.', icon='✅')

# Display the current expenses in a table
st.header('Current Expenses')
if os.path.exists(FILEPATH_EXPENSES):
    expenses_df = pd.read_csv(FILEPATH_EXPENSES, delimiter=';')
    st.dataframe(expenses_df)
else:
    st.info('No expenses found.')

