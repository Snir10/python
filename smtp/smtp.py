import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

email = "sniroded@gmail.com" # the email where you sent the email
password = "bfgroocspcnbjqoj"
send_to_email = "sniroded05@gmail.com" # for whom
subject = "Gmail"
message = "This is a test email sent by Python. Isn't that cool?!"

msg = MIMEMultipart()
msg["From"] = email
msg["To"] = send_to_email
msg["Subject"] = subject

msg.attach(MIMEText(message, 'plain'))

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(email, password)
text = msg.as_string()
server.sendmail(email, send_to_email, text)
server.quit()