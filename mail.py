import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from logs import logger


class Mail:
    port = 465
    smtp_server_domain_name = 'smtp.gmail.com'
    sender_mail = 'dp217py@gmail.com'
    sender_name = '"Enrollment_assistant"'
    password = os.environ.get('PASS_MAIL')

    def send_mail(self, data):
        logger.info('send_mail started')
        email = data['mail']
        text_template = data['text']
        subject = data['subject']
        time.sleep(1)
        report = ""
        try:
            service = smtplib.SMTP_SSL(self.smtp_server_domain_name, self.port)
            service.login(self.sender_mail, self.password)

            mail = MIMEMultipart('alternative')
            mail['Subject'] = subject
            mail['From'] = self.sender_name
            mail['To'] = email

            text_content = MIMEText(text_template, 'html')

            mail.attach(text_content)

            service.sendmail(self.sender_mail, self.email, mail.as_string())
            report += f"Mail to {self.email} was sent.\n"
            logger.info(report)
            return report

        except smtplib.SMTPException as error:
            logger.error(error)
            return f'{error}\nSend mail error!'

        finally:
            service.quit()
