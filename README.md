# Bookkeeping Application

Author: Marijn Luijmes.
A mockup bookkeeping app with basic functionality for demonstration purposes.
It is built with Streamlit. Manage clients, invoices, and expenses. It's designed to help individuals or small businesses keep track of financial transactions and generate invoices.

## Features


### Clients
- View a list of clients with their contact information.
- Add new clients to the client list.
- Remove clients from the list.

### Invoices
- Create new invoices for clients.
- Add line items to invoices, including the date, description, quantity, price, and tax information.
- View a list of invoices with details such as the invoice number, date, total amount, client, and status.
- Delete invoices.
- Print and preview invoices as PDF documents.

### Expenses
- Record expenses, including the total amount, date, seller/vendor, description, payment method, invoice/receipt number, tax information, category, and currency.
- View a table of recorded expenses.
- Submit and save expense records.

## Project Structure

The project consists of three main modules:

1. **Clients.py**: Manages client data, including viewing existing clients and adding new ones. Users can also remove clients from the list.

2. **Invoices.py**: Handles invoice creation and management. Users can create new invoices, add line items, view existing invoices, and delete them. It also includes a PDF generation feature for printing and previewing invoices.

3. **Expenses.py**: Records expenses, allowing users to input expense details such as total amount, date, seller/vendor, and more. It displays the current list of expenses in a table.

## File Structure

- **data**: Contains CSV and text files to store client information, invoices, and expenses.
- **modules**: Holds utility functions used across modules.
- **README.md**: This file.
- **app.py**: The main Streamlit application that imports and runs the modules.

## Usage

To run the application, you need to have Python and Streamlit installed. Navigate to the project directory and run the following command:

```bash
streamlit run app.py
