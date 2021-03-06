"""
Contains all modules imported to provide and export live data such as
operating system, email formats, current Coordinated Universal Timezone
and google sheets
"""
import os
import re
import datetime
from datetime import timezone
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive'
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('n3orthotics')
REGEX = r'^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$'

user_data = ['f_name', 'l_name', 'user_email']
order_data = [
    'size_eu', 'height', 'width', 'order_no', '', 'order_status', '', 'row_no'
    ]
update_order = ['order_status', 'order_update']
export_data = []
search_row = [0]


def start():
    """
    Start screen prompting user to Create or Retrieve an existing order
    using an order number
    """
    print('Welcome to N(3)ORTHOTICS order portal.\n')
    print('Use this app to directly access made-to-order N3D Printed Insoles')
    print('Please visit northotics.com/home for more information\n')
    print('Select 1. : Place a new N3D insole order')
    print('Select 2. : Retrieve an existing N3D order')
    print('Select 3. : Exit Program\n')


def select_option():
    """
    Initial user choice to place a new or retrieve an existing N3D order
    """
    correct = input('Your Selection: ')
    for selection in correct:
        if selection == '1':
            return True
        elif selection == '2':
            clear_screen()
            print('Retrieve an existing N3D insole order : \n')
            display_order()
        elif selection == '3':
            clear_screen()
            quit()
        else:
            print(
                f'The number you have provided "{correct}" is not available.')
            print('Please select again\n')
            select_option()


def instruct_user_data():
    """
    Instruct User on format of first name, last name and email.
    """
    clear_screen()
    print('Place a N(3)ORTHOTICS.com N3D printed insole order:\n')
    print('Where prompted below, please enter your name and email.')
    print('This information should be in a valid syntax, with no spaces.')
    print('For example:\n')
    print('First Name: Rob\nLast Name: Bertoez')
    print('Email: rubbertoez@yourdomain.com\n')


def get_user_data():
    """
    User input of first name, last name and email to from a string
    with fist letter capitalized for names and all lowercase email
    """
    f_name = remove_blank_space(input('Your First Name: ').capitalize())
    validate_user_f_name(f'{f_name}')
    f_name = user_data[0]

    l_name = remove_blank_space(input('Your Last Name: ').capitalize())
    validate_user_l_name(f'{l_name}')
    l_name = user_data[1]

    user_email = remove_blank_space(input('Your Email: ').lower())
    validate_user_email(f'{user_email}')
    user_email = user_data[2]


def summary_user_data():
    """
    Produces a readable summary of the current user_data list
    """
    print(f'Full Name : {user_data[0]} {user_data[1]}\nEmail : {user_data[2]}')


def summary_order_data():
    """
    Produces a summary of the current order data stored locally
    """
    size_eu = order_data[0]
    height = order_data[1]
    width = order_data[2]
    print('\nYour order details are as follows:')
    summary_user_data()
    print(f'Shoe Size : EU {size_eu}')
    print(f'Arch Height : {height}')
    print(f'Insole Width : {width}')


def validate_user_f_name(values):
    """
    Inside the try, checks all user input syntax.
    Raises ValueError if strings cannot be converted and prompts to
    replace data in index [0] of the user_data list = f_name
    """
    try:
        if values.isalpha():
            user_data[0] = values.capitalize()
        else:
            raise ValueError(
                f'The name you have provided "{values}" does not seem'
                f'\nto be in a regular format'
            )
    except ValueError as error:
        print(
            f'\nInvalid data: {error}. Please check the entry and try again.\n'
            )
        f_name = remove_blank_space(input('Your First Name : ').capitalize())
        validate_user_f_name(f_name)
        user_data[0] = f_name


def validate_user_l_name(values):
    """
    Inside the try, checks all user input syntax.
    Raises ValueError if strings cannot be converted and prompts to
    replace data in index [1] of the user_data list = l_name
    """
    try:
        if values.isalpha():
            user_data[1] = values.capitalize()
        else:
            raise ValueError(
                f'The name you have provided "{values}" does not seem'
                f'to be in a regular format'
            )
    except ValueError as error:
        print(
            f'\nInvalid data: {error}. Please check the entry and try again.\n'
            )
        l_name = remove_blank_space(input('Your Last Name : ').capitalize())
        validate_user_l_name(l_name)
        user_data[1] = l_name


