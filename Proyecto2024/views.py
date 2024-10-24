from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test
from .models import CustomUser, VerificationCode, Curso, Inscripcion, Evaluacion, Calificacion
from .forms import RegistroForm, VerificacionForm, CursoForm, EvaluacionForm

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
            user = form.save()
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
        if form.is_valid() and form.cleaned_data['code'] == str(user.verificationcode.code):
            user.verificationcode.verified = True
            user.verificationcode.save()
            login(request, user)
            return redirect('inicio')
    else:
        form = VerificacionForm()
    return render(request, 'verificar.html', {'form': form})

# 3. Vista para que los administradores creen cursos
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

# 4. Vista para listar los cursos disponibles a los que los estudiantes pueden inscribirse
@user_passes_test(es_estudiante)
def lista_cursos_disponibles(request):
    cursos = Curso.objects.all()
    return render(request, 'lista_cursos.html', {'cursos': cursos})

# 5. Vista para que los estudiantes se inscriban en un curso
@user_passes_test(es_estudiante)
def inscribirse_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    if not Inscripcion.objects.filter(estudiante=request.user, curso=curso).exists():
        Inscripcion.objects.create(estudiante=request.user, curso=curso)
    return redirect('detalle_curso', curso_id=curso.id)

# 6. Vista para que los profesores creen evaluaciones para los cursos a los que están asignados
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

# 7. Vista para que los estudiantes vean sus calificaciones
@user_passes_test(es_estudiante)
def ver_calificaciones(request):
    calificaciones = Calificacion.objects.filter(estudiante=request.user)
    return render(request, 'ver_calificaciones.html', {'calificaciones': calificaciones})

# 8. Vista para ver los detalles de un curso (tanto estudiantes como profesores)
def detalle_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    evaluaciones = Evaluacion.objects.filter(curso=curso)
    context = {
        'curso': curso,
        'evaluaciones': evaluaciones,
    }
    return render(request, 'detalle_curso.html', context)


