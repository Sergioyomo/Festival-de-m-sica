# 9.1. Consultas básicas

## 1. Mostrar todos los artistas ordenados alfabéticamente.

```python
Artista.objects.order_by("nombre")
```