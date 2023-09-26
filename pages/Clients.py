import streamlit as st
from modules import functions as func
import pandas as pd
import os
from PIL import Image
from streamlit_option_menu import option_menu

# Files
FILEPATH_CATEGORIES = 'data/expense_categories.txt'
FILEPATH_INVOICES = 'data/invoices.csv'
FILEPATH_CLIENTS = 'data/clients.csv'
FILEPATH_CLIENT_IMG = 'data/client_images'

# Header
st.header('Clients')
st.divider()

#Tabs
TAB_0 = 'View All'
TAB_1 = 'Add New'
tab = option_menu(
    menu_title='',
    options=['View All', 'Add New'],
    icons=['bar-chart-fill', 'file-earmark'],
    menu_icon='cast',
    orientation='horizontal',
    default_index=0
)

if tab == TAB_0:
    # General Options Ribbon
    with st.container():
        btn1, btn2 = st.columns(2)
        with btn1:
            num_columns = st.selectbox('Columns',
                        options=[1, 2, 3, 4],
                        index=0,
                        help='Set colums in view',
                        label_visibility='collapsed'
                                       )
        with btn2:
            EXPANDED = st.checkbox('Expand/collapse all', value=True)

    # Clients overview
    clients = pd.read_csv(FILEPATH_CLIENTS, delimiter=';')
    client_dict = clients.to_dict(orient='records')

    # Divide into columns
    columns = st.columns(num_columns,
                         gap='medium')

    for index, row in clients.iterrows():
        with columns[index % num_columns]:
            with st.expander(row['name'], expanded=EXPANDED):
                img_file_png = os.path.join(FILEPATH_CLIENT_IMG, row['name'] + '.png')
                img_file_jpg = os.path.join(FILEPATH_CLIENT_IMG, row['name'] + '.jpg')
                if os.path.exists(img_file_png):
                    st.image(img_file_png, width=64)
                elif os.path.exists(img_file_jpg):
                    st.image(img_file_jpg, width=64)
                # Create two columns for keys and values
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Contact Name**  \n"
                                f"**Phone**  \n"
                                f"**Email**  \n"
                                f"**Website**  \n"
                                f"**City**  \n"
                                f"**Address Line 1**  \n"
                                f"**Address Line 2**  "
                                )
                with col2:
                    st.markdown(f"{row['contact_name']}  \n"
                                f"{row['phone']}  \n"
                                f"{row['email']}  \n"
                                f"{row['website']}  \n"
                                f"{row['city']}  \n"
                                f"{row['adressline1']}  \n"
                                f"{row['adressline2']}  "
                                )
                delete_client = st.button('Remove', 'delete_' + str(index))
                if delete_client:
                    func.remove_loclist_txt(index + 1, FILEPATH_CLIENTS)
                    st.experimental_rerun()

if tab == TAB_1:
    # Add new client
    with st.expander('New Client', expanded=True):
        with st.form('New Client', clear_on_submit=True):
            client_name = st.text_input('Client Name')
            client_img = st.file_uploader('Add Image')
            contact_name = st.text_input('Contact')
            phone = st.text_input('Phone')
            email = st.text_input('Email')
            website = st.text_input('Website')
            st.divider()
            city = st.text_input('City')
            adressline1 = st.text_input('Adressline 1')
            adressline2 = st.text_input('Adressline 2')
            add = st.form_submit_button('Create')

            if client_img is not None:
                image_extension = os.path.splitext(client_img.name)[1]
                image_path = os.path.join(FILEPATH_CLIENT_IMG, f"{client_name}{image_extension}")
                pil_image = Image.open(client_img)
                pil_image.save(image_path)
            if add:
                csv_row = [
                    client_name,
                    contact_name,
                    phone,
                    email,
                    website,
                    city,
                    adressline1,
                    adressline2
                ]
                csv_row_formatted = ';'.join(map(str, csv_row))
                func.append_loclist_row(csv_row_formatted, FILEPATH_CLIENTS)
                st.success(f"{client_name} successfully added", icon='✅')

