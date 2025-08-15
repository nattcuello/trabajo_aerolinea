README - Proyecto "Avioncitos JeyJey"
====================================================

1. Datos Generales
----------------------------------------------------
Nombre oficial del proyecto: Avioncitos JeyJey
Integrantes: Cuello Natalia, Gonzalez Sofia y Reartes Imanol
Fecha de entrega: 14/08/2025 23:59hs

2. Resumen Ejecutivo
----------------------------------------------------
Objetivo:
Desarrollar un sistema web completo para gestionar una aerolínea,
implementando los conceptos aprendidos durante el primer semestre.

Listado de módulos (por app):

App pasajeros:
- Pasajero

App reservas:
- Asiento
- AsientoVuelo
- Reserva

App usuarios:
- PerfilUsuario

App vuelos:
- Avion
- Vuelo

Tecnologías exactas usadas:
- asgiref 3.8.1
- Django 5.2.3
- djangorestframework 3.16.0
- pip 24.0
- sqlparse 0.5.3
- sqlite (última versión)
- DBeaver (última versión)
- JavaScript (última versión)

3. Arquitectura
----------------------------------------------------
EFI V3
|----.environment
|----trabajo_aerolinea
     |---- pasajeros
          |---- migrations
          |---- templates
          |---- repositories.py
          |---- services.py
          |---- admin.py
          |---- forms.py
          |---- apps.py
          |---- models.py
          |---- tests.py
          |---- urls.py
          |---- views.py
          |---- serializers.py
     |---- usuarios
          |---- templates
          |---- repositories.py
          |---- services.py
          |---- migrations
          |---- admin.py
          |---- forms.py
          |---- apps.py
          |---- models.py
          |---- tests.py
          |---- urls.py
          |---- views.py
          |---- serializers.py
          |---- signals.py
     |---- reservas
          |---- management
          |---- templates
          |---- repositories.py
          |---- services.py
          |---- migrations
          |---- admin.py
          |---- forms.py
          |---- apps.py
          |---- models.py
          |---- tests.py
          |---- urls.py
          |---- views.py
          |---- serializers.py
          |---- signals.py
     |---- vuelos
          |---- repositories.py
          |---- services.py
          |---- migrations
          |---- templates
          |---- admin.py
          |---- forms.py
          |---- apps.py
          |---- models.py
          |---- tests.py
          |---- urls.py
          |---- views.py
          |---- serializers.py
          |---- signals.py

	home
	  migrations
	  templates
	  admin.py
	  apps.py
	  models.py
	  tests.py
	  urls.py
	  views.py

	trabajo_aerolinea
	  __init__.py
	  asgi.py
	  settings.py
	  urls.py
	  wsgi.py
  .gitignore
  manage.py
  requirements.txt
  db.sqlite3

4. Guía de Instalación
----------------------------------------------------
Requisitos previos:
- Python 3.12+
- pip instalado
- Entorno virtual recomendado

Pasos de instalación:
1. Clonar el repositorio:
   git clone <URL_DEL_REPOSITORIO>

2. Acceder al directorio del proyecto:
   cd trabajo_aerolinea

3. Crear y activar entorno virtual:
   python3 -m venv .environment
   source .environment/bin/activate

4. Instalar dependencias:
   pip install -r requirements.txt

5. Realizar migraciones:
   python manage.py migrate

6. Crear superusuario:
   python manage.py createsuperuser

7. Iniciar el servidor de desarrollo:
   python manage.py runserver

8. Acceder a la aplicación:
   http://127.0.0.1:8000

5. Manual de Usuario
----------------------------------------------------
Primera vista:
- Iniciar sesión: si ya estás registrado, utilizá tus credenciales.
- Registrarse: si es la primera vez, registrate como pasajero.

Vista pasajero:
- Inicio: vuelve al home.
- Vuelos: permite reservar, ver asientos disponibles y realizar reservas.
- Ver detalle: muestra detalles de reservas realizadas.

Vista admin:
- Pasajeros: listado con información y opción de crear pasajero.
- Vuelos: CRUD completo de vuelos.
- Nuevo vuelo: formulario para cargar nuevo vuelo.
- Nuevo avión: formulario para crear nuevo avión.

====================================================
