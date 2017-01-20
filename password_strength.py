import re
import os
from getpass import getpass

REGULAR_EXPRESSIONS = [
    {'expression': r'\d',
     'message': 'The password must have a numbers!',
     'rate': 1},
    {'expression': r'[A-Z]',
     'message': 'The password must have a large letters!',
     'rate': 2},
    {'expression': r'[a-z]',
     'message': 'The password must have a small letters!',
     'rate': 1},
    {'expression': r'\d\d.\d\d.\d\d\d\d',
     'message': 'The password should not look like a date',
     'rate': 0,
     'date_search': True},
    {'expression': r'[$*#!@^%_?]',
     'message': 'The password must have a special characters,\
such as @, #, $!',
     'rate': 3},
    {'expression': r'.{8}',
     'message': 'The length should be longer than 8 characters',
     'rate': 3},
]


def get_black_list(black_list_file_name):
    if not os.path.exists(black_list_file_name):
        return None
    with open(black_list_file_name, 'r') as file_handler:
        return file_handler.read().split()


def check_password_in_blacklist(password, black_list):
    if password not in black_list:
        return 0, None
    else:
        return -2, 'Password in BlackList!'


def get_password_strength(user_password, regular_expression):
    if 'date_search' not in regular_expression:
        if not re.search(regular_expression['expression'], user_password):
            return 0, regular_expression['message']
        else:
            return regular_expression['rate'], None
    else:
        if re.search(regular_expression['expression'], user_password):
            return 0, regular_expression['message']
        else:
            return regular_expression['rate'], None


if __name__ == '__main__':
    password = getpass("Enter the Password:")
    print("Password: {}".format(password))
    password_rate = 0
    messages = []
    blacklist_check = check_password_in_blacklist(
        password, get_black_list('blacklist.txt'))
    password_rate += blacklist_check[0]
    if blacklist_check[1]:
        messages.append(blacklist_check[1])
    for expression in REGULAR_EXPRESSIONS:
        expression_result = get_password_strength(
            password, expression)
        password_rate += expression_result[0]
        if expression_result[1]:
            messages.append(expression_result[1])
    print('The strength of a password equal to {}'.format(password_rate))
    for message in messages:
        print(message)
