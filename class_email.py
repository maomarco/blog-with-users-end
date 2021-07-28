import smtplib
import ssl

class Class_email():

    def __init__(self):
        self.my_email = "maomarco8@gmail.com"
        self.password = 'zjbiqizcgfajresy'

    def send_email(self, msg, to, subj):
        port = 465
        context = ssl.create_default_context()

        message = f'subject: {subj}\n\n {msg}'

        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(self.my_email, self.password)
            server.sendmail(from_addr=self.my_email, to_addrs=to, msg=message)