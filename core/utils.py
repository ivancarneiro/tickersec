from django.db import models


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
    CRITICO     = "CRITICO"
    IMPORTANTE  = "IMPORTANTE"
    MODERADO    = "MODERADO"
    BAJO        = "BAJO"
    NULO        = "NULO"