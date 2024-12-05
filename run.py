import gspread
from google.oauth2.service_account import Credentials

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
        

def validate_data(values):

    """ 
    Converts all string values into integers
    Raises ValueError if strings can not be converted into integer
    or if there aren't exactly 6 values
    """

    try:
        [int(val) for val in values]
        if len(values) != 6:
            raise ValueError(f'Exactly 6 values is required, you provided {len(values)}')
    except ValueError as e:
        print(f'Invalid data: {e}, please try again.\n')
        return False
    
    return True
        
def update_sales_worksheet(data):
    
    """
    update sales worksheet, add new row with the list data provided
    """

    print('updating sales worksheet...\n')
    sales_worksheet = SHEET.worksheet('sales')
    sales_worksheet.append_row(data)
    print('sales worksheet updated successfully\n')


data = get_sales_data()
sales_data = [int(val) for val in data]
update_sales_worksheet(sales_data)
