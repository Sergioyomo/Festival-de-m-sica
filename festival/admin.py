from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Artista)
admin.site.register(Escenario)
admin.site.register(Concierto)
admin.site.register(Perfil)
admin.site.register(Reserva)