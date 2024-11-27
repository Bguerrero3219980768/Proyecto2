from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Curso, ContenidoCurso, CustomUser, Evaluacion, Calificacion, Inscripcion

class RegistroForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'user_type', 'password1', 'password2')

    # Opcional: validación personalizada si es necesario
    def clean_user_type(self):
        user_type = self.cleaned_data.get('user_type')
        if not user_type:
            raise forms.ValidationError('Debe seleccionar un tipo de usuario.')
        return user_type

# Formulario de verificación de cuenta
class VerificacionForm(forms.Form):
    codigo_verificacion = forms.UUIDField(label='Código de verificación')

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['nombre', 'descripcion', 'profesor']

# Formulario de creación de evaluación
class EvaluacionForm(forms.ModelForm):
    class Meta:
        model = Evaluacion
        fields = ['titulo', 'descripcion', 'fecha']
        
class CalificacionForm(forms.ModelForm):
    class Meta:
        model = Calificacion
        fields = ['estudiante', 'evaluacion', 'calificacion']
        widgets = {
            'calificacion': forms.NumberInput(attrs={'min': 0, 'max': 5, 'step': 0.1}),
        }

    def __init__(self, *args, **kwargs):
        profesor = kwargs.pop('profesor')
        super().__init__(*args, **kwargs)
        # Filtrar las evaluaciones para que sean solo del profesor autenticado
        self.fields['evaluacion'].queryset = Evaluacion.objects.filter(curso__profesor=profesor)

        # Filtrar los estudiantes inscritos en el curso relacionado con la evaluación seleccionada
        self.fields['estudiante'].queryset = CustomUser.objects.filter(
            id__in=Inscripcion.objects.filter(curso__profesor=profesor).values('estudiante')
        )
        
    def clean_calificacion(self):
        calificacion = self.cleaned_data.get('calificacion')
        if calificacion < 0 or calificacion > 5:
            raise ValidationError('La calificación debe estar entre 0 y 5.')
        return calificacion

class ContenidoCursoForm(forms.ModelForm):
    class Meta:
        model = ContenidoCurso
        fields = ['titulo', 'descripcion', 'archivo']

# Formulario de recuperación de clave
class RecuperarClaveForm(forms.Form):
    email = forms.EmailField(label='Correo electrónico', required=True)
    
class EditarPerfilForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['foto_perfil', 'telefono', 'correo_alternativo', 'email']
        widgets = {
            'email': forms.EmailInput(attrs={'readonly': 'readonly'}),
        }
