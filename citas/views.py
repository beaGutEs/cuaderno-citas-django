"""
Vistas de la app citas.

Aquí están todas las funciones que manejan las páginas de citas:
- Ver lista de citas con filtros
- Inbox (citas sin clasificar)
- Cita aleatoria
- Crear nueva cita
- Editar cita existente
- Marcar/desmarcar favorito

Todas estas vistas están protegidas con @login_required, así que solo 
los usuarios logueados pueden acceder.

También filtro por owner (request.user) para que cada usuario vea solo sus cosas.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
import random
from .models import Cita, Tema
from .forms import QuoteForm, QuoteFilterForm


@login_required
def quote_list(request):
    """
    Lista de todas mis citas con filtros.
    
    Aquí hago varias cosas:
    1. Muestro SOLO las citas del usuario logueado (nadie ve citas de otros)
    2. Permito filtrar por:
       - Texto (busca en el campo text y source)
       - Solo favoritas
       - Solo las que tienen imagen
       - Por tema específico
    
    Los filtros vienen en la URL como parámetros GET, por eso uso request.GET
    Ejemplo: /citas/?q=motivacion&favorite_only=on
    
    OJO: Uso Q() para hacer búsquedas OR (buscar en text O en source)
    """
    # Empiezo con todas las citas del usuario actual
    # .filter(owner=request.user) es súper importante
    # Sin esto, verías las citas de TODOS los usuarios
    citas = Cita.objects.filter(owner=request.user)
    
    # Creo el formulario de filtros
    # Le paso request.GET (los parámetros de la URL)
    # Y le paso user=request.user para que solo muestre temas del usuario
    # Si request.GET está vacío, pongo None para que el form esté vacío
    form = QuoteFilterForm(request.GET or None, user=request.user)
    
    # Compruebo si el formulario es válido
    # Aunque los filtros son opcionales, necesito validar por si hay algo raro
    if form.is_valid():
        # === FILTRO DE BÚSQUEDA POR TEXTO ===
        # Obtengo el valor del campo 'q' (el buscador)
        q = form.cleaned_data.get('q')
        
        # Si el usuario escribió algo en el buscador
        if q:
            # Filtro las citas que contengan 'q' en text O en source
            # icontains = busca sin importar mayúsculas/minúsculas
            # Q() permite hacer OR (|)
            # Sin Q() solo podría hacer AND (&)
            citas = citas.filter(
                Q(text__icontains=q) | Q(source__icontains=q)
            )
        
        # === FILTRO SOLO FAVORITAS ===
        # Si marcó el checkbox de "solo favoritas"
        if form.cleaned_data.get('favorite_only'):
            # Me quedo solo con las que is_favorite=True
            citas = citas.filter(is_favorite=True)
        
        # === FILTRO SOLO CON IMAGEN ===
        # Si marcó el checkbox de "solo con imagen"
        if form.cleaned_data.get('with_image_only'):
            # exclude(image='') quita las que NO tienen imagen
            # También podría hacer: filter(image__isnull=False)
            # Pero exclude me parece más claro
            citas = citas.exclude(image='')
        
        # === FILTRO POR TEMA ===
        # Obtengo el tema seleccionado (si seleccionó alguno)
        tag = form.cleaned_data.get('tag')
        
        # Si eligió un tema específico
        if tag:
            # Filtro solo las citas de ese tema
            citas = citas.filter(tag=tag)
    
    # Renderizo la plantilla
    # Le paso las citas (ya filtradas) y el formulario
    return render(request, 'citas/quote_list.html', {
        'citas': citas,
        'form': form,
    })


@login_required
def quote_inbox(request):
    """
    Inbox: citas sin clasificar.
    
    Esta vista muestra solo las citas que NO tienen tema asignado.
    Es como una "bandeja de entrada" para clasificar después.
    
    Por qué es útil:
    - A veces guardas una cita rápido y no la clasificas
    - Luego vienes aquí y les asignas tema
    
    Filtro por tag__isnull=True (que el tag sea NULL en la BD)
    """
    # Obtengo las citas del usuario que NO tienen tema
    # tag__isnull=True significa "donde tag es NULL"
    # Podría hacer filter(tag=None) pero isnull es más explícito
    citas = Cita.objects.filter(owner=request.user, tag__isnull=True)
    
    # Renderizo la plantilla del inbox
    return render(request, 'citas/quote_inbox.html', {
        'citas': citas,
    })


@login_required
def quote_random(request):
    """
    Muestra una cita aleatoria del usuario.
    
    Me costó un poco esto al principio porque .order_by('?') no me convencía
    (es lento si tienes muchas citas), así que uso random.choice().
    
    Pasos:
    1. Convierto las citas a lista con list()
    2. Uso random.choice() de Python para elegir una
    3. Si no hay citas, pongo None y lo manejo en el template
    """
    # Obtengo todas las citas del usuario y las convierto a lista
    # Convertir a lista es necesario para usar random.choice()
    # Si uso .order_by('?')[0] sería más "Django" pero más lento
    citas = list(Cita.objects.filter(owner=request.user))
    
    # Si hay al menos una cita
    if citas:
        # Elijo una aleatoria
        # random.choice(lista) devuelve un elemento random de la lista
        cita = random.choice(citas)
    else:
        # Si no hay citas, pongo None
        # En el template verifico: {% if cita %}
        cita = None
    
    # Renderizo la plantilla
    return render(request, 'citas/quote_random.html', {
        'cita': cita,
    })


@login_required
def quote_create(request):
    """
    Crear nuevo contenido.
    
    Esta vista maneja dos casos:
    - GET: mostrar el formulario vacío
    - POST: recibir los datos, validar y guardar
    
    OJO: Aquí hay que pasar request.FILES porque el formulario tiene imagen.
    Sin request.FILES, la imagen no se subiría aunque la selecciones.
    
    También hago commit=False para asignar el owner antes de guardar.
    """
    # Si es POST, el usuario envió el formulario
    if request.method == 'POST':
        # Creo el form con los datos enviados
        # request.POST: datos del formulario (text, source, etc.)
        # request.FILES: archivos subidos (la imagen)
        # user=request.user: para filtrar los temas
        form = QuoteForm(request.POST, request.FILES, user=request.user)
        
        # Valido el formulario
        # Esto llama a clean() y comprueba que haya texto o imagen
        if form.is_valid():
            # Guardo pero NO en la BD todavía (commit=False)
            # Necesito asignar el owner antes
            cita = form.save(commit=False)
            
            # Asigno el usuario actual como owner
            # Sin esto, owner estaría vacío y daría error
            cita.owner = request.user
            
            # AHORA sí guardo en la BD
            cita.save()
            
            # Mensaje de éxito (se muestra en el siguiente request)
            # success = mensaje verde en Bootstrap
            messages.success(request, 'Contenido añadido correctamente')
            
            # Redirijo a la lista
            # Post-Redirect-Get pattern: después de POST, siempre redirect
            # Si no hiciera redirect y el usuario recarga, volvería a guardar
            return redirect('citas:quote_list')
    
    # Si es GET (o si el form no era válido)
    else:
        # Creo un formulario vacío
        form = QuoteForm(user=request.user)
    
    # Renderizo el template del formulario
    # Uso el mismo template para crear y editar
    # Por eso paso 'titulo' para saber qué mostrar
    return render(request, 'citas/quote_form.html', {
        'form': form,
        'titulo': 'Añadir Contenido',
    })


@login_required
def quote_edit(request, pk):
    """
    Editar contenido existente.
    
    Parámetros:
    - pk: el ID del contenido (viene en la URL: /citas/edit/5/)
    
    Importante:
    - Uso get_object_or_404 para que si no existe (o no es tuyo), dé error 404
    - Es más seguro que hacer .get() que daría error 500
    
    Reutilizo el mismo formulario que para crear (QuoteForm)
    Pero le paso instance=cita para que precargue los datos
    """
    # Obtengo el contenido de la BD
    # get_object_or_404() busca con pk=pk y owner=request.user
    # Si no existe o no es del usuario, devuelve 404 (Not Found)
    # Esto evita que un usuario edite contenido de otros
    cita = get_object_or_404(Cita, pk=pk, owner=request.user)
    
    # Si es POST, está enviando el formulario editado
    if request.method == 'POST':
        # Creo el form CON instance=cita
        # instance le dice al form que debe EDITAR ese contenido, no crear uno nuevo
        form = QuoteForm(request.POST, request.FILES, instance=cita, user=request.user)
        
        # Valido
        if form.is_valid():
            # Guardo (actualiza el contenido existente)
            # Como ya tiene instance, no necesito asignar owner
            form.save()
            
            # Mensaje de éxito
            messages.success(request, 'Contenido actualizado correctamente')
            
            # Redirijo a la lista
            return redirect('citas:quote_list')
    
    # Si es GET, muestro el formulario con los datos actuales
    else:
        # Creo el form precargado con los datos
        form = QuoteForm(instance=cita, user=request.user)
    
    # Renderizo el mismo template que para crear
    # Pero el título será "Editar Contenido"
    return render(request, 'citas/quote_form.html', {
        'form': form,
        'titulo': 'Editar Contenido',
        'cita': cita,  # Por si quiero mostrar algo más en el template
    })

@login_required
def tema_create(request):
    """
    Crear un nuevo tema.
    """
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        
        if nombre:
            tema, creado = Tema.objects.get_or_create(
                owner=request.user,
                name=nombre
            )
            
            if creado:
                messages.success(request, f'Tema "{nombre}" creado correctamente')
            else:
                messages.info(request, f'Ya tienes un tema llamado "{nombre}"')
            
            next_url = request.GET.get('next', 'citas:quote_list')
            return redirect(next_url)
        else:
            messages.error(request, 'El nombre del tema no puede estar vacío')
    
    # Obtengo los temas del usuario para mostrarlos
    temas = Tema.objects.filter(owner=request.user)
    
    return render(request, 'citas/tema_create.html', {'temas': temas})

@login_required
def quote_toggle_favorite(request, pk):
    """
    Marcar/desmarcar una cita como favorita.
    
    Esta vista solo acepta POST (es un botón, no un enlace).
    
    Lo que hace:
    - Si is_favorite=True, lo pone a False
    - Si is_favorite=False, lo pone a True
    
    Después redirige de vuelta a la página donde estabas.
    
    OJO: Solo POST porque cambiar el estado de algo debe ser POST, no GET.
    Si fuera GET, un bot podría marcar/desmarcar tus favoritos solo visitando URLs.
    """
    # Solo permito POST
    # Si alguien intenta con GET (escribiendo la URL en el navegador), no pasa nada
    if request.method == 'POST':
        # Obtengo la cita (verifico que sea del usuario)
        cita = get_object_or_404(Cita, pk=pk, owner=request.user)
        
        # Cambio el valor de is_favorite
        # not True = False
        # not False = True
        # Es como un switch on/off
        cita.is_favorite = not cita.is_favorite
        
        # Guardo los cambios en la BD
        cita.save()
        
        # Mensaje según el nuevo estado
        if cita.is_favorite:
            messages.success(request, 'Cita marcada como favorita ⭐')
        else:
            messages.info(request, 'Cita desmarcada de favoritas')
    
    # Redirijo de vuelta a donde estaba el usuario
    # request.META.get('HTTP_REFERER') = la URL de donde vino
    # Si no existe, redirijo a la lista por defecto
    # Esto es útil porque puedes marcar favorito desde la lista, inbox o random
    return redirect(request.META.get('HTTP_REFERER', 'citas:quote_list'))