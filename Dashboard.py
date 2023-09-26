import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from modules import functions as func
import altair as alt

st.set_page_config(
     layout="wide",
     initial_sidebar_state="collapsed",
     menu_items={
         'Get Help': 'https://www.extremelycoolapp.com/help',
         'Report a bug': "https://www.extremelycoolapp.com/bug",
         'About': "# This is a header. This is an *extremely* cool app!"
     }
 )

# Files
FILEPATH_CATEGORIES = 'data/expense_categories.txt'
FILEPATH_INVOICES = 'data/invoices.csv'
FILEPATH_CLIENTS = 'data/clients.csv'
FILEPATH_INVOICES = 'data/invoices.csv'
FILEPATH_CAT_EXPENSES = 'data/expense_categories.txt'
FILEPATH_CAT_INCOME = 'data/income_categories.csv'
FILEPATH_EXPENSES = 'data/expenses.csv'

# Currencies
currency_locales = {
    '$': 'en_US',    # United States Dollar
    '€': 'en_EU',    # Euro
    '£': 'en_GB',    # British Pound Sterling
    'A$': 'en_AU',   # Australian Dollar
    'C$': 'en_CA'    # Canadian Dollar
}
CURRENCY = '$' #st.selectbox('Default Currency', currency_locales.keys())
CURRENCY_LOCALE = currency_locales[CURRENCY]

selected = option_menu(
    menu_title='Dashboard',
    options=['Overview', 'Revenue', 'Expenses'],
    icons=['bar-chart-fill', 'file-earmark', 'credit-card'],
    menu_icon='cast',
    orientation='horizontal',
    default_index=0
)

# Tabs
TAB_NAME_0 = 'Overview'
TAB_NAME_1 = 'Revenue'
TAB_NAME_2 = 'Expenses'

# Tabs
if selected == TAB_NAME_1:
    st.title(TAB_NAME_1)
if selected == TAB_NAME_2:
    st.title(TAB_NAME_2)

