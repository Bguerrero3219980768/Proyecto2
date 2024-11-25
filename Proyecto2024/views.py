import string
import random
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, get_user_model, logout as auth_logout
from django.contrib.auth.decorators import user_passes_test, login_required
from django.conf import settings
from django.core.mail import send_mail
from .models import CustomUser, VerificationCode, Curso, Inscripcion, Evaluacion, Calificacion
from .forms import RegistroForm, VerificacionForm, CursoForm, EvaluacionForm, RecuperarClaveForm  # Asegúrate de importar tu nuevo formulario

# Función para verificar si el usuario es administrador
def es_administrador(user):
    return user.user_type == 'admin'

# Función para verificar si el usuario es profesor
def es_profesor(user):
    return user.user_type == 'teacher'

# Función para verificar si el usuario es estudiante
def es_estudiante(user):
    return user.user_type == 'student'

# 1. Vista para registrar usuarios
def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Desactiva la cuenta hasta la verificación
            user.save()

            # Crear código de verificación y enviar email
            codigo_verificacion = VerificationCode.objects.create(user=user)
            codigo_verificacion.send_verification_email()

            return redirect('verificar_cuenta', user_id=user.id)
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})

# 2. Vista para verificar la cuenta mediante código de verificación
def verificar_cuenta(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    if request.method == 'POST':
        form = VerificacionForm(request.POST)
        if form.is_valid():
            codigo_ingresado = form.cleaned_data['codigo_verificacion']
            try:
                # Buscar el código de verificación
                codigo_obj = VerificationCode.objects.get(user=user, code=codigo_ingresado)
                if not codigo_obj.verified:
                    user.is_active = True  # Activa la cuenta del usuario
                    user.save()
                    codigo_obj.verified = True  # Marca el código como usado
                    codigo_obj.save()
                    return redirect('login')
                else:
                    form.add_error(None, 'El código ya ha sido usado.')
            except VerificationCode.DoesNotExist:
                form.add_error('codigo_verificacion', 'Código incorrecto')
    else:
        form = VerificacionForm()
    return render(request, 'verificar.html', {'form': form})

# 3. Vista de login con opciones para estudiante y profesor
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            if user.user_type == 'student':
                return redirect('home_estudiante')  # Redirigir a la página del estudiante
            elif user.user_type == 'teacher':
                return redirect('home_profesor')  # Redirigir a la página del profesor
            else:
                return redirect('home')  # Redirigir a la página principal para otros tipos
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
    return render(request, 'login.html')
@login_required
def logout(request):
    auth_logout(request)
    return redirect('login')  # Redirige al login después de cerrar sesión

@login_required
def home_estudiante(request):
    # Obtener las inscripciones del estudiante
    inscripciones = Inscripcion.objects.filter(estudiante=request.user)
    
    return render(request, 'home_estudiante.html', {'user': request.user, 'inscripciones': inscripciones})

@login_required
def home_profesor(request):
     # Filtrar los cursos asignados al profesor actual
    cursos = Curso.objects.filter(profesor=request.user)
    return render(request, 'home_profesor.html', {'cursos': cursos})

# 4. Vista para que los administradores creen cursos1
@user_passes_test(es_administrador)
def crear_curso(request):
    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_cursos')
    else:
        form = CursoForm()
    return render(request, 'crear_curso.html', {'form': form})

# 5. Vista para listar los cursos disponibles a los que los estudiantes pueden inscribirse
@user_passes_test(es_estudiante)
def lista_cursos_disponibles(request):
    cursos = Curso.objects.all()
    return render(request, 'lista_cursos.html', {'cursos': cursos})

# 6. Vista para que los estudiantes se inscriban en un curso
@user_passes_test(es_estudiante)
def inscribirse_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    if not Inscripcion.objects.filter(estudiante=request.user, curso=curso).exists():
        Inscripcion.objects.create(estudiante=request.user, curso=curso)
    return redirect('detalle_curso_estudiante', curso_id=curso.id)

# 7. Vista para que los profesores creen evaluaciones para los cursos a los que están asignados
@user_passes_test(es_profesor)
def crear_evaluacion(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    if curso.profesor != request.user:
        return redirect('error_permiso')  # Si el profesor no está asignado al curso

    if request.method == 'POST':
        form = EvaluacionForm(request.POST)
        if form.is_valid():
            evaluacion = form.save(commit=False)
            evaluacion.curso = curso
            evaluacion.save()
            return redirect('detalle_curso', curso_id=curso.id)
    else:
        form = EvaluacionForm()
    return render(request, 'crear_evaluacion.html', {'form': form, 'curso': curso})

# 8. Vista para que los estudiantes vean sus calificaciones
@user_passes_test(es_estudiante)
def ver_calificaciones(request):
    calificaciones = Calificacion.objects.filter(estudiante=request.user)
    return render(request, 'ver_calificaciones.html', {'calificaciones': calificaciones})

# 9. Vista para ver los detalles de un curso (tanto estudiantes como profesores)
def detalle_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    evaluaciones = Evaluacion.objects.filter(curso=curso)
    context = {
        'curso': curso,
        'evaluaciones': evaluaciones,
    }
    return render(request, 'detalle_curso.html', context)

@login_required
def detalle_curso_estudiante(request, curso_id):
    # Verificar que el curso pertenece al estudiante
    curso = get_object_or_404(Curso, id=curso_id)
    inscripcion = Inscripcion.objects.filter(estudiante=request.user, curso=curso).exists()

    if not inscripcion:
        return redirect('home_estudiante')  # Redirige si no está inscrito en el curso

    return render(request, 'detalle_curso_estudiante.html', {'curso': curso})

User = get_user_model()

# 10. Vista para recuperar la clave
def recuperar_clave(request):
    if request.method == 'POST':
        form = RecuperarClaveForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                usuario = User.objects.get(email=email)
                password_temporal = generar_password_temporal()
                
                # Establecer la contraseña temporal
                usuario.set_password(password_temporal)
                usuario.save()

                # Enviar el correo con la contraseña temporal
                subject = 'Recuperación de Contraseña'
                message = f'Tu nueva contraseña temporal es: {password_temporal}. Te recomendamos cambiarla después de iniciar sesión.'
                from_email = settings.DEFAULT_FROM_EMAIL
                send_mail(subject, message, from_email, [email])

                messages.success(request, 'Se ha enviado una contraseña temporal a tu correo electrónico.')
            except User.DoesNotExist:
                form.add_error('email', 'No existe una cuenta asociada a este correo.')
    else:
        form = RecuperarClaveForm()
    return render(request, 'recuperar_clave.html', {'form': form})

def generar_password_temporal():
    caracteres = string.ascii_letters + string.digits
    password = ''.join(random.choice(caracteres) for _ in range(10))  # Genera una contraseña de 10 caracteres
    return password
