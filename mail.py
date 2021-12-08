import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os


class Mail:
    port = 465
    smtp_server_domain_name = 'smtp.gmail.com'
    sender_mail = 'dp217py@gmail.com'
    password = os.environ.get('PASS_MAIL')

    def __init__(self, data):
        self.email = data['mail']
        self.text_template = data['text']
        self.subject = data['subject']

    def send_mail(self):
        report = ""
        try:
            service = smtplib.SMTP_SSL(self.smtp_server_domain_name, self.port)
            service.login(self.sender_mail, self.password)

            mail = MIMEMultipart('alternative')
            mail['Subject'] = self.subject
            mail['From'] = self.sender_mail
            mail['To'] = self.email

            text_content = MIMEText(self.text_template, 'html')

            mail.attach(text_content)

            service.sendmail(self.sender_mail, self.email, mail.as_string())
            report += f"Mail to {self.email} was sent.\n"
            return report

        except smtplib.SMTPException as error:
            return f'{error}\nSend mail error!'

        finally:
            service.quit()
