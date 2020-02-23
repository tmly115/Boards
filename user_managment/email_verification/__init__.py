import datetime

from random import randint
import app_config
from .email_methods import send_validation_email


base_email_url = 'http://127.0.0.1:5000/verify_email/'




def verify_email(email, user_id):
    send_validation_email(email, generate_verification_code(email, user_id))




#Returns a URL which will activate the account.

def generate_verification_code(email, user_id):
    code = randint(1000000, 9999999)
    code_not_unique = True
    while code_not_unique:
        if(app_config.db.get_verifcation_code_by_code(code)):
            code = randint(1000000, 9999999)
        else:
            code_not_unique = False
    app_config.db.add_verification_code(code, datetime.datetime.now().strftime('%d-%m-%Y'), user_id)
    return base_email_url + str(code) + '/?email=' + email




def activate_user_account(code, email):
    code_details = app_config.db.get_verifcation_code_by_code(int(code))
    if(code_details):
        user_details = app_config.db.get_user_by_id(code_details['user_id'])
        if(user_details['email'] == email):
            app_config.db.update_user_account_type(user_details['id'], 1)
            return True
    return False
