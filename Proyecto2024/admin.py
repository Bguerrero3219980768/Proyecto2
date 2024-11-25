from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Curso

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'user_type', 'is_staff')
    list_filter = ('user_type',)
    search_fields = ('username', 'email')

admin.site.register(CustomUser, CustomUserAdmin)

# Configuración del panel para Curso
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'profesor', 'descripcion')
    list_filter = ('profesor',)  # Agregar filtro por profesor
    search_fields = ('nombre', 'descripcion')  # Agregar barra de búsqueda

admin.site.register(Curso, CursoAdmin)