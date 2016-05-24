#!/usr/bin/env python

import smtplib
from email.header import Header
from email.utils import formataddr



TO = 'bikeshkawang@gmail.com'
SUBJECT = 'TEST MAIL'
TEXT = 'This is email test from python'



# Gmail Sign In
gmail_sender = 'sendermail@gmail.com'
gmail_passwd = 'senderpassword'

author = formataddr((str(Header(u'your name', 'utf-8')), "sendermail@gmail.com"))




server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
server.login(gmail_sender, gmail_passwd)
BODY = '\r\n'.join(['To: %s' % TO,
                    'From: %s' % author,
                    'Subject: %s' % SUBJECT,
                    '', TEXT])

try:
    server.sendmail(gmail_sender, [TO], BODY)
    print ('email sent')
except:
    print ('error sending mail')

server.quit()