from django import template
from Proyecto2024.models import Calificacion  # Importa el modelo de Calificacion

register = template.Library()

@register.filter
def get_calificacion(evaluacion, estudiante):
    """
    Obtiene la calificación única de un estudiante para una evaluación específica.
    """
    return Calificacion.objects.filter(evaluacion=evaluacion, estudiante=estudiante).first()

