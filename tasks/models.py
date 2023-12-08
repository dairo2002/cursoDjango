from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Cremos una clase que una tabla de base de datos
class Task(models.Model):
    titulo = models.CharField(max_length=100)
    # (blank=True) quiere decir que es opcional
    descripcion = models.TextField(blank=True)
    creacion = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    importante = models.BooleanField(default=False)
    # la relacionamos con la clese user, Django por defecto viene con una tablas de user
    # utilizamos la eliminacion CASCADE para que cuando el user(Usuario se eliminado, entonces sus taresa tambien van a ser eliminadas)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo +' - by '+ self.usuario.username
    