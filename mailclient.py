import os, sys, re
from smtplib import SMTP_SSL as SMTP

SMTPserver = os.environ['email_server']
sender = os.environ['email_from']
destination = ['quintenstekie@gmail.com']

username = sender
password = os.environ['email_password']

text_subtype = 'html'
