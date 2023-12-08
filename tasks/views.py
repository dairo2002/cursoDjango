from django.shortcuts import render, redirect, get_object_or_404
# importamos la clase UserCreationForm nos permite crear un usuario con un formulario
# importamos la clase AuthenticationForm nos sirve para conmporbar si el usuario exite
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# importamos la clase de usuario de Django
from django.contrib.auth.models import User
# importamos la clase login que nos trae las cookies 
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.db import IntegrityError
# importamos taskForm de la forms
from .forms import taskForm
from .models import Task
from django.utils import timezone
# login_required para proteger las rutas
from django.contrib.auth.decorators import login_required



# vistas
def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm    
        })
    else: 
        # se validan que las dos contraseñas concidan contraseña y confirmar contraseña
        if request.POST['password1'] == request.POST['password2']:
            try:
                # registrar usuario
                usuario = User.objects.create_user(username=request.POST['username'],
                password=request.POST['password1'])
                # save() guarda el usuario dentro de la base de datos
                usuario.save()
                login(request, usuario)
                # si el usuario es creado con exito, me lo redirije a la vista tasks 
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    "error": 'Usuario ya existe'      
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            "error": 'las contraseñas no conciden'      
         })

@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
        # traemos el formulario
            'form': taskForm
        })
    else:
        try:
            # new_task.usuario = request.user: Esta línea establece el campo usuario del objeto new_task. El campo usuario parece ser una clave foránea en tu modelo de Django (probablemente definido en models.py). Se establece con el usuario actualmente autenticado (request.user), vinculando la tarea al usuario que la creó.
            # new_task.save(): Esta línea guarda el objeto new_task en la base de datos. Ahora que commit está establecido en False, los cambios realizados después de llamar a form.save() se aplican al llamar a new_task.save().
            # return redirect('tasks'): Si todo es exitoso, la vista redirige al usuario a una página llamada 'tasks'.
            form = taskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.usuario = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:    
            return render(request, 'create_task.html', {        
                'form': taskForm,
                'error': 'Por favor, ingrese informacion valida'
            })

# pasamos el id, que esta en las urls.py
@login_required
def task_detail(request, task_id):
    # actualizar la tarea
    if request.method == 'GET':
        # con este task_id podemos consultar en la base de datos en la tabla Task, si no se encuenta nos arroja un error 404
        # validamos que nos traiga solo traiga las tareas del usuario esta registrado,  usuario=request.user
        task = get_object_or_404(Task, pk=task_id, usuario=request.user)
        # lo pasamos a la vista
        form = taskForm(instance=task)
        return render(request, 'task_detail.html', 
            {'task':task,
             'form': form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, usuario=request.user)
            form = taskForm(request.POST, instance=task)
            # guarda la actualizacion
            form.save()
            # nos redirije a la pagina de tareas(tasks)
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', 
            {'task':task,
            'form': form,
            'error': 'Error al actualizar la tarea'})

# una tarea(Tasks) completada
@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, usuario=request.user)
    if request.method == 'POST':
        # si la tarea es completa la actualizamos(timezone.now()) y la guardamos(save()) y lo redireciona la pagina de tareas        
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

# eliminar una tarea
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, usuario=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

@login_required
def tasks(request):
    # hacemos una consulta a la base de datos
    # filter(usuario=request.user) nos va atraer las tareas del usuario que esta activo y no de todos los usuario
    # usuario viene del modelo.py de la tabla Task 
    # datecompleted__isnull=True nos muestra las tareas que no estan completadas 
    tasks = Task.objects.filter(usuario=request.user, datecompleted__isnull=True)
    # se la pasamos la variable tasks al fronend de la vista tasks.html
    return render(request, 'tasks.html', {'tasks': tasks})

# nos va a mostrar las tareas completada
@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(usuario=request.user, datecompleted__isnull=False).order_by('-datecompleted')    
    return render(request, 'tasks.html', {'tasks': tasks})

# Esta vista nos cierra sesion y nos redirije a la vista 'home'
@login_required
def cerrarSesion(request):
    logout(request)
    return redirect('home')

# Esta vista nos va permitir inciar sesion a usuario que ya se haya logueado(registrado)
def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        # se autentica el usuario si no exite nos muestra el error

        usuario = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if usuario is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'El usuario o contraseña es incorrecta'
            })
        else:
            login(request, usuario)
            # Si el usuario es correcto no redirije a la pagina tasks
            return redirect('tasks')



