from django.contrib import admin
from .models import Estudiante, Profesor, Curso, Evaluacion, Calificacion, Administrador

admin.site.register(Estudiante)
admin.site.register(Profesor)
admin.site.register(Curso)
admin.site.register(Evaluacion)
admin.site.register(Calificacion)
admin.site.register(Administrador)