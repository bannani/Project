# coding=utf-8
import smtplib
import mimetypes
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.mime.image import MIMEImage
from email.Utils import COMMASPACE, formatdate
from email import Encoders


def sendmail(mail) :
    filePath = "IMAGE_1.PNG"#your file name

    From = 'test'
    To = mail

    msg = MIMEMultipart()
    msg['From'] = 'imed.gaidi@technica-engineering.de'
    msg['To'] = To
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = 'Time Clock Process Notice'
    text=""" 

Dar colleagues,\n\n
As you all know, we are all required to clock in at our assigned start time and must clock out when we go off duty. However, in case you forget to do so, you have to send an e-mail informing Hela about that(see template) and you should send it in the afternoon at the latest when you miss to clock in the morning and next day morning if you miss to clock out otherwise it will be deemed as a day off.
Thank you for your cooperation😊\n\n

Rgds,\n

Mariem
"""
    part1= MIMEText(text, 'plain')
    msg.attach(part1)
    
    smtp = smtplib.SMTP('192.168.1.142')
    """try:
        smtp = smtplib.SMTP('smtp.enis.tn:587')
        smtp.starttls()
        smtp.login('', '')
    except:
    i = 1
else:
    i = 0"""

    try:
        smtp.sendmail(From, To,msg.as_string())
    except:
        print "Mail not sent"
    else:
        print ("Mail sent to " + mail)
        smtp.close()

"""if i == 0:
    ctype, encoding = mimetypes.guess_type(filePath)
    if ctype is None or encoding is not None:
        # No guess could be made, or the file is encoded (compressed), so
        # use a generic bag-of-bits type.
        ctype = 'application/octet-stream'
    maintype='text'
    if maintype == 'text':
        fp = open(filePath)
        # Note: we should handle calculating the charset
        part = MIMEText(fp.read(), _subtype=subtype)
        fp.close()
    elif maintype == 'image':
        fp = open(filePath, 'rb')
        part = MIMEImage(fp.read(), _subtype=subtype)
        fp.close()
    elif maintype == 'audio':
        fp = open(filePath, 'rb')
        part = MIMEAudio(fp.read(), _subtype=subtype)
        fp.close()
    else:
        fp = open(filePath, 'rb')
        part = MIMEBase(maintype, subtype)
        part.set_payload(fp.read())
        fp.close()
        # Encode the payload using Base64
        Encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % filePath)
    msg.attach(part)"""

sendmail('akram.rekik@technica-engineering.de')
