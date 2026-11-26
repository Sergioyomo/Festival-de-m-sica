from django.db import models
from django.conf import settings
from django.db.models import Q



# Create your models here.
class Artista(models.Model):
    class Genero_musical(models.TextChoices):
        ROCK = "ROCK", "Rock"
        POP = "POP", "Pop"
        CLASICA = "CLAS", "Clasica"
        METAL = "META", "Metal"
        BACHATA = "BACH", "Bachata"

    nombre = models.CharField(max_length=200, unique=True)
    pais = models.CharField(max_length=100)
    genero_musical = models.CharField(
        max_length=4,
        choices=Genero_musical.choices,
        default=Genero_musical.CLASICA,
    )
    fecha_creacion = models.DateTimeField()
    cache = models.DecimalField(default=0.00, max_digits=8, decimal_places=2)
    activo = models.BooleanField(default=True)

    constraints = [
        models.CheckConstraint(
            condition=Q(cache__gte=0),
            name="Artista_cache_no_negativo",
        ),
    ]


    def __str__(self) -> str:
        return self.nombre

class Escenario(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    ubicacion = models.CharField(max_length=200)
    aforo = models.IntegerField(null=False)
    cubierto = models.BooleanField(default=True)
    artistas = models.ManyToManyRel(
        to="Artista",
        related_name="escenarios",
        field="escenarios",
    )      
    def __str__(self) -> str:
        return self.nombre

class Concierto(models.Model):
    nombre = models.CharField(max_length=150)
    fecha_hora = models.DateTimeField()
    duracion = models.IntegerField(null=False)
    precio = models.DecimalField(default=0.00, max_digits=8, decimal_places=2)
    artista = models.ForeignKey(
        "Artista", on_delete=models.CASCADE, related_name="conciertos"
    )
    escenario = models.ForeignKey(
        "Escenario", on_delete=models.CASCADE, related_name="escenarios"
    )
    entradas_disponibles = models.BooleanField(default=True)
    cancelado = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.nombre

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["artista", "escenario"], name="participacion_unica_artista_escenario"
            ),
            models.CheckConstraint(
                condition=Q(precio__gte=0),
                name="Concierto_precio_no_negativo",
                ),
            models.CheckConstraint(
                condition=Q(entradas_disponibles__gte=0),
                name="Concierto_entradas_disponibles_no_negativo",
                ),
        ]

class Perfil(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="perfil",
    )
    dni = models.CharField(max_length=9, unique=True)
    telefono = models.IntegerField()
    fecha_nacimiento = models.DateField()
    localidad = models.CharField(max_length=120)

    class Meta:
            constraints = [
                models.UniqueConstraint(
                    fields=["dni"], name="dni_unico_perfil"
                ),
            ]

    def __str__(self) -> str:
        return self.usuario.username

class Reserva(models.Model):
    class Estado(models.TextChoices):
            CONFIRMADA = "CONFIR", "Confirmada"
            CANCELADA = "CANCEL", "Cancelada"
    localizador = models.CharField(max_length=9, unique=True)
    usuario = models.ForeignKey(
            settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="usuarios"
        )
    concierto = models.ForeignKey(
            "Concierto", on_delete=models.CASCADE, related_name="conciertos"
        )
    fecha_reserva = models.DateTimeField()
    num_entrada = models.IntegerField()
    importe_total = models.DecimalField(default=0.00, max_digits=8, decimal_places=2)
    estado = models.CharField(
        max_length=6,
        choices=Estado.choices,
        default=Estado.CONFIRMADA,
    )
    def __str__(self) -> str:
        return self.localizador
    