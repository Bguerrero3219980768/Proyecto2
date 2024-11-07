from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Curso, ContenidoCurso, CustomUser, Evaluacion

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
        fields = ['titulo', 'fecha']

class ContenidoCursoForm(forms.ModelForm):
    class Meta:
        model = ContenidoCurso
        fields = ['titulo', 'descripcion', 'archivo']

# Formulario de recuperación de clave
class RecuperarClaveForm(forms.Form):
    email = forms.EmailField(label='Correo electrónico', required=True)
