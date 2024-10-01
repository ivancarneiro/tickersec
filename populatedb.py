import os
from time import sleep
from unicodedata import category

from flask.cli import F
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tickersec.settings')

import django, random

django.setup()

from django.contrib.auth.models import User
from datetime import datetime
from core.utils import TicketType, TicketStatus, Severity, Impact
from core.models import TicketCategory, Ticket, TicketReport


# testUser = User.objects.create(username='testUser', password='testPassword4321')

def es_bisiesto(year):
    '''Devuelve True si el año es bisiesto, de lo contrario False.'''
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

def random_date():
    '''Genera una fecha aleatoria en el año actual sin segundos.'''
    current_year = datetime.now().year
    month31 = [1, 3, 5, 7, 8, 10, 12]
    month30 = [4, 6, 9, 11]
    
    month = random.randint(1, 12)
    
    if month in month31:
        day = random.randint(1, 31)
    elif month in month30:
        day = random.randint(1, 30)
    else:  # Caso de febrero
        if es_bisiesto(current_year):
            day = random.randint(1, 29)
        else:
            day = random.randint(1, 28)
    
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    
    random_date = datetime(current_year, month, day, hour, minute)
    return random_date.replace(second=0, microsecond=0)


def create_ticket(type,category,date,severity,impact):
    '''Método para poblar la tabla tickets, creando un ticket con datos aleatorios en tipo, categoría, fecha (año actual), severidad, impacto.'''
    
    Ticket.objects.create(
        type = type,
        category = category,
        title = f'Prueba {category.name} - {category.subcategory}',
        createdAt = date,
        severity = severity,
        impact = impact,
        status = TicketStatus.ABIERTO,
        createdBy = User.objects.get(username='testUser'),
        assignedTo = User.objects.get(username='ivan'),
        resume = f'Ticket de prueba para poblar db...')

# print(random.choices(list(TicketType)))
# print(len(categorias))
# categorias = list(TicketCategory.objects.all())
# print(TicketCategory.objects.get(id=random.randint(1, len(categorias)+1)))
# print(Ticket.objects.all().last().pk+1)

for _ in range(100):
    type= random.choice(list(TicketType))
    category = random.choice(list(TicketCategory.objects.all()))
    date = random_date()
    severity = random.choice(list(Severity))
    impact = random.choice(list(Impact))
    create_ticket(type,category,date,severity,impact)
    sleep(1)


if __name__ == '__main__':
    print('Poblando Database Tabla core_ticket...')

    # Imprimir los últimos 3 tickets creados
    # ultimos_tickets = Ticket.objects.all().order_by('-id')[:3]
    # for ticket in ultimos_tickets:
    #     print(ticket)