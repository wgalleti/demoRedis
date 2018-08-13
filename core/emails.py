from smtplib import SMTPException
from threading import Thread

from django.core.mail import EmailMessage
from django.template.loader import get_template

from config import settings
from core.models import Erro


class Mail(Thread):

    def __init__(self, email_to, name_destination, title, template, context=None):
        self.email_to = email_to
        self.name_destination = name_destination
        self.context = dict(data=context)
        self.title = title
        self.template = template
        Thread.__init__(self)

    def run(self):
        template = get_template(self.template)
        message_html = template.render(self.context)

        email = EmailMessage(self.title, message_html, settings.DEFAULT_FROM_EMAIL, [self.email_to])
        email.content_subtype = 'html'

        try:
            email.send()
        except SMTPException as e:
            Erro(titulo='Erro ao enviar Email', log=str(e)).save()