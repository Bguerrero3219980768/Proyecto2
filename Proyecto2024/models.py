from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from django.core.mail import send_mail

from Proyecto2 import settings

# Modelo de usuario personalizado
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Estudiante'),
        ('teacher', 'Profesor'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    foto_perfil = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    correo_alternativo = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.username

# Modelo de código de verificación para el registro
class VerificationCode(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    code = models.UUIDField(default=uuid.uuid4, editable=False)
    verified = models.BooleanField(default=False)

    def send_verification_email(self):
        subject = 'Código de verificación de registro'
        message = f'Tu código de verificación es: {self.code}'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [self.user.email]
        send_mail(subject, message, from_email, recipient_list)

# Modelo de Curso
class Curso(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    profesor = models.ForeignKey(CustomUser, limit_choices_to={'user_type': 'teacher'}, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
    
class ContenidoCurso(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    archivo = models.FileField(upload_to='contenidos/', blank=True, null=True)  # Opcional: para archivos adjuntos
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    profesor = models.ForeignKey(settings.AUTH_USER_MODEL, limit_choices_to={'user_type': 'teacher'}, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo

# Modelo de Inscripción de Estudiantes en Cursos
class Inscripcion(models.Model):
    estudiante = models.ForeignKey(CustomUser, limit_choices_to={'user_type': 'student'}, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.estudiante.username} inscrito en {self.curso.nombre}"

# Modelo de Evaluación para los Cursos
class Evaluacion(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha = models.DateField()

    def __str__(self):
        return self.titulo

# Modelo de Calificación de Estudiantes en Evaluaciones
class Calificacion(models.Model):
    estudiante = models.ForeignKey(CustomUser, limit_choices_to={'user_type': 'student'}, on_delete=models.CASCADE)
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE)
    calificacion = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.estudiante.username} - {self.evaluacion.titulo} - {self.calificacion}"
