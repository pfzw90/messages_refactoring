import email
import imaplib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Mailer:
    def __init__(self, login: str, password: str, smtp: str, imap: str):
        self.login = login
        self.password = password
        self.SMTP = smtp
        self.IMAP = imap

    def send_message(self, text: str, subj: list, to: str):
        message = MIMEMultipart()
        message['From'] = self.login
        message['To'] = ', '.join(to)
        message['Subject'] = subj
        message.attach(MIMEText(text))

        send_server = smtplib.SMTP(self.SMTP, 587)
        send_server.ehlo()
        send_server.starttls()
        send_server.ehlo()
        send_server.login(self.login, self.password)
        send_server.sendmail(self.login, send_server, message.as_string())

        send_server.quit()

    def receive_messages(self, head):
        receive_server = imaplib.IMAP4_SSL(self.IMAP)
        receive_server.login(self.login, self.password)
        receive_server.list()
        receive_server.select("inbox")

        if head:
            criterion = '(HEADER Subject "%s")' % head
        else:
            criterion = 'ALL'

        result, data = receive_server.uid('search', None, criterion)
        if len(data) == 0:
            res = 'There are no letters with current header'
        else:
            latest_email_uid = data[0].split()[-1]
            result, data = receive_server.uid('fetch', latest_email_uid, '(RFC822)')
            raw_email = data[0][1]
            res = email.message_from_string(raw_email)

        receive_server.logout()
        return res


if __name__ == '__main__':
    mailer = Mailer('login@gmail.com', 'qwerty', 'smtp.gmail.com', 'imap.gmail.com')

    mailer.send_message('Message', ['vasya@email.com', 'petya@email.com'], 'Subject')
    print(mailer.receive_messages(None))