if selected == TAB_NAME_0:

    with st.container():
        widget1, widget2, widget3 = st.columns(3)
        with widget1:
            # Total Revenue
            total_revenue = sum(func.get_csv_column(FILEPATH_INVOICES, 'Total Amount'))
            st.metric('Total Revenue', func.format_currency(total_revenue, CURRENCY, CURRENCY_LOCALE, 2),
                      delta_color='normal',
                      label_visibility='visible')

        with widget2:
            # Total Expenses
            total_expenses = sum(func.get_csv_column(FILEPATH_EXPENSES, 'Total Amount'))
            st.metric('Total Expenses', func.format_currency(total_expenses*-1, CURRENCY, CURRENCY_LOCALE, 2),
                      delta_color='normal',
                      label_visibility='visible')

        with widget3:
            # Total Hours
            total_hours = sum(func.get_csv_column(FILEPATH_INVOICES, 'Quantity'))
            st.metric('Total Hours', total_hours,
                      delta_color='normal',
                      label_visibility='visible')

    monthly_totals_income = func.sum_invoice_amounts_by_month(FILEPATH_INVOICES, 'Total Amount')
    monthly_totals_expenses = func.sum_invoice_amounts_by_month(FILEPATH_EXPENSES, 'Total Amount')

    data = pd.DataFrame({
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        'Income': list(monthly_totals_income.values()),
        'Expenses': list(monthly_totals_expenses.values()),
    })

    def calculate_cumulative_values(data):
        cumulative_values = []
        cumulative_value = 0

        for value in data['Income']:
            cumulative_value += value
            cumulative_values.append(cumulative_value)

        return cumulative_values


    cumulative_revenue = calculate_cumulative_values(data)

    # Create a Streamlit app
    st.title('Profitability')

    column1, column2 = st.columns(2)

    # Calculate net profitability (Income - Expenses)
    data['Profit'] = data['Income'] + data['Expenses']  # Net profit is now calculated as Income + Expenses

    # Graphic Settings
    bar_width = 10
    dot_size = 40
    line_width = 2

    primary_color = '#4E8DB7'
    secondary_color = '#3C54E7'
    negative_color = '#FF0000'
    text_color = '#AAAAAA'
    bg_color = '#1A1A1A'
    sec_bg_color = '#1C1C1C'

    income_color = primary_color
    expenses_color = negative_color
    delta_color = secondary_color

    # Define the desired order of months
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    # Create the Altair chart with adjustable settings
    chart = alt.Chart(data).mark_bar(size=bar_width).encode(
        x=alt.X('Month:O', sort=month_order),  # Use ordinal scale with specified sort order
        y=alt.Y('Income', axis=alt.Axis(format='$.0f')),
        color=alt.value(income_color),
    ) + alt.Chart(data).mark_bar(size=bar_width).encode(
        x=alt.X('Month:O', sort=month_order),  # Use ordinal scale with specified sort order
        y=alt.Y('Expenses', axis=alt.Axis(format='$.0f')),
        color=alt.value(expenses_color),
    ) + alt.Chart(data).mark_circle(size=dot_size, color=delta_color).encode(
        x=alt.X('Month:O', sort=month_order),  # Use ordinal scale with specified sort order
        y=alt.Y('Profit', axis=alt.Axis(format='$.0f')),
    ) + alt.Chart(data).mark_line(color=delta_color, strokeWidth=line_width).encode(
        x=alt.X('Month:O', sort=month_order),  # Use ordinal scale with specified sort order
        y=alt.Y('Profit', axis=alt.Axis(format='$.0f')),
    )

    # Display the chart
    with column1:
        with st.expander('Cashflow', expanded=True):
            st.altair_chart(chart, use_container_width=True)

    # Calculate the cumulative sum of revenue
    data['Cumulative Revenue'] = data['Profit'].cumsum()

    # Define a dictionary to map month abbreviations to month numbers
    month_map = {
        'Jan': '01',
        'Feb': '02',
        'Mar': '03',
        'Apr': '04',
        'May': '05',
        'Jun': '06',
        'Jul': '07',
        'Aug': '08',
        'Sep': '09',
        'Oct': '10',
        'Nov': '11',
        'Dec': '12'
    }

    # Convert the "Month" column to datetime format (YYYY-MM) for Altair
    data['Month'] = '2023-' + data['Month'].map(month_map)

    # Create Altair chart with customizable properties
    line_color = primary_color
    area_color = primary_color
    area_opacity = 0.4

    # Create an Altair chart with line, dots, and customizable properties
    chart = alt.Chart(data).encode(
        x=alt.X('Month:T', title='Month'),
        y=alt.Y('Cumulative Revenue:Q', title='Cumulative Revenue')
    )
    line_chart = chart.mark_line(stroke=line_color, strokeWidth=line_width)
    dot_chart = chart.mark_circle(size=dot_size, fill=line_color)
    area_chart = chart.mark_area(opacity=area_opacity, fill=area_color)

    combined_chart = area_chart + line_chart + dot_chart

    with column2:
        with st.expander('Cumulative Revenue', expanded=True):
            # Display the chart in Streamlit
            st.altair_chart(combined_chart, use_container_width=True)


    with st.expander('Client Distribution', expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            st.subheader('Insights')
            inp1, inp2 = st.columns(2)
            with inp1:
                conditional_key = st.selectbox('Grouping', options=['Category', 'Client', 'Status'])
            with inp2:
                key = st.selectbox('Filter', options=['Quantity', 'Amount', 'Tax Amount', 'Total Amount'])

            categories = set(func.get_csv_column(FILEPATH_INVOICES, conditional_key))

            keys = func.get_csv_keys(FILEPATH_INVOICES)

            category_distribution = func.csv_category_sum(FILEPATH_INVOICES, conditional_key, key)

            colors = func.assign_color_gradient(list(category_distribution.keys()), primary_color, negative_color)
            colors_list = list(colors.values())

            df = pd.DataFrame(list(category_distribution.items()), columns=[conditional_key, key])

            # Create the Altair doughnut chart
            chart = alt.Chart(df).mark_arc(innerRadius=40).encode(
                theta=key,
                color=alt.Color(f'{conditional_key}:N', scale=alt.Scale(range=colors_list)),
                tooltip=[conditional_key, key]
            ).properties(
                width=250,
                height=250
            ).interactive()

            col1, col2 = st.columns(2)

            # Display the Altair chart in Streamlit
            st.altair_chart(chart, use_container_width=True)

        indexing_column = 'Invoice Number'
        columns_to_return = ['Quantity', 'Amount', 'Tax Amount', 'Total Amount']

        invoices = func.retrieve_invoices(indexing_column, columns_to_return, FILEPATH_INVOICES)

        invoice_df = df = pd.DataFrame.from_dict(invoices, orient='index')


        with c2:
            st.subheader('Recent Invoices')
            range = st.selectbox('Show last', [10, 20, 30, 40, 50])
            st.table(invoice_df[:range])