def validate_user_email(values):
    """
    Inside the try, checks all user email input syntax.
    Raises ValueError if strings cannot be converted and prompts to
    replace data in index [2] of the user_data list = user_email
    """
    try:
        if re.fullmatch(REGEX, values):
            print('Email is valid...')
            user_data[2] = values.lower()
            clear_screen()
        else:
            raise ValueError(
                f'The email you have provided "{values}" does not seem'
                'to be in a regular format'
            )
    except ValueError as error:
        print(
            f'\nInvalid data: {error}. Please check the entry and try again.\n'
            )
        user_email = remove_blank_space(input('Your Email: ').lower())
        validate_user_email(user_email)
        user_data[2] = user_email


def remove_blank_space(string):
    """
    Removes all spaces in string inputs
    """
    return string.replace(' ', '')


def get_latest_row_entry():
    """
    Prints a list to the terminal of the row last updated
    between columns A to F in the worksheet
    """
    orders = SHEET.worksheet('orders').get_values('A:G')
    latest = orders[-1]
    print(latest)


def yes_no_user():
    """
    Prompt for user to confirm or input correct user_data
    """
    summary_user_data()
    correct = input('\nIs this information correct? y/n: ').lower()
    if correct.startswith('y'):
        clear_screen()
        f_name = user_data[0]
        print(
            f'Thanks {f_name}. Now lets customise your N3 Orthoses order...'
            )
        get_order_data()
        generate_order_no()
        combine_data_for_export()
        summary_order_data()
        submit_order()
    else:
        clear_screen()
        get_user_data()


def get_order_data():
    """
    Collection of User input used to order N3D Orthosis.
    """
    get_size_data()
    get_height_data()
    get_width_data()


def get_size_data():
    """
    Converts to a float() between EU shoe size between EU19 and EU50 only.
    Inside the try, converts all string values into floating points and
    raises ValueError if not a number.
    """
    while True:
        try:
            size_eu = float(remove_blank_space(input(
                '\nWhat EU Shoe Size would you like to fit into?'
                '\n(sized in 0.5 increments between 19 and 50): '
                )))
            size_divisble = size_eu % 0.5

            if size_eu >= 19 and size_eu <= 50:
                if size_divisble != 0:
                    print(
                        '\nIncorrect information provided for European'
                        f'shoe sizing: {size_eu}'
                        )
                    get_size_data()
                else:
                    order_data[0] = size_eu
                    return size_eu
            else:
                print(
                    f'\nUnfortunatley {size_eu} is not within the European'
                    'shoe size range we do.'
                    )
                get_size_data()
        except ValueError as error:
            print(f'Invalid data : {error}, please try again.\n')
            continue


def get_height_data():
    """
    Height user input converted into ['Low', 'Med', 'High'] for order_data
    Only strings starting with l, m or h accepted. Not case sensitive.
    """
    height = remove_blank_space(input(
        '\nWhat level of support under the inside arch would you like?'
        '\n(L: Low Support / M: Medium Support / H: High Support): '
        ).lower())
    if height.startswith('l'):
        order_data[1] = 'Low'
    elif height.startswith('m'):
        order_data[1] = 'Medium'
    elif height.startswith('h'):
        order_data[1] = 'High'
    else:
        print(f'\nIncorrect information provided for arch height: {height}')
        get_height_data()


def get_width_data():
    """
    Width user input converted into ['Narrow', 'Standard', 'Wide'] for
    order_data
    """
    width = remove_blank_space(input(
        '\nWidth of insole to fit the foot &/or shoe'
        '\n(N: Narrow / S: Standard / W: Wide): '
        ).lower())
    if width.startswith('n'):
        order_data[2] = 'Narrow'
    elif width.startswith('s'):
        order_data[2] = 'Standard'
    elif width.startswith('w'):
        order_data[2] = 'Wide'
    else:
        print(f'\nIncorrect information provided for insole width: {width}')
        get_width_data()


