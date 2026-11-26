# 9.1. Consultas básicas

## 1. Mostrar todos los artistas ordenados alfabéticamente.

```python
Artista.objects.order_by("nombre")
```

## 2. Mostrar únicamente los artistas activos.

```python
Artista.objects.filter(activo=True)
```

## 3. Obtener los artistas de un determinado país.

```python
Artista.objects.filter(pais__icontains="España")
```

## 4. Buscar artistas cuyo nombre contenga una cadena de texto.

```python
Artista.objects.filter(nombre__icontains="as")
```

## 5. Mostrar los conciertos cuyo precio esté comprendido entre 20 y 50 euros.

```python
Concierto.objects.filter(precio__gte=20,precio__lte=50)
```

## 6. Mostrar los conciertos gratuitos.

```python
Concierto.objects.filter(precio=0)
```

## 7. Mostrar los conciertos con entradas disponibles y no cancelados.


```python
 Concierto.objects.filter(entradas_disponibles=True, cancelado=False)
 ```

## 8. Mostrar los conciertos ordenados por fecha y hora.

```python
Concierto.objects.order_by("fecha_hora")
```

# 9.2. Consultas sobre modelos relacionados

## 9. Mostrar los conciertos de un escenario determinado.

```python
Concierto.objects.filter(escenario__pk=1)
```

## 10. Mostrar los artistas de un concierto.

```python
Artista.objects.filter(conciertos__pk=1)
```

## 11. Obtener los conciertos en los que participa un artista.

```python
Artista.objects.get(pk=1).conciertos.all()
```

## 12. Mostrar las reservas de un usuario.

```python
Reserva.objects.filter(usuario__pk=1)
```

## 13. Mostrar los usuarios con alguna reserva confirmada para un concierto determinado, sin duplicados.

```python
User.objects.filter(usuarios__concierto__pk=1).distinct()
```

## 14. Mostrar los conciertos con artistas de un determinado país.

```python
Concierto.objects.filter(artista__pais="España")
```

## 15. Mostrar los artistas que no participan en ningún concierto.

```python
Artista.objects.filter(conciertos__isnull=True)
```

# 9.3. Consultas de agregación y agrupación

## 16. Calcular el precio medio de los conciertos.

```python
Concierto.objects.aggregate(precio_medio=Avg("precio"))
```

## 17. Obtener el precio del concierto más caro y del más barato.

```python
Concierto.objects.aggregate(precio_maximo=Max("precio"), precio_minimo=Min("precio"))
```

## 18. Calcular el aforo total de todos los escenarios.

```python
Escenario.objects.aggregate(aforo_total=Sum("aforo"))
```

## 19. Obtener el número de conciertos de cada escenario.

```python
Escenario.objects.annotate(total_conciertos=Count("escenarios"))
```

## 20. Obtener el número de conciertos en los que participa cada artista.

```python
Artista.objects.annotate(total_conciertos=Count("conciertos"))
```

## 21. Calcular el número total de entradas reservadas y confirmadas por concierto.

```python
Concierto.objects.annotate(total_entradas=Sum("conciertos__num_entrada",filter=Q(conciertos__estado="CONFIR")))
```

## 22. Calcular la recaudación de cada concierto, excluyendo reservas canceladas.

```python
Concierto.objects.annotate(recaudacion=Sum("conciertos__importe_total")).exclude(conciertos__estado="CANCEL")
```

## 23. Obtener los tres conciertos con más entradas reservadas y confirmadas.

```python
Concierto.objects.annotate(total_entradas=Sum("conciertos__num_entrada",filter=Q(conciertos__estado="CONFIR"))).order_by("-total_entradas")[:3]
```

## 24. Mostrar los usuarios con más de una reserva confirmada.

```python
User.objects.annotate(total_reservas=Count("usuarios",filter=Q(usuarios__estado="CONFIR"))).filter(total_reservas__gt=1)
```