#Objects that act as data-structures and validate data inputed from forms

class Login_Form:
    def __init__(self, login_form_dict):
        self.username = login_form_dict['username']
        self.password = login_form_dict['password']



class Signup_Form:
    def __init__(self, signup_form_dict):
        if(self._validate(signup_form_dict)):
            self.username = signup_form_dict['username']
            self.full_name = signup_form_dict['full_name']
            self.email =  signup_form_dict['email']
            self.password = signup_form_dict['password']
            self.error = False

    def _validate(self, signup_form_dict):
        if(signup_form_dict['email'] != signup_form_dict['retyped_email']) or (signup_form_dict['password'] != signup_form_dict['retyped_password']):
            self.error = True
            self.error_description = 'Email and / or passwords do not match.'
            return False
        elif(len(signup_form_dict['password']) < 6):
            self.error = True
            self.error_description = 'Password needs to be 6 charecters or more.'
        elif('@' and '.' not in signup_form_dict['email']):
            self.error = True
            self.error_description = 'Email enterd is not valid.'
            return False
        else:
            return True

class Change_Username_and_Password_Form:
    def __init__(self, change_username_password_form_dict):
        if self._validate(change_username_password_form_dict):
            self.username = change_username_password_form_dict['username']
            self.password = change_username_password_form_dict['password']
            self.error = False

    def _validate(self, change_username_password_form_dict):
        if change_username_password_form_dict['password'] != change_username_password_form_dict['retyped_password']:
            self.error = True
            self.error_description = 'Passwords do not match.'
            return False
        elif len(change_username_password_form_dict['password']) < 6:
            self.error = True
            self.error_description = 'Password needs to be 6 charecters or more.'
            return False
        else:
            return True
