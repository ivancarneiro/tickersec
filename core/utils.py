import os

from django.db import models
from datetime import datetime


def ticket_capture_upload_to(instance, filename):
    # Obtener la fecha actual
    now = datetime.now()
    # Construir la ruta del archivo
    path = f"ticket_captures/{now.year}/{now.month}/{now.day}/{instance.pk}"
    return os.path.join(path, filename)

class TicketType(models.TextChoices):
    INCIDENTE       = "INC", "Incidente"
    VULNERABILIDAD  = "VUL", "Vulnerabilidad"
    EVENTO          = "EVE", "Evento"

class TicketStatus(models.TextChoices):
    ABIERTO     = "ABIERTO", "Abierto"
    TRAMITADO   =  "TRAMITADO", "Tramitado"
    CERRADO     = "CERRADO", "Cerrado"

class Severity(models.TextChoices):
    CRITICA = "CRITICA"
    ALTA    = "ALTA"
    MEDIA   = "MEDIA"
    BAJA    = "BAJA"
    NULA    = "NULA"

class Impact(models.TextChoices):
    CRITICA     = "CRITICO"
    IMPORTANTE  = "IMPORTANTE"
    MODERADO    = "MODERADO"
    BAJO        = "BAJO"
    NULO        = "NULO"