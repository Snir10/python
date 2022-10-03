import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

email = "sniroded@gmail.com" # the email where you sent the email
password = "bfgroocspcnbjqoj"
send_to_email = "sniroded05@gmail.com" # for whom
subject = "TEST RESULTS"
message = "CSV files attached above."


#files to be attached
files = ['/Users/user/Desktop/Backup/products.csv', '/Users/user/Desktop/Backup/products.csv']

msg = MIMEMultipart()
msg["From"] = email
msg["To"] = send_to_email
msg["Subject"] = subject

msg.attach(MIMEText(message, 'plain'))



for path in files:
    part = MIMEBase('application', "octet-stream")
    with open(path, 'rb') as file:
        part.set_payload(file.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition',
                    'attachment; filename={}'.format(Path(path).name))
    msg.attach(part)

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(email, password)
text = msg.as_string()
server.sendmail(email, send_to_email, text)
server.quit()