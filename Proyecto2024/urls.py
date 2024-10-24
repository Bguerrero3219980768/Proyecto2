# urls.py
from django.urls import path
from .views import (
    registro_usuario,
    verificar_cuenta,
    crear_curso,
    lista_cursos_disponibles,
    inscribirse_curso,
    crear_evaluacion,
    ver_calificaciones,
    detalle_curso,
)

urlpatterns = [
    path('registro/', registro_usuario, name='registro_usuario'),
    path('verificar/<int:user_id>/', verificar_cuenta, name='verificar_cuenta'),
    path('crear-curso/', crear_curso, name='crear_curso'),
    path('cursos/', lista_cursos_disponibles, name='lista_cursos'),
    path('cursos/inscribirse/<int:curso_id>/', inscribirse_curso, name='inscribirse_curso'),
    path('cursos/<int:curso_id>/crear-evaluacion/', crear_evaluacion, name='crear_evaluacion'),
    path('calificaciones/', ver_calificaciones, name='ver_calificaciones'),
    path('cursos/<int:curso_id>/', detalle_curso, name='detalle_curso'),
]