def combine_data_for_export():
    """
    Loops through user_data then order_data to create single export_data
    list in preparation to update_order_worksheet
    """
    clear_screen()
    export_data.clear()
    for value in user_data:
        export_data.append(value)
    for value in order_data:
        export_data.append(value)
    export_data.pop()
    return export_data


def clear_screen():
    """
    Checks if Operating System is Mac and Linux or Windows and
    clears the screen. Sourced from:
    https://codecap.org/clear-screen-in-python/
    """
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        _ = os.system('cls')


def slice_last_order_no():
    """
    Steps order number back by one value to account for the heading information
    within gsheets document.
    """
    order_no = SHEET.worksheet('orders').get_values('G:G')
    last_index = len(order_no) - 1
    last_entry = order_no[last_index]
    last_entry_int = last_entry[0]
    slice_last_digit = slice(6)
    reset_no = int(last_entry_int[slice_last_digit])
    reset_no_to_ten_thousand = reset_no * 10000
    return reset_no_to_ten_thousand


def generate_order_no():
    """
    Generates an order number with todays date + increment from previous
    order entry in worksheet
    """
    order_no = SHEET.worksheet('orders').get_values('G:G')
    last_index = len(order_no) - 1
    last_entry = order_no[last_index]
    last_entry_int = int(last_entry[0])
    now = datetime.datetime.now(timezone.utc)
    order_date = now.strftime('%y%m%d')
    new_order_no = (
        int(order_date)*10000) + (last_entry_int - slice_last_order_no() + 1)
    order_data[3] = new_order_no
    return new_order_no


def generate_utc_time():
    """
    Creates Universal Coordinated Time (UTC) ISO version of date and time
    """
    iso_utc_now = datetime.datetime.now(timezone.utc).isoformat()
    return iso_utc_now


def update_date_ordered():
    """
    Updates the order_date filed within order_data list
    """
    time_zone = generate_utc_time()
    order_data[4] = time_zone
    order_data[5] = 'NEW ORDER'


def generate_row_no():
    """
    Retrieves current row data length and extends it by 1 value
    """
    row_data = SHEET.worksheet('orders').get_values('K:K')
    new_row_no = len(row_data) + 1
    export_data.append(new_row_no)


def update_to_pending_status():
    """
    Updates status to pending when user saves order
    """
    time_zone = generate_utc_time()
    export_data[9] = time_zone
    export_data[8] = 'PENDING'
    export_data[7] = ''
    new_order_no = generate_order_no()
    export_data[6] = new_order_no
    generate_row_no()
    order_worksheet = SHEET.worksheet('orders')
    order_worksheet.append_row(export_data)
    clear_screen()
    print('Data successfully saved as PENDING.')
    print(
        f'\nPlease carefully record order no : {export_data[6]}'
        '\nYou will need it to recall this item into the future.'
        )


def input_order_no():
    """
    Checks the user input order number is only numerical and correct length
    """
    print('Please enter your order number below.')
    print(
        'This information should be in a valid syntax, with no spaces.'
        'For example:\n'
        )
    print('Example order_no format: 2205190001\n')
    while True:
        try:
            order_no = int(remove_blank_space(input('You Order Number: ')))
            search_row[0] = order_no
            order_no_string = str(order_no)
            if len(order_no_string) != 10:
                raise ValueError(
                    'Our order numbers require 10 digits.'
                    f'\nUnfortunatley {order_no} has {len(order_no_string)}'
                    ' digits.'
                )
        except ValueError as error:
            print(
                f'Invalid data : {error}'
                '\nPlease check your records and try again below;\n')
            continue
        return order_no


def flatten_nested_list(input_list):
    """
    Flattens a nested list into a list
    """
    flattened_list = []
    for value in input_list:
        if isinstance(value, list):
            flattened_list.extend(flatten_nested_list(value))
        else:
            flattened_list.append(value)
    return flattened_list


