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
    detalle_curso,
    detalle_curso_estudiante,
    recuperar_clave,  # Asegúrate de importar la vista
    editar_perfil,
    asignar_calificacion,
    calificaciones_estudiante,
    generar_reporte_pdf,
)

urlpatterns = [
    path('', login, name='login'),
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
    path('curso/<int:curso_id>/', detalle_curso, name='detalle_curso'),
    path('detalle-curso/<int:curso_id>/', detalle_curso_estudiante, name='detalle_curso_estudiante'),
    path('recuperar-clave/', recuperar_clave, name='recuperar_clave'),  # Nueva URL para recuperar clave
    path('editar-perfil/', editar_perfil, name='editar_perfil'),
    path('curso/<int:curso_id>/asignar_calificacion/', asignar_calificacion, name='asignar_calificacion'),
    path('calificaciones/', calificaciones_estudiante, name='calificaciones_estudiante'),
    path('generar_reporte_pdf/', generar_reporte_pdf, name='generar_reporte_pdf'),
]