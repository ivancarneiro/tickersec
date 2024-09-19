import os

from django.db import models
from datetime import datetime


class TicketType(models.TextChoices):
    INCIDENTE       = "INC", "Incidente"
    VULNERABILIDAD  = "VUL", "Vulnerabilidad"
    EVENTO          = "EVE", "Evento"

class TicketStatus(models.TextChoices):
    ABIERTO     = "ABIERTO", "Abierto"
    TRAMITADO   =  "TRAMITADO", "Tramitado"
    CERRADO     = "CERRADO", "Cerrado"

class Severity(models.TextChoices):
    CRITICA = "CRITICO"
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