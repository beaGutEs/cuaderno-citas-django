"""
Vistas de autenticación.

Aquí manejo todo lo de usuarios:
- Registro de nuevos usuarios
- Login (inicio de sesión)
- Logout (cerrar sesión)

Uso los formularios que trae Django (UserCreationForm y AuthenticationForm)
en vez de hacerlos desde cero porque ya tienen toda la validación.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import RegisterForm


def register(request):
    """
    Registro de nuevos usuarios.
    
    Pasos:
    1. El usuario rellena username, email, password1, password2
    2. Django valida (passwords iguales, username único, etc.)
    3. Si todo OK, creo el usuario
    4. Lo logueo automáticamente (para que no tenga que volver a escribir la contraseña)
    5. Redirijo a la lista de citas
    
    OJO: Extendí UserCreationForm en forms.py para añadir email obligatorio.
    """
    # Si es POST, está enviando el formulario de registro
    if request.method == 'POST':
        # Creo el form con los datos enviados
        form = RegisterForm(request.POST)
        
        # Valido el formulario
        # Comprueba:
        # - Username único (que no exista ya)
        # - Passwords iguales
        # - Password cumple requisitos de seguridad
        # - Email válido
        if form.is_valid():
            # Guardo el usuario en la BD
            # form.save() crea el User y lo devuelve
            user = form.save()
            
            # Logueo al usuario automáticamente
            # Así no tiene que ir a login después de registrarse
            # login() crea la sesión y asocia el usuario
            login(request, user)
            
            # Mensaje de bienvenida
            messages.success(request, f'¡Bienvenido, {user.username}! Tu cuenta ha sido creada.')
            
            # Redirijo a la lista de citas
            # Podría ir a 'core:home' pero prefiero mandarlo directo a las citas
            return redirect('citas:quote_list')
    
    # Si es GET, muestro el formulario vacío
    else:
        form = RegisterForm()
    
    # Renderizo el template de registro
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """
    Login de usuarios existentes.
    
    Proceso:
    1. Usuario escribe username y password
    2. Django verifica que sean correctos
    3. Si OK, creo la sesión
    4. Redirijo a donde iba el usuario (o a citas por defecto)
    
    Lo del 'next' es para cuando intentas acceder a una página protegida:
    - Intentas ir a /citas/create/
    - No estás logueado
    - Te manda a /login/?next=/citas/create/
    - Después de login, te manda de vuelta a /citas/create/
    """
    # Si es POST, está intentando loguearse
    if request.method == 'POST':
        # AuthenticationForm necesita 'request' como primer parámetro
        # No es como los otros forms
        # data=request.POST tiene los datos del formulario
        form = AuthenticationForm(request, data=request.POST)
        
        # Valido las credenciales
        # Comprueba que el usuario exista y la contraseña sea correcta
        if form.is_valid():
            # Obtengo el usuario validado
            # form.get_user() devuelve el User si la validación fue OK
            user = form.get_user()
            
            # Creo la sesión (logueo al usuario)
            login(request, user)
            
            # Mensaje de bienvenida
            messages.success(request, f'Hola de nuevo, {user.username}')
            
            # Obtengo la URL a la que iba el usuario (si existe)
            # request.GET.get('next') lee el parámetro ?next=...
            # Si no existe, uso 'citas:quote_list' por defecto
            next_url = request.GET.get('next', 'citas:quote_list')
            
            # Redirijo
            return redirect(next_url)
        else:
            # Si las credenciales no son válidas, muestro error
            # El formulario ya tiene los errores, pero añado un mensaje extra
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    # Si es GET, muestro el formulario vacío
    else:
        form = AuthenticationForm()
    
    # Renderizo el template de login
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """
    Logout (cerrar sesión).
    
    Esto es super simple:
    1. Borro la sesión del usuario
    2. Muestro un mensaje
    3. Redirijo al home
    
    No necesita ser POST porque no está cambiando datos.
    Solo está borrando la sesión, que es del propio usuario.
    """
    # Cierro la sesión
    # logout() borra la cookie de sesión
    logout(request)
    
    # Mensaje informativo
    messages.info(request, 'Has cerrado sesión correctamente')
    
    # Redirijo al home
    # Podría ir a login pero prefiero home para que vea la página pública
    return redirect('core:home')