import re
from django.forms import ValidationError


def solo_letras(value):
    if any(char.isdigit() for char in value):
        raise ValidationError('El nombre solo admite letras. %(valor)s', code='Invalid',       params={'valor': value})


def custom_validate_email(value):
    email_regex = r'^([\w\-\.]+)@((\[([0-9]{1,3}\.){3}[0-9]{1,3}\])|(([\w\-]+\.)+)([a-zA-Z]{2,4}))$'
    if not re.match(email_regex, value):
        raise ValidationError('Correo electrónico inválido')