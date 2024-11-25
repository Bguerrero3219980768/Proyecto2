from django.urls import path
from .views import (
    login,
    logout,
    registro_usuario,
    verificar_cuenta,
    home_estudiante,
    home_profesor,
    crear_curso,
    lista_cursos_disponibles,
    inscribirse_curso,
    crear_evaluacion,
    ver_calificaciones,
    detalle_curso,
    detalle_curso_estudiante,
    recuperar_clave,  # Asegúrate de importar la vista
)

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name="logout"),
    path('recuperar-clave/', recuperar_clave, name='recuperar_clave'),
    path('registro/', registro_usuario, name='registro_usuario'),
    path('verificar/<int:user_id>/', verificar_cuenta, name='verificar_cuenta'),
    path('home/estudiante/', home_estudiante, name='home_estudiante'),  # URL para estudiante
    path('home/profesor/', home_profesor, name='home_profesor'),      # URL para profesor
    path('crear-curso/', crear_curso, name='crear_curso'),
    path('cursos/', lista_cursos_disponibles, name='lista_cursos'),
    path('inscribirse/<int:curso_id>/', inscribirse_curso, name='inscribirse_curso'),
    path('crear-evaluacion/<int:curso_id>/', crear_evaluacion, name='crear_evaluacion'),
    path('calificaciones/', ver_calificaciones, name='ver_calificaciones'),
    path('curso/<int:curso_id>/', detalle_curso, name='detalle_curso'),
    path('detalle-curso/<int:curso_id>/', detalle_curso_estudiante, name='detalle_curso_estudiante'),
    path('recuperar-clave/', recuperar_clave, name='recuperar_clave'),  # Nueva URL para recuperar clave
]
