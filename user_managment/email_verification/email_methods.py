#This file will need editing to insert custom branding etc.

import smtplib

mail_email = 'chat.boards.online@gmail.com'
mail_password = 'msdghxvcjgvdpwle'

def send_validation_email(email, url):
    server = smtplib.SMTP('smtp.gmail.com', 587)

    email_content = f'''From: Chat Boards <{mail_email}>
Content-type: text/html
Subject: Activate your Chat Boards Account

<p>Hello,</p>
<p>
This email has been used to verify an account made with us.
If you did not make an account with Chat Boards then please ignore
this email, as clicking the link could compromise your data.
Otherwise, please click the below link to activate your account.
</p>

<a href = "{url}">{url}</a>

<p>
Thank you for creating an account with Chat Boards, we hope that you like
our site and it allows you to connect with friends, family and like minded
people from around the globe.
</p>

<p><i>The Chat Boards Dev Team</i></p>
'''

    server.starttls()
    server.login(mail_email, mail_password)

    server.sendmail(mail_email, email, email_content)