def retrieve_order():
    """
    Searches worksheet coloum 'order_no' for a match to user input and
    returns row information to local user_data, oder_data and export_data lists
    """
    search_input = str(input_order_no())
    order_nos_import = SHEET.worksheet('orders').get_values('G:G')
    order_nos = flatten_nested_list(order_nos_import)
    order_match = [
        index_no for index_no in range(len(order_nos))
        if order_nos[index_no] == search_input
        ]
    if order_match == []:
        clear_screen()
        print(f"Order number '{search_input}' NOT FOUND?\n")
        retrieve_order()
    else:
        row_location = [
            index_no for index_no, order_no in enumerate(order_nos, 1)
            if order_no == search_input
            ]
        search_match_row = row_location[0]
        search_row[0] = search_match_row


def display_order():
    """
    Gets orders by row from worksheet
    Converts specific string values back into integers and
    Displays entire order as a list
    """
    retrieve_order()
    row = search_row[0]
    order_row = SHEET.worksheet('orders').get_values(f'A{row}:K{row}')
    flat_order = flatten_nested_list(order_row)
    size_eu = flat_order[3]
    flat_order[3] = float(size_eu)
    order_no = flat_order[6]
    flat_order[6] = int(order_no)
    user_data[0:3] = flat_order[0:3]
    order_data[0:6] = flat_order[3:9]
    order_data[7] = int(row)

    combine_data_for_export()
    print('Your order details are as follows:\n')
    print(
        f'Full Name : {user_data[0]} {flat_order[1]}\nEmail : {flat_order[2]}'
        )
    print(
        f'Shoe Size : EU {flat_order[3]}'
        f'\nArch Height : {flat_order[4]}'
        f'\nInsole Width : {flat_order[5]}'
        )
    print(
        f'Order No. : {flat_order[6]}'
        f'\nDate Ordered : {flat_order[7]}'
        f'\nCurrent Status : {flat_order[8]}')
    print(f'Row : {flat_order[10]}\n')
    update_status()


def validate_change_feature_of_order():
    """
    Validates order is prior to 'SUBMITTED TO PRINT' stage for
    change_feature_of_order function
    """
    row = order_data[7]
    order_row = SHEET.worksheet('orders').get_values(f'A{row}:K{row}')
    flat_order = flatten_nested_list(order_row)
    print(f'Current order status is: {flat_order[8]}')
    if flat_order[8] == 'PENDING' or flat_order[8] == 'NEW ORDER' or \
            flat_order[8] == 'UPDATED ORDER' or flat_order[8] == 'CREATED' or \
            flat_order[8] == 'ACCEPTED' or flat_order[8] == 'DESIGNED':
        print('Order is modifiable.')
        print('\nYour order details are as follows:\n')
        print(
            f'Order No. : {flat_order[6]}'
            f'\nDate Ordered : {flat_order[7]}'
            f'\nDatabase Row entry : {flat_order[10]}'
            f'\nCurrent Status : {flat_order[8]}'
            )
        print('\nDetails you can edit:\n')
        print(
            f'1. First Name : {user_data[0]}'
            f'\n2. Surname : {user_data[1]}'
            f'\n3. Email : {user_data[2]}'
            )
        print(
            f'4. Shoe Size : EU {order_data[0]}'
            f'\n5. Arch Height : {order_data[1]}'
            f'\n6. Insole Width : {order_data[2]}\n'
            )
        print(
            '7. Submit the above details'
            '\n8. Take me Home\n'
            )
        change_feature_of_order()
    else:
        print(
            f'\nAt the {flat_order[8]} stage, this order is beyond the point'
            ' in production\nwhere modifications can occur.'
            )
        email_print_update_startover()


def change_feature_of_order():
    """
    Generates a list to choose which feature of an existing order to change
    """
    feature_selection = input('Your Selection : ')
    if feature_selection == '1':
        clear_screen()
        f_name = input('New First Name details: ')
        clear_screen()
        validate_user_f_name(f_name)
        f_name = user_data[0]
        validate_change_feature_of_order()
    elif feature_selection == '2':
        clear_screen()
        l_name = input('New Last Name details: ')
        clear_screen()
        validate_user_l_name(l_name)
        l_name = user_data[1]
        validate_change_feature_of_order()
    elif feature_selection == '3':
        clear_screen()
        user_email = input('New Email details: ')
        validate_user_email(user_email)
        user_email = user_data[2]
        validate_change_feature_of_order()
    elif feature_selection == '4':
        clear_screen()
        get_size_data()
        clear_screen()
        validate_change_feature_of_order()
    elif feature_selection == '5':
        clear_screen()
        get_height_data()
        clear_screen()
        validate_change_feature_of_order()
    elif feature_selection == '6':
        clear_screen()
        get_width_data()
        clear_screen()
        validate_change_feature_of_order()
    elif feature_selection == '7':
        update_date_ordered()
        combine_data_for_export()
        submit_row_data()
    elif feature_selection == '8':
        combine_data_for_export()
        main()
    else:
        print(
            f'The number you have provided "{feature_selection}" is not part'
            'of this selection.'
            )
        print('Please select again\n')
        validate_change_feature_of_order()


def update_status():
    """
    Generates a list of user options to append details of an exsisting order to
    create new order details and/or navigate through the system
    """
    order_no = order_data[3]
    print(f'What would you like to do with order no. {order_no} ?')
    print('\nSelect 1. : Re-Print this order again (no changes)')
    print('Select 2. : Change the features')
    print('Select 3. : Place a new N3D insole order')
    print('Select 4. : Cancel order')
    print('Select 5. : Search different order')
    print('Select 6. : Take me home\n')
    startover = input('Your Selection: ')

    for selection in startover:
        if selection == '1':
            clear_screen()
            print(f'Re-printing order number : {order_no}...')
            submit_order()
        elif selection == '2':
            clear_screen()
            print(f'Order No. {order_no}')
            validate_change_feature_of_order()
        elif selection == '3':
            clear_screen()
            print('Starting a new N3D insole order...')
            yes_no_user()
        elif selection == '4':
            clear_screen()
            print(f'Checking the current status of order no. {order_no} ...')
            update_to_canceled_status()
        elif selection == '5':
            clear_screen()
            display_order()
        elif selection == '6':
            clear_screen()
            main()
        else:
            print(
                f'The number you have provided "{startover}" is not available.'
            )
            print('Please select again\n')
            email_print_update_startover()
    iso_format_timezone = generate_utc_time()
    update_order[1] = iso_format_timezone


def cancel_confirm():
    """
    Confirms the user input to cancel order and returns to main screen
    """
    confirm = input('Are you sure you wish to cancel this order? y/n : ')
    if confirm.startswith('y'):
        return True
    elif confirm.startswith('n'):
        main()


def update_to_canceled_status():
    """
    Updates status to pending when user saves order
    """
    row = order_data[7]
    order_worksheet = SHEET.worksheet('orders')
    print(f'Current order status is: {export_data[8]}')
    if export_data[8] == 'PENDING' or export_data[8] == 'NEW ORDER' or \
            export_data[8] == 'UPDATED ORDER' or export_data[8] == 'CREATED' \
            or export_data[8] == 'ACCEPTED' or export_data[8] == 'DESIGNED':
        print('Order is modifiable.\n')
        cancel_confirm()
        iso_format_timezone = generate_utc_time()
        export_data[9] = iso_format_timezone
        export_data[8] = 'CANCELED'
        order_worksheet.update(f'I{row}', f'{export_data[8]}')
        order_worksheet.update(f'J{row}', f'{export_data[9]}')
        print('\nOrder successfully CANCELED.')
        print(
            f"An email with it's credit note details will be sent to"
            f' {export_data[2]}'
            )
        print(
            f'\nPlease carefully record the order no. {export_data[6]}'
            '\nYou will need it to refer to this action into the future.'
            )
        email_print_update_startover()
    else:
        print(
            '\nUnfortunatley as a custom made product, this order is now at'
            f' the \n{export_data[8]} stage, manufacturing has commenced and'
            ' the opportunity\nto alter or cancel the order has passed.'
            )
        print(
            '\nFor further clarification of made-to-order products purchased'
            ' online,'
            '\nspecifically section 13(1)(c): UK Distance Selling'
            ' Regulations, please visit: '
            '\nhttps://www.legislation.gov.uk/uksi/2000/2334/contents/made '
            '\nAlternately, contact info@northotics.com referring order '
            'number :'
            f' {export_data[6]}'
            '\n\nYour purchasing rights have not been affected.'
            )
        email_print_update_startover()


