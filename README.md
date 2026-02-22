# Cuaderno de Citas

Aplicación web para guardar contenido inspiracional (memes, citas, imágenes) y organizarlo por temas.

## Requisitos

- Python 3.8 o superior
- pip

## Instalación

1. Crear y activar entorno virtual:

Windows:
```
python -m venv venv
venv\Scripts\activate
```

Linux/Mac:
```
python3 -m venv venv
source venv/bin/activate
```

2. Instalar dependencias:
```
pip install -r requirements.txt
```

3. Aplicar migraciones:
```
python manage.py migrate
```

4. Crear superusuario (opcional pero recomendado):
```
python manage.py createsuperuser
```
Credenciales sugeridas: admin / admin123

5. Iniciar servidor:
```
python manage.py runserver
```

6. Acceder en el navegador: http://127.0.0.1:8000

## Usuarios de prueba

Superusuario:
- Usuario: admin
- Contraseña: admin123
- Acceso admin: http://127.0.0.1:8000/admin/

Usuario normal (crear desde registro o admin):
- Usuario: demo
- Contraseña: demo1234

## Estructura

- **core**: Páginas públicas (home, about)
- **accounts**: Autenticación (registro, login, logout)
- **citas**: Gestión de contenido (crear, listar, editar, filtrar)

## Funcionalidades

- Registro e inicio de sesión de usuarios
- Crear contenido con texto y/o imagen (obligatorio al menos uno)
- Organizar contenido por temas personalizados
- Marcar contenido como favorito
- Inbox para contenido sin clasificar
- Vista aleatoria
- Búsqueda y filtrado por texto, favoritos, imágenes, tema

## Modelos

- **Tema**: Categorías para organizar (Motivación, Memes, etc.)
- **Cita**: Contenido con texto/imagen, fuente, tema, favorito

Relaciones:
- Un usuario tiene muchos temas y citas
- Una cita pertenece a un tema (opcional)

## Notas técnicas

- Base de datos: SQLite
- Framework CSS: Bootstrap 5
- Formularios: django-crispy-forms
- Imágenes: Pillow (ImageField)
- Autenticación: sistema de Django con login_required
- Validación: al menos texto o imagen obligatorio
```
