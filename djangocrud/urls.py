"""
URL configuration for djangocrud project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
# importamos las vistas
from tasks import views

# aca van las rutas de la vista
urlpatterns = [
    path('admin/', admin.site.urls),
    #name ='' el nombre de la ruta
    path('', views.home, name='home'), 
    path('signup/', views.signup, name='signup'),
    path('tasks/', views.tasks, name='tasks'),
    # mostrar todas las tareas completas
    path('tasks_completed/', views.tasks_completed, name='tasks_completed'),
    path('tasks/create/', views.create_task, name='create_task'),
    # creamos una variable en la ruta tasks, con el id que va hacer entero, esto nos permite hacer busqueda por un numero las tareas(Tasks), este id lo pasamos en la vista
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    # marcar una tarea
    path('tasks/<int:task_id>/complete', views.complete_task, name='complete_task'),
    # eliminar una tarea
    path('tasks/<int:task_id>/delete', views.delete_task, name='delete_task'),
    path('logout/', views.cerrarSesion, name='logout'),
    path('signin/', views.signin, name='signin')
]
