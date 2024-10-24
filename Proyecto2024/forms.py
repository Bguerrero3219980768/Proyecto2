# forms.py
from django import forms
from .models import Estudiante, Profesor

class RegistroEstudianteForm(forms.ModelForm):
    contrasena = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Estudiante
        fields = ['nombre', 'email', 'contrasena', 'matricula']

    def save(self, commit=True):
        estudiante = super().save(commit=False)
        estudiante.set_password(self.cleaned_data['contrasena'])  # Encripta la contraseña
        if commit:
            estudiante.save()
        return estudiante

class RegistroProfesorForm(forms.ModelForm):
    contrasena = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Profesor
        fields = ['nombre', 'email', 'contrasena', 'idProfesor']

    def save(self, commit=True):
        profesor = super().save(commit=False)
        profesor.set_password(self.cleaned_data['contrasena'])  # Encripta la contraseña
        if commit:
            profesor.save()
        return profesor

