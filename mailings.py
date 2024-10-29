from config    import settings

from email.message          import EmailMessage
from email.headerregistry   import Address
from email.utils            import make_msgid

from utils  import get_content_from_template
from utils  import get_datas_from_template
from utils  import attach_images_to_message

import smtplib

def send(message):

    # Send the email via SMTP server
    with smtplib.SMTP_SSL(settings.host, settings.port) as server:
        server.login(settings.login, settings.password)
        server.send_message(message)


def send_message_from_template(template_name: str, receiver: str, required_constants: dict = {}):
    
    msg = EmailMessage()
    datas = get_datas_from_template(template_name)

    # Add required constants
    if required_constants:
        for key in list(required_constants.keys()):
            datas['constants'][key] = required_constants[key]

    msg['Subject'] = datas['Subject']
    msg['To'] = receiver
    msg['From'] = Address(settings.userlabel, settings.emailname, settings.domain)
    msg.set_content(get_content_from_template(template_name, datas['constants'], type="txt"))
    msg.add_alternative(get_content_from_template(template_name, datas['constants']), subtype="html")
    msg = attach_images_to_message(template_name, msg)

    send(msg)

    print("Mail sent.")
