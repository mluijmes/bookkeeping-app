import pandas as pd
import csv
import pandas as pd
import numpy as np
import matplotlib.colors as mcolors
import locale
from datetime import datetime
import requests

def get_device_country():
    """
    Returns the country of the device based on its IP address.
    """
    try:
        # Get the public IP address of the device using ipinfo.io
        response = requests.get("https://ipinfo.io")
        data = response.json()

        # Extract the country information
        country = data.get("country")

        if country:
            return country
        else:
            return "Country not found"
    except Exception as e:
        return str(e)


def get_current_timestamp():
    """
    Returns the current timestamp in the format 'YYYY-MM-DD HH:MM:SS'.
    """
    current_time = datetime.now()
    formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_time


def retrieve_invoices(indexing_column, columns_to_return, csv_file_path):
    # Initialize a dictionary to store the grouped rows
    grouped_rows = {}

    # Open and read the CSV file
    with open(csv_file_path, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')

        # Iterate through each row in the CSV
        for row in reader:
            # Get the value from the indexing column
            index_value = row[indexing_column]

            # Create a new dictionary for this row if it doesn't exist
            if index_value not in grouped_rows:
                grouped_rows[index_value] = {}

            # Populate the grouped dictionary with the selected columns
            for column in columns_to_return:
                grouped_rows[index_value][column] = row.get(column, None)

    return grouped_rows




def format_currency(amount, currency_symbol="$", locale_name="en_US", decimal_places=2):
    # Set the locale for formatting
    locale.setlocale(locale.LC_ALL, locale_name)

    # Format the amount as currency with the specified decimal places
    formatted_amount = locale.format_string(f"%.{decimal_places}f", amount, grouping=True)

    # Replace the default currency symbol with the desired symbol
    formatted_amount = formatted_amount.replace(locale.localeconv()['currency_symbol'], currency_symbol)

    return f'{currency_symbol}{formatted_amount}'

def assign_color_gradient(item_list, color_start, color_end):
    colormap = mcolors.LinearSegmentedColormap.from_list("custom", [color_start, color_end], N=len(item_list))
    interpolated_colors = [colormap(i) for i in np.linspace(0, 1, len(item_list))]
    color_hex_values = [mcolors.to_hex(color) for color in interpolated_colors]

    color_dict = {item: color_hex for item, color_hex in zip(item_list, color_hex_values)}

    return color_dict


def sum_invoice_amounts_by_month(csv_file, column):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file, delimiter=';')

    # Convert the date column to a datetime object
    df['Date'] = pd.to_datetime(df['Date'])

    # Extract month and year from the date
    df['Month'] = df['Date'].dt.strftime('%B')

    # Group the data by month and sum the invoice amounts
    monthly_totals = df.groupby('Month')[column].sum().reset_index()

    # Create a list of all months
    all_months = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]

    # Create a dictionary with all months initialized to 0
    result_dict = {month: 0 for month in all_months}

    # Update the dictionary with the calculated totals
    result_dict.update(dict(zip(monthly_totals['Month'], monthly_totals[column])))

    return result_dict


def get_csv_keys(csv_file):
    """
    Reads a CSV and returns the column headers as a list.
    :param csv_file: Path of the file location.
    :return: A list of headers.
    """
    try:
        df = pd.read_csv(csv_file, delimiter=';')
        columns = df.columns.tolist()
        return columns
    except Exception as e:
        return str(e)


def csv_conditional_sum(file_path, condition_column, condition_key):
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path, delimiter=';')

        # Filter the DataFrame based on the condition
        filtered_df = df[df[condition_column] == condition_key]

        # Aggregate and sum the 'QUANTITY' column for the filtered data
        total_quantity = filtered_df['QUANTITY'].sum()

        return total_quantity
    except Exception as e:
        return f"An error occurred: {str(e)}"


def csv_category_sum(file_path, condition_column, sum_column):
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path, delimiter=';')

        # Group the data by the category column and calculate the sum of 'QUANTITY'
        category_sum = df.groupby(condition_column)[sum_column].sum().to_dict()

        return category_sum
    except Exception as e:
        return f"An error occurred: {str(e)}"


def csv_conditional_filter(file_path, condition_column, condition_key):
    filtered_data = []

    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file, delimiter=';')

        for row in reader:
            if row.get(condition_column) == condition_key:
                filtered_data.append(row)

    return filtered_data


