from django.core.exceptions import ValidationError

def validar_par(value):
    if value % 2 != 0:
        raise ValidationError("El valor debe ser par")

def validar_subject(value):
    if value == "prueba":
        raise ValidationError("El subject no debe ser prueba")
