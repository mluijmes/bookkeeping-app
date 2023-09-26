import streamlit as st
import pandas as pd
from modules import functions as func
import webbrowser as web
from fpdf import FPDF
from streamlit_option_menu import option_menu
from datetime import datetime, timedelta
import csv

# Page
PAGE_TITLE = 'Invoices'
TAB_NAME_0 = 'Database'
TAB_NAME_1 = 'New'
st.set_page_config(page_title=PAGE_TITLE,
                   layout='wide')
st.header(PAGE_TITLE)
st.divider()

# Files
FILEPATH_CATEGORIES = 'data/income_categories.csv'
FILEPATH_INVOICES = 'data/invoices.csv'
FILEPATH_CLIENTS = 'data/clients.csv'
FILEPATH_ACTIVITIES = 'data/activities.csv'

# Types
TAX_TYPE = ['No Tax', '0.09', '0.21']
QTY_TYPE = ['Hours', 'Units']

# Clients & Categories
clients = pd.read_csv(FILEPATH_CLIENTS, delimiter=';')
client_dict = clients.to_dict(orient='records')
CLIENTS = [client['name'] for client in client_dict]
CATEGORIES = func.get_loclist_txt(FILEPATH_CATEGORIES)
COUNT = func.get_last_invoice_number(FILEPATH_INVOICES)

# Initialize session state
if 'invoice_nr' not in st.session_state:
    st.session_state.invoice_nr = int(COUNT) + 1  # Set the initial value


# Custom HTML styling
custom_style = """
<style>
    .custom-container {
        padding: 20px; /* Adjust padding as needed */
        background-color: #f7f7f7;
        border: 1px solid #ddd;
        border-radius: 8px;
    }
    .custom-text {
        font-size: 18px; /* Adjust font size as needed */
        line-height: 3; /* Adjust line height as needed */
        color: #333; /* Adjust text color as needed */
    ,status-text {
        font-size: 18px; /* Adjust font size as needed */
        line-height: 3; /* Adjust line height as needed */
    }
</style>
"""

# Tabs
tab = option_menu(
    menu_title='',
    options=[TAB_NAME_0, TAB_NAME_1],
    icons=['database', 'database-add'],
    menu_icon='cast',
    orientation='horizontal',
    default_index=0
)

if tab == TAB_NAME_0:
    with st.expander('Overview', expanded=True):
        invoice_data = func.select_last_activity(FILEPATH_INVOICES, 'Invoice Number')
        st.divider()
        for index, row in invoice_data.iterrows():
            invoice_number = row["Invoice Number"]
            col1, col2, col3, col4, col5, col6 = st.columns(6)
            with col1:
                st.markdown(f'<div class="custom-text">{invoice_number}</div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<div class="custom-text">{row["Date"]}</div>', unsafe_allow_html=True)
            with col3:
                st.markdown(f'<div class="custom-text">{row["Total Amount"]}</div>', unsafe_allow_html=True)
            with col4:
                st.markdown(f'<div class="custom-text">{row["Client"]}</div>', unsafe_allow_html=True)
            with col5:
                status_color = 'blue'
                status = row["Status"]
                if status == 'Draft':
                    st.markdown(f':grey[{status}]', True)
                elif status == 'Sent':
                    st.markdown(f':blue[{status}]', True)
                elif status == 'Paid':
                    st.markdown(f':green[{status}]', True)
                elif status == 'Overdue':
                    st.markdown(f':red[{status}]', True)
            with col6:
                delete_invoice = st.button('x', 'delete_' + str(index))
                if delete_invoice:
                    func.delete_invoice(FILEPATH_INVOICES, invoice_number)
                    func.sort_csv_by_invoice_number(FILEPATH_INVOICES)
                    st.experimental_rerun()

if tab == TAB_NAME_1:
    with st.expander('New Invoice', expanded=True):
        current_date = datetime.now()
        due_date = current_date + timedelta(days=30)
        invoice_nr = st.number_input('Number', min_value=0, value=st.session_state.invoice_nr)
        invoice_date = st.date_input('Date')
        invoice_due = st.date_input('Due Date', value=due_date)
        invoice_sum = 0
        invoice_client = st.selectbox('Client', CLIENTS)
        invoice_category = st.selectbox('Category', CATEGORIES)
        invoice_status = st.selectbox('Status', ['Draft', 'Sent', 'Paid', 'Overdue'], 0)
        invoice_name = 'INVOICE_' + str(invoice_nr)
        st.divider()

        # Add new activity
        with st.container():
            in0, in1, in2, in3, in4, in5 = st.columns(6)
            with in0:
                activity_date = st.date_input('Date', key='activity_date')
            with in1:
                activity_name = st.text_input('Activity', value='', placeholder='')
            with in2:
                activity_qty_type = st.selectbox('Unit', QTY_TYPE, placeholder='type')
            with in3:
                activity_qty = st.number_input('Quantity', min_value=0, max_value=999, value=1, step=1)
            with in4:
                activity_amt = st.number_input('Amount', min_value=0.0, value=10.0)
            with in5:
                tax_type = st.selectbox('Tax', TAX_TYPE, placeholder='tax')
            add = st.button('Add')

        # Activities
        total_amount_sum = 0
        activity_data = pd.read_csv(FILEPATH_ACTIVITIES, delimiter=';')
        col0, col1, col2, col3, col4, col5 = st.columns(6)
        st.markdown(custom_style, unsafe_allow_html=True)
        for index, row in activity_data.iterrows():
            with st.container():
                with col0:
                    st.markdown(f'<div class="custom-text">{row["Date"]}</div>', unsafe_allow_html=True)
                with col1:
                    st.markdown(f'<div class="custom-text">{row["Activity"]}</div>', unsafe_allow_html=True)
                with col2:
                    st.markdown(f'<div class="custom-text">{row["Quantity Type"]}</div>', unsafe_allow_html=True)
                with col3:
                    st.markdown(f'<div class="custom-text">{row["Quantity"]}</div>', unsafe_allow_html=True)
                with col4:
                    st.markdown(f'<div class="custom-text">{row["Total Amount"]}</div>', unsafe_allow_html=True)
                with col5:
                    delete_activity = st.button('x', 'delete_' + str(index))
                    if delete_activity:
                        func.remove_loclist_txt(index + 1, FILEPATH_ACTIVITIES)
                        func.sort_csv_by_invoice_number(FILEPATH_ACTIVITIES)
                        st.experimental_rerun()
            total_amount_sum += row['Total Amount']  # Accumulate the total amount
        with col5:
            st.divider()
            st.subheader(round(total_amount_sum, 2))

        activity_tot_amt = activity_amt * activity_qty
        tax_perc = float(tax_type) if tax_type != 'No Tax' else 0
        tax_amt = activity_tot_amt * tax_perc
        total_amt = activity_tot_amt * (1 + tax_perc)

        csv_row_activity = [
            str(invoice_nr),
            str(invoice_name),
            str(invoice_date),
            str(invoice_due),
            str(activity_name),
            str(activity_qty),
            str(activity_qty_type),
            str(activity_tot_amt),
            str(tax_type),
            str(tax_amt),
            str(total_amt),
            str(total_amount_sum),
            str(invoice_client),
            str(invoice_status),
            str(invoice_category)
        ]
        csv_row_formatted = ';'.join(csv_row_activity)

        if add:
            func.append_row_to_csv(FILEPATH_ACTIVITIES, csv_row_formatted)
            st.experimental_rerun()
            st.session_state.invoice_nr += 1
        st.divider()


        action1, action2 = st.columns(2)
        with action1:
            generate_pdf = st.button('Print Preview', type='secondary', use_container_width=True)
        with action2:
            add_invoice = st.button('Add Invoice', type='primary', use_container_width=True)


        if add_invoice:
            activities = func.read_csv_rows(FILEPATH_ACTIVITIES)
            func.merge_csv_files(FILEPATH_INVOICES, FILEPATH_ACTIVITIES,FILEPATH_INVOICES)
            func.clear_csv(FILEPATH_ACTIVITIES)
            st.experimental_rerun()
            st.success('Invoice successfully added.', icon='✅')




        class InvoicePDF(FPDF):
            def header(self):
                # Add header content here
                self.set_font('Arial', 'B', 12)
                self.cell(0, 10, 'INVOICE', 0, 1, 'C')

            def footer(self):
                # Position at 1.5 cm from bottom
                self.set_y(-15)
                self.set_font('Arial', 'I', 8)
                self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

            def chapter_title(self, num, label):
                # Add chapter title content here
                self.set_font('Arial', 'B', 12)
                self.cell(0, 10, 'Chapter %d : %s' % (num, label), 0, 1, 'L')

            def chapter_body(self, body):
                # Add chapter body content here
                self.set_font('Arial', '', 12)
                self.multi_cell(0, 10, body)
                self.ln()

            def add_invoice_details(self, details):
                self.set_font('Arial', '', 12)
                for key, value in details.items():
                    self.cell(0, 10, '%s: %s' % (key, value), 0, 1, 'L')

        # Create a PDF instance
        pdf = InvoicePDF()
        pdf.add_page()

        # Add header content
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Invoice', 0, 1, 'C')

        # Add invoice details
        invoice_details = {
            'Invoice Number': invoice_nr,
            'Date': invoice_date,
            'Due Date': invoice_due,
            'Total Amount': invoice_sum
        }
        pdf.add_invoice_details(invoice_details)

        # Add line items
        line_items = [
            {'Item': 'Item 1', 'Quantity': '2', 'Price': '$250.00'},
            {'Item': 'Item 2', 'Quantity': '1', 'Price': '$500.00'}
        ]
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Line Items', 0, 1, 'L')
        pdf.set_font('Arial', '', 12)
        for item in line_items:
            pdf.cell(0, 10, '%s: %s x %s' % (item['Item'], item['Quantity'], item['Price']), 0, 1, 'L')


        # Output the PDF
        if generate_pdf:
            pdf.output('invoice.pdf')
            web.open('invoice.pdf')