def get_csv_column(csv_file, key):
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_file, delimiter=';')

        # Check if the key exists as a column header
        if key in df.columns:
            # Return the specified column as a list
            return df[key].tolist()
        else:
            return None  # Key not found in columns
    except Exception as e:
        return None  # Error occurred while reading the CSV file


def filter(file_path, invoice_number):
    """
    Filter a CSV file to keep only rows with a specific invoice number.

    :param file_path: The file location of the CSV.
    :param invoice_number: The invoice number to filter by.
    :return: Filtered DataFrame.
    """
    df = pd.read_csv(file_path, delimiter=';')
    filtered_df = df[df['Invoice Number'] == invoice_number]
    return filtered_df


def delete_invoice(csv_file_path, invoice_number):
    """
    Delete all rows in CSV file associated with the specified invoice number.
    :param csv_file_path: The file location of the CSV.
    :param invoice_number: The invoice number to identify the rows to delete.
    """
    df = pd.read_csv(csv_file_path, sep=';')
    df = df[df["Invoice Number"] != invoice_number]
    df.to_csv(csv_file_path, sep=';', index=False)


def select_last_activity(csv_file_path, column):
    """
    Groups data based on their invoice number.
    :param csv_file_path: The file location of the CSV.
    :return: Invoice Data.
    """
    df = pd.read_csv(csv_file_path, sep=';')
    last_activity_df = df.groupby(column).last().reset_index()
    return last_activity_df


def sort_csv_by_invoice_number(file_path):
    """
    Sorts a CSV file by the 'Invoice Number' column and rewrites the CSV with the sorted data.
    :param file_path: The file location of the CSV.
    """
    df = pd.read_csv(file_path, sep=';')
    df_sorted = df.sort_values(by='Invoice Number')
    df_sorted.to_csv(file_path, sep=';', index=False)


def read_settings(file_path):
    """
    Read key/value like settings from a .txt file.
    :param file_path: The path of the txt. settings file.
    :return: All settings as a list.
    """
    settings = {}
    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            settings[key] = value
    return settings


def get_setting_value(file_path, key):
    """
    Get a specific value from a key from a settings.txt file.
    :param file_path: The path of the txt. settings file.
    :param key: The key of the value to retrieve.
    :return: The value belonging to given key.
    """
    settings = read_settings(file_path)
    return settings.get(key, None)  # Return None if key doesn't exist


def update_setting(file_path, key, new_value):
    """
    Update a given key with a new value in a settings.txt file.
    :param file_path: The path of the txt. settings file.
    :param key: The key of the value to adjust.
    :param new_value: The new value given key.
    """
    settings = read_settings(file_path)
    settings[key] = new_value
    with open(file_path, 'w') as file:
        for key, value in settings.items():
            file.write(f'{key}={value}\n')


def append_loclist_row(row, filepath):
    """
    Function that appends a row to a csv file.
    :param row: The text row to append.
    :param filepath: The path of the csv file.
    """
    with open(filepath, 'a', newline='', encoding='utf-8') as path:
        path.write(row + '\n')  # Append a newline character at the end of the row


def get_last_invoice_number(csv_file_path):
    """
    Reads the first column of the bottom-most row in a CSV file.

    :param csv_file_path: The path to the CSV file.
    :return: The value in the first column of the last row, or None if the file is empty or an error occurs.
    """
    try:
        df = pd.read_csv(csv_file_path, sep=';')
        last_row = df.iloc[-1]
        first_column_value = last_row.iloc[0]
        return first_column_value
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return 0


def clear_loclist(file_path):
    """
    Function that clears a txt. or csv. file from its contents.
    :param file_path: The path of the txt. or csv. file.
    """
    try:
        with open(file_path, 'w') as text_file:
            pass  # Open the text file in write mode without writing anything
    except Exception as e:
        return f"Error clearing the file: {e}"


def read_csv_rows(file_path):
    """
    Reads a CSV file without the header row.
    :param file_path (str): The path to the CSV file.
    :return: A list of rows from the CSV file without the header.
    """
    try:
        df = pd.read_csv(file_path, header=None)
        data = df.values.tolist()
        return data[1:]  # Exclude the first row (header)
    except FileNotFoundError:
        return []  # Return an empty list if the file doesn't exist


def clear_csv(file_path):
    """
    Function that clears the contents of a CSV file, except for the header row.
    :param file_path: The path of the CSV file.
    """
    try:
        # Read the header row
        with open(file_path, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            header_row = next(reader)

        # Clear the file by opening it in write mode
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # Write the header row back to the file
            writer.writerow(header_row)

    except Exception as e:
        return f"Error clearing the file: {e}"


def get_loclist_length(filepath):
    """
    Function that returns the length from a txt. or csv. file, assuming each row is 1.
    :param filepath: The path of the txt. or csv. file.
    :return: Returns the length of the file.
    """
    with open(filepath, 'r') as file:
        row_count = sum(1 for line in file)
    return row_count


def overwrite(filepath, content):
    try:
        # Open the file in write mode ('w') to overwrite its contents
        with open(filepath, 'w') as file:
            # Write each item in the content list as a separate line
            for item in content:
                file.write(str(item))

        return True  # Operation successful
    except Exception as e:
        print(f"Error: {e}")
        return False  # Operation failed


def get_loclist_txt(filepath):
    """
    Function that fetches list from a txt. file.
    :param filepath: The path of the txt. file.
    :return: Returns the lines in the txt file.
    """
    with open(filepath, 'r') as file_local:
        list = file_local.readlines()
        return list


def write_loclist_txt(list, filepath):
    """
    Function that writes list into a txt. file.
    :param filepath: The path of the txt. file.
    :param list: The new list to write.
    """
    with open(filepath, 'w') as file_local:
        file_local.writelines(list)


def filter_column_by_date_range(file_path, column_name, start_date, end_date):
    """
    Searches a column and filters items that are within the date range.
    :param file_path: The path of the txt. file.
    :param column_name: Name of the column header to search in.
    :param start_date: Date start
    :param end_date: Date end
    :return: A list of filtered items.
    """
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path, delimiter=';')

        # Convert date columns to datetime objects for comparison
        df['Date'] = pd.to_datetime(df['Date']).dt.date  # Extract date part only

        # Filter the DataFrame based on the date range
        filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

        # Extract the values in the specified column and corresponding dates
        column_values = filtered_df[column_name].tolist()
        dates = filtered_df['Date'].tolist()
        return dates, column_values
    except Exception as e:
        return [], []


def append_row_to_csv(filepath, row_data):
    """
    Append a list item as a row of text into a txt. file.
    :param row_data: The new line of text or code to append to the txt. list file.
    :param filepath: The path of the txt. file.
    :return: Returns the modified list.
    """
    list = get_loclist_txt(filepath)
    new_item = row_data
    list.append(new_item)
    write_loclist_txt(list, filepath)
    return list


def merge_csv_files(file1_path, file2_path, output_path):
    try:
        df1 = pd.read_csv(file1_path)
        df2 = pd.read_csv(file2_path)
        merged_df = pd.concat([df1, df2], ignore_index=True)
        merged_df.to_csv(output_path, index=False)
    except Exception as e:
        return f"An error occurred: {str(e)}"


def add_loclist_txt(item, filepath):
    """
    Append a list item as a row of text into a txt. file.
    :param item: The new line of text or code to append to the txt. list file.
    :param filepath: The path of the txt. file.
    :return: Returns the modified list.
    """
    list = get_loclist_txt(filepath)
    new_item = item + '\n'
    list.append(new_item)
    write_loclist_txt(list, filepath)
    return list


def remove_loclist_txt(index, filepath):
    """
    Removes a row (item) from a txt.file.
    :param index: The index of the list item to remove.
    :param filepath: The path of the txt. file.
    :return: Returns the modified list.
    """
    list = get_loclist_txt(filepath)
    list.pop(index)
    write_loclist_txt(list, filepath)
    return list


def edit_loclist_txt(item, index, filepath):
    """
    Modifies a row (item) from a txt.file by replacing it with a new one.
    :param item: New text item.
    :param index: Index of the item to edit.
    :param filepath: The path of the txt.file.
    :return: Returns the modified list.
    """
    list = get_loclist_txt(filepath)
    list.pop(index)
    list.insert(index, item)
    write_loclist_txt(list, filepath)
    return list
