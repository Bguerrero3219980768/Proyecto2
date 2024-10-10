from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=255)
    tipoUsuario = models.CharField(max_length=50)

    def iniciarSesion(self, email, contrasena):
        # Lógica de inicio de sesión
        pass

    def cerrarSesion(self):
        # Lógica de cierre de sesión
        pass

    class Meta:
        abstract = True
        
class Estudiante(Usuario):
    matricula = models.CharField(max_length=50, unique=True)

    def verCalificaciones(self):
        # Lógica para ver las calificaciones
        pass

    def inscribirseCurso(self, curso):
        # Lógica para inscribirse a un curso
        pass
class Profesor(Usuario):
    idProfesor = models.CharField(max_length=50, unique=True)
    
    def calificarEstudiante(self, estudiante, calificacion):
        # Lógica para calificar estudiante
        pass

    def crearEvaluacion(self, evaluacion):
        # Lógica para crear una evaluación
        pass
class Curso(models.Model):
    idCurso = models.CharField(max_length=50, unique=True)
    nombreCurso = models.CharField(max_length=255)
    descripcion = models.TextField()
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)
    estudiantes = models.ManyToManyField(Estudiante, related_name='cursos')

    def asignarEstudiante(self, estudiante):
        # Lógica para asignar estudiante
        pass

    def removerEstudiante(self, estudiante):
        # Lógica para remover estudiante
        pass

class Evaluacion(models.Model):
    idEvaluacion = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=255)
    fecha = models.DateField()
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    calificaciones = models.ManyToManyField('Calificacion', related_name='evaluaciones')

    def crearEvaluacion(self):
        # Lógica para crear evaluación
        pass

    def modificarEvaluacion(self):
        # Lógica para modificar evaluación
        pass
class Calificacion(models.Model):
    idCalificacion = models.CharField(max_length=50, unique=True)
    valor = models.FloatField()
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)

    def asignarCalificacion(self):
        # Lógica para asignar calificación
        pass
class Administrador(Usuario):
    idAdministrador = models.CharField(max_length=50, unique=True)

    def gestionarUsuarios(self):
        # Lógica para gestionar usuarios
        pass

    def gestionarCursos(self):
        # Lógica para gestionar cursos
        pass
