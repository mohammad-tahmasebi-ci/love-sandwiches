import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('lovesandwiches.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')


# sales = SHEET.worksheet('sales')

# data = sales.get_all_values()
# print(data)


def get_sales_data():

    """
    Get sales data from the user
    """

    while True:
        print('Please enter sales data from the last market')
        print('Data should be six numbers, separated by commas')
        print('Example: 10,20,30,40,50,60')

        data_str = input('Enter your data here: ')
        sales_data = data_str.split(',')
        if validate_data(sales_data):
            break
    
    return sales_data

def validate_data(values):

    """ 
    Converts all string values into integers
    Raises ValueError if strings can not be converted into integer
    or if there aren't exactly 6 values
    """

    try:
        values = [int(val) for val in values]
        if len(values) != 6:
            raise ValueError(f'Exactly 6 values is required, you provided {len(values)}')
    except ValueError as e:
        print(f'Invalid data: {e}, please try again.\n')
        return False
    return True

def update_worksheet(data, worksheet):

    """
    update sales and surplus worksheets based on data
    provided by the user
    """

    print(f'update {worksheet} worksheet...\n')
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f'{worksheet} worksheet updated successfully\n')

def calculate_surplus_data(sales_row):

    """
    compare sales with stock and calculate the surplus for each item type

    the surplus is defined as the sales figure subtracted from the stock:
    - positive surplus indicates waste
    - negative surplus indicates extra made when stock was sold out
    """

    print('calculating surplus data...\n')
    stock = SHEET.worksheet('stock').get_all_values()
    stock_row = stock[-1]
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    return surplus_data

def get_last_5_entries_sales():
    
    """
    collect columns of data from sales worksheet, collecting
    the last 5 entries for each sandwich and returns the data
    as a list of lists
    """
    
    sales = SHEET.worksheet('sales')
    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    
    return columns

def calculate_stock_data(data):
    """
    calculate the average stock for each item type, adding 10%
    """

    print('calculating stock data...\n')
    new_stock_data = []
    for col in data:
        int_col = [int(num) for num in col]
        avg = sum(int_col) / len(int_col)
        stock_num = avg * 1.1
        new_stock_data.append(round(stock_num))
    
    return new_stock_data

def stock_data_as_dictionary(stock_data):
    
    """
    converts stock_data into a dictionary
    """
    
    stock_sheet_cols = SHEET.worksheet('stock').row_values(1)
    stock_data_dictionary = {}
    for item, qty in zip(stock_sheet_cols, stock_data):
        stock_data_dictionary[item] = qty
    
    print(stock_data_dictionary)

def main():

    """
    run all program functions
    """

    data = get_sales_data()
    sales_data = [int(val) for val in data]
    update_worksheet(sales_data, 'sales')
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, 'surplus')
    sales_column = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_column)
    stock_data_as_dictionary(stock_data)
    update_worksheet(stock_data, 'stock')


print('welcome to love sandwiches data automation')
main()


