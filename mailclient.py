import os, sys, re
from smtplib import SMTP_SSL as SMTP
from email.mime.text import MIMEText

SMTPserver = os.environ['email_server']
sender = os.environ['email_username']
destination = []
username = sender
password = os.environ['email_password']
text_subtype = 'html'
content = ''
subject = 'Voltooi jouw boeking!'


def set_body(journey, gotoUrl):
    global content
    content = '<a href =\'https://www.nsinternational.nl/\'>' \
              '<img src=\'http://www.natm.nl/web/wp-content/uploads/2015/04/logo_nsinternational.jpg\' alt=\'NsInternational\' title=\'NsInternational\' style=\'display:block\' height=\'100px\' width=\'272px\'>' \
              '</a><br>' \
              'Beste Reiziger,<br>' \
              '<br>' \
              'Voltooi jouw boeking door op <a href =\'' + gotoUrl + \
              '\'>deze</a> link te klikken. Fijne reis!<br>' \
              '<br>' \
              '<h3>Samenvatting van de reis</h3>' \
              '<div style=\'border-left:6px solid;border-color:#2196F3;color:#000;background-color:#ddffff;padding-left:16px\'>Vetrek om: ' \
              + journey['origin']['departure']['planned'].split()[1] + '  <br>' \
              'Vertrek van: ' + journey['origin']['name'] + '</div>' \
              '<br>' \
              '<div style=\'border-left:6px solid;border-color:#0000FF;color:#000;background-color:#eedddd;padding-left:16px\'>Aankomst om: ' \
              + journey['destination']['arrival']['planned'].split()[1] + '<br>' \
              'Aankomst op: ' + journey['destination']['name'] + '</div>' \
              '<br>' \
              '<b>Totale prijs: ' + journey['offers'][0]['salesPrice']['amount'] + ' </b>' \
              '<br><br>' \
              'Met vriendelijke groet,<br><br> Quinten \'Eindbaas\' Stekelenburg<br>'


def set_destination(email):
    global destination
    destination.append(email)


def send_mail():
    global content, destination
    try:
        msg = MIMEText(content, text_subtype)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = destination[0]
        print(msg)
        conn = SMTP(SMTPserver)
        conn.set_debuglevel(True)
        conn.login(username, password)
        try:
            conn.sendmail(sender, destination, msg.as_string())
        finally:
            conn.quit()
            destination = []
            return True
    except Exception:
        print(sys.exc_info()[0])
        return False
