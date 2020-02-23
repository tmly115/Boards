'''
User Managment System for Flask, Thomas Young (c) 2020

This Usermanagment system is desinged to be used with any flask web-app.
If a user is successfully logged on to the web app then their email will be
saved in the session object and can be referenced with 'email'.

'''


from flask import Blueprint, render_template, url_for, redirect, request, session
import app_config

import datetime
from .forms import Login_Form, Signup_Form, Change_Username_and_Password_Form
from .se import encrypt_line, generate_key

from .email_verification import verify_email, activate_user_account

user_managment = Blueprint('user_managment', __name__, template_folder = 'templates')



@user_managment.route('/login/', methods = ['GET', 'POST'])
def login():
    if 'email' in session:
        return 'You can\'t log in if you are already logged in!'
    elif request.method == 'POST':
        form = Login_Form(request.form)
        en_username = encrypt_line(generate_key(form.password), form.username)
        user_info = app_config.db.get_user_by_username(en_username)
        if user_info:
            if user_info['account_type'] > 0:
                session['email'] = user_info['email']
                if app_config.db.get_profile_by_user_id(user_info['id']):
                    return redirect(url_for('main_app.home'))
                else:
                    return redirect(url_for('main_app.setup_profile'))
            else:
                return render_template('log_in.html', title = 'Log In', error_description = 'You must activate your account with the link sent to you by email.')
        else:
            return render_template('log_in.html', title = 'Log In', error_description = 'Username or Password are not correct.')
    else:
        return render_template('log_in.html', title = 'Log In')



@user_managment.route('/logout/')
def logout():
    session.pop('email')
    return redirect(url_for('main_app.boards'))



@user_managment.route('/signup/', methods = ['GET', 'POST'])
def signup():
    if 'email' in session:
        return 'You can\'t create an account if you are already logged in!'
    elif request.method == 'POST':
        form = Signup_Form(request.form)
        if(form.error):
            return render_template('sign_up.html', title = 'Sign Up', error_description = form.error_description)
        en_username = encrypt_line(generate_key(form.password), form.username)
        if(app_config.db.get_user_by_email(form.email)):
            return render_template('sign_up.html', title = 'Sign Up', error_description = 'Email is already tied to another account.')
        elif(app_config.db.get_user_by_username(en_username)):
            return render_template('sign_up.html', title = 'Sign Up',
                error_description = 'Password / Username combination has already been used. Please change one and try again.')
        else:
            app_config.db.add_user(en_username, form.full_name,
                form.email, datetime.datetime.now().strftime("%d-%m-%Y"))
            return redirect(url_for('user_managment.verify_email_static', email = form.email))
    return render_template('sign_up.html', title = 'Sign Up')



@user_managment.route('/verify_email/')
def verify_email_static():
    user = app_config.db.get_user_by_email(request.args.get('email'))
    if(user):
        verify_email(user['email'], user['id'])
        return render_template('verify_email.html', title = 'Verify Email', users_email = user['email'])
    else:
        return 'No No, you can\'t do that!'



@user_managment.route('/verify_email/<code>/')
def verify_email_code(code):
    email =  request.args.get('email')
    if(email):
        if(activate_user_account(code, email)):
            return render_template('email_verified.html', title = 'Email Verified')
        else:
            return 'The link used was invalid :('
    else:
        return 'What do you think your doing!'



@user_managment.route('/change_username_and_password/', methods = ['GET', 'POST'])
def change_username_and_password():
    if 'email' in session:
        user = app_config.db.get_user_by_email(session['email'])
        if user:
            if request.method == 'POST':
                form = Change_Username_and_Password_Form(request.form)
                if form.error:
                    return render_template('change_username_and_password.html', title = 'Change Username and Password',
                        user = user, error_description = form.error_description)
                en_username = encrypt_line(generate_key(form.password), form.username)
                if app_config.db.get_user_by_username(en_username):
                    return render_template('change_username_and_password.html', title = 'Change Username and Password',
                        user = user, error_description = 'Username and Password combination has already been used.')
                else:
                    app_config.db.update_username(en_username, user['id'])
                    return redirect(url_for('main_app.home'))
            else:
                return render_template('change_username_and_password.html', title = 'Change Username and Password', user = user)
    return 'Must be logged in to do that!'
