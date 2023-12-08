from django.contrib import admin
# traemos el modelo y importamos la clase tarea(Task) que es la tabla de la base de datos
from .models import Task

# traemos el campo created de la tabla DB Task para que tambien sea mostrada la fecha de creacion en el Task
class TaskAdmin(admin.ModelAdmin):
    # no lo podemos modificar porque este es un campo de solo lectura
    readonly_fields = ("creacion", )

# aca añadimos la tablas de la base de datos al panel de administrador
admin.site.register(Task, TaskAdmin)
