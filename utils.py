from templates import __TEMPLATES_FOLDER__

from email.message      import EmailMessage
from email.mime.image   import MIMEImage

from jinja2 import Environment
from jinja2 import FileSystemLoader

import json
import os


def get_content_from_template(template_name: str, template_keywords: dict, type: str = "html"):
    """Returns a content rendered from a template with given keywords.

    :param template_name: Name of the mail template.
    :type template_name: str
    :param template_keywords: Keywords to replace.
    :type template_keywords: dict
    :param type: Which content file to work with, 'html' or 'txt', defaults to "html"
    :type type: str, optional
    :raises NotADirectoryError: Raises an error if the template does not exist
    :return: The content with replaced values
    :rtype: str
    """

    template_path = os.path.join(__TEMPLATES_FOLDER__, template_name)
    if not os.path.isdir(template_path):
        raise NotADirectoryError("Requested template does not exist.")

    environment = Environment(loader=FileSystemLoader(template_path))
    template = environment.get_template("content.%s"%type)

    return template.render(**template_keywords)


def get_datas_from_template(template_name: str):
    """Returns the datas associated with a mail template

    :param template_name: The name of the mail template
    :type template_name: str
    :raises NotADirectoryError: Raises an error if the template does not exist
    :return: A dict containing the datas
    :rtype: dict
    """

    template_path = os.path.join(__TEMPLATES_FOLDER__, template_name)
    if not os.path.isdir(template_path):
        raise NotADirectoryError("Requested template does not exist.")
    
    with open(os.path.join(template_path, "datas.json")) as json_file:
        datas = json.load(json_file)

    return datas


def attach_images_to_message(template_name: str, message: EmailMessage):
    """Attach images of the template to the message object

    :param template_name: Name of the mail template
    :type template_name: str
    :param message: The message object to send
    :type message: EmailMessage
    :raises NotADirectoryError: Raises an error if template does not exist
    :raises NotADirectoryError: Raises an error if template does not have images
    :return: The message with all its attachments
    :rtype: EmailMessage
    """

    template_path = os.path.join(__TEMPLATES_FOLDER__, template_name)
    if not os.path.isdir(template_path):
        raise NotADirectoryError("Requested template does not exist.")

    images_path = os.path.join(template_path, "images")
    if not os.path.isdir(images_path):
        raise NotADirectoryError("Requested template does not have images.")

    # Get all template images
    images = os.listdir(images_path)

    # Attach each image to the given message object
    for image in images:
        with open(os.path.join(images_path, image), "rb") as img:
            message.get_payload()[1].add_related(img.read(), 'image', 'png', cid='<%s>'%(os.path.splitext(image)[0]))

        #     img_to_attach = MIMEImage(img.read())
        # img_to_attach.add_header('Content-ID', '<%s>'%(os.path.splitext(image)[0]))

        # message.attach(img_to_attach)

    return message

