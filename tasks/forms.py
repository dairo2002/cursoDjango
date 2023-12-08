# from django.forms import ModelForm
from django import forms
from .models import Task
# podemos crear un formulario con los campos de la base de datos, del models.py y lo enviamos al fron-end
class taskForm(forms.ModelForm):
    class Meta: 
        model = Task
        fields = ['titulo', 'descripcion', 'importante']
        # Asi podemos estilizar los campos que son de la base de datos que son utilizados en create_task.html
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el titulo de la tarea'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describa la tarea'}),
            'importante': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }