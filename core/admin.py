from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(TicketCategory)
admin.site.register(Ticket)
admin.site.register(TicketReport)