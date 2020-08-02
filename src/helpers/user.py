import re

class User:
    '''
    Class for storing name, number, and email address.
    '''
    def __init__(self, params: dict):
        self.name = params['name']
        self.number = params['number']
        self.email = params['email']


class UserList:
    '''
    Class for storing and accessing valid user data.
    '''
    def __init__(self, users_info = []):
        self._users = []

        # Add specified users, if any
        for user_info in users_info:
            self.add_user(user_info)
    
    def add_user(self, user_info: dict):
        '''
        Adds a user to the list of users.

        Keyword arguments:
            user_info - Dictionary containing information about the user
        '''
        if self.validate(user_info):
            self._users.append(User(user_info))
        else:
            pass
            # logging.error('Improper formatting of user with name {}'.format(user_info['name']))

    def get_emails(self) -> list:
        return [user.email for user in self._users]

    def get_numbers(self) -> list:
        return [user.number for user in self._users]

    def get_users(self) -> list:
        return self._users
    
    def validate(self, user_info: dict) -> bool:
        return validate_number(user_info['number']) and validate_email(user_info['email'])


def validate_number(phone_number: str) -> bool:
    regexp = r'^\+[1-9]\d{1,14}$'
    return re.match(regexp, phone_number) is not None

def validate_email(email: str) -> bool:    
    regexp = r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
    return re.match(regexp, email) is not None
