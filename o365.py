''' script to send a E-Mail via Microsoft Graph API'''

from O365 import Account
from decouple import config


class _mail():
    def authenticate(self):
        ''' authentication with GRAPH API '''
        client_id = config('CLIENTID')
        client_secret = config('CLIENTSECRET')
        tenant_id = config('TENANTID')

        credentials = (client_id, client_secret)
        try:
            self.account = Account(credentials,
                                   auth_flow_type='credentials',
                                   tenant_id=tenant_id)
            if self.account.authenticate():
                print('Authenticated!')
        except Exception as e:
            print(e)

    def send_mail(self, header: dict, body: str):
        ''' send mail header has to be dict
        mandatory keys: to, subject
        optional keys: cc, file
        body: str'''
        try:
            sender = header['from']
            to = header['to']
            subject = header['subject']
            mailbox = self.account.mailbox(sender)
            message = mailbox.new_message()
            message.to.add(to)
            if header['cc']:
                message.cc.add(header['cc'])
            message.subject = subject
            message.body = body
            if header['file']:
                message.attachments.add(header['file'])
        except Exception as e:
            print(e)
        try:
            # send message
            message.send()
        except Exception as e:
            print(e)