def submit_row_data():
    """
    Replaces the existing row data in the worksheet with updated data and
    records the date of the order update
    """
    row = order_data[7]
    order_worksheet = SHEET.worksheet('orders')

    print(f'Accessing your order on row number : {row}')
    iso_format_timezone = generate_utc_time()
    export_data[9] = iso_format_timezone
    export_data[8] = 'UPDATED ORDER'
    order_worksheet.update(f'A{row}', export_data[0])
    order_worksheet.update(f'B{row}', export_data[1])
    order_worksheet.update(f'C{row}', export_data[2])
    order_worksheet.update(f'D{row}', float(export_data[3]))
    order_worksheet.update(f'E{row}', export_data[4])
    order_worksheet.update(f'F{row}', export_data[5])
    order_worksheet.update(f'G{row}', int(export_data[6]))
    order_worksheet.update(f'H{row}', export_data[7])
    order_worksheet.update(f'I{row}', export_data[8])
    order_worksheet.update(f'J{row}', export_data[9])

    print(f'\nOrder No. {export_data[6]} successfully updated!')
    print('Thanks for using the N(3)Orthotics order submission app.\n')
    update_status()


def submit_order():
    """
    User choice to deny or confirm order submission.
    Confirm compiles list from user_data and oder_data then exports it to
    update_sales-worksheet function
    """
    submit = input('\nWould you like to submit this order? y/n: ').lower()
    if submit.startswith('n'):
        save_order()
    else:
        clear_screen()
        generate_order_no()
        update_date_ordered()
        combine_data_for_export()
        generate_row_no()
        update_order_worksheet(export_data)
        recent_order_no = export_data[6]
        order_data[7] = export_data[10]
        submitted_time = export_data[7]
        print('Order Successfully Submitted!!')
        print(f'\nYour order number is: {recent_order_no}')
        print(f'Submitted on: {submitted_time}')
        summary_order_data()
        email_print_update_startover()


def update_order_worksheet(data):
    """
    Update sales google worksheet, add new row with the list data provided
    """
    print('Contacting the mothership...')
    order_worksheet = SHEET.worksheet('orders')
    order_worksheet.append_row(data)
    print('Information received...')


def save_order():
    """
    User decision to save order as pending within gsheets or
    clear all local data and return to main screen
    """
    save = input('\nWould you like to save this order? y/n: ').lower()
    if save.startswith('n'):
        order_data.clear()
        export_data.clear()
        clear_screen()
        main()
    else:
        export_data[7] = ''
        update_to_pending_status()
        email_print_update_startover()


def email_print_update_startover():
    """
    User decision tree to navigate following a successful submission,
    feature change, save or change of status
    """
    print('\nWhat would you like to do next?')
    print('Select 1. : Change the features of this Order')
    print('Select 2. : Place a new N3D insole order')
    print('Select 3. : Retrieve an existing N(3) order')
    print('Select 4. : Take Me Home')
    print('Select 5. : Exit the N(3)Orthotics order portal\n')
    startover = input('Your Selection: ')
    order_no = order_data[3]
    for selection in startover:
        if selection == '1':
            clear_screen()
            print(f'Order No. {order_no}')
            validate_change_feature_of_order()
        elif selection == '2':
            clear_screen()
            print('Starting a new N3D insole order...')
            yes_no_user()
        elif selection == '3':
            clear_screen()
            print('Retrieve an Exsisting Order...\n')
            display_order()
        elif selection == '4':
            print('Taking you to home page...\n')
            clear_screen()
            start()
            select_option()
        elif selection == '5':
            print('Exiting this n3orthotics session...\n')
            clear_screen()
            exit()
        else:
            print(
                f'The number you have provided "{startover}" is not available.'
                '\nPlease select again\n'
                )
            email_print_update_startover()


def main():
    """
    Run all primary program functions
    """
    clear_screen()
    start()
    select_option()
    instruct_user_data()
    get_user_data()
    clear_screen()
    yes_no_user()
    summary_order_data()
    combine_data_for_export()


main()
