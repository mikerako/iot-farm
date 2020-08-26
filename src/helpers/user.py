'''
Module containing User and Users classes for accessing basic user info.

Author: Kevin Kraydich <kevin.kraydich@gmail.com>
'''

import re

class User:
    '''
    Class for storing name, number, and email address.
        params: Dictionary containing a user's name, phone number, and email address
    '''
    def __init__(self, params: dict):
        self.name = params['name']
        self.number = params['number']
        self.email = params['email']


class Users:
    '''
    Class for storing and accessing valid user data.
        users_info: List of dictionaries containing user info
    '''
    def __init__(self, users_info = []):
        self._users = []

        # Add specified users, if any
        for user_info in users_info:
            self.add_user(user_info)
    
    def add_user(self, user_info: dict):
        '''
        Adds a user to the list of users.
            user_info - Dictionary containing user info
        '''
        if self.validate(user_info):
            self._users.append(User(user_info))
        else:
            pass
            # logging.error('Improper formatting of user with name {}'.format(user_info['name']))

    def get_emails(self) -> list:
        '''
        Returns a list of users' email addresses.
        '''
        return [user.email for user in self._users]

    def get_numbers(self) -> list:
        '''
        Returns a list of users' phone numbers.
        '''
        return [user.number for user in self._users]

    def get_users(self) -> list:
        '''
        Returns a list of users.
        '''
        return self._users
    
    def validate(self, user_info: dict) -> bool:
        '''
        Validates user info based on whether the number/email is properly formatted.
            user_info - Dictionary containing user info
        '''
        return validate_number(user_info['number']) and validate_email(user_info['email'])


def validate_number(phone_number: str) -> bool:
    '''
    Checks whether a phone number adheres to E.164 formatting (see <https://www.twilio.com/docs/glossary/what-e164>).
        phone_number - String containing the phone number
    '''
    regexp = r'^\+[1-9]\d{1,14}$'
    return re.match(regexp, phone_number) is not None

def validate_email(email: str) -> bool:
    '''
    Checks whether an email address is properly formatted.
        email - String containing email address
    '''
    regexp = r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
    return re.match(regexp, email) is not None
