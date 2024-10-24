# views.py
from django.shortcuts import render, redirect
from .forms import RegistroEstudianteForm, RegistroProfesorForm

def registro_usuario(request):
    if request.method == 'POST':
        tipo_usuario = request.POST.get('tipoUsuario')  # Captura el tipo de usuario del formulario
        
        if tipo_usuario == 'Estudiante':
            form = RegistroEstudianteForm(request.POST)
        elif tipo_usuario == 'Profesor':
            form = RegistroProfesorForm(request.POST)
        else:
            form = None  # No se seleccionó ningún tipo de usuario
        
        if form and form.is_valid():
            form.save()  # Guarda el usuario correspondiente
            return redirect('home')  # Redirige a la página de inicio o a donde quieras después del registro
    else:
        form = None
    
    return render(request, 'registro.html', {'form': form})
