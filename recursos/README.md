# Recursos del proyecto

Aquí se guardan las imágenes e iconos de la interfaz, separados del código y de los datos.

```text
recursos/
├── imagenes/   fotos, ilustraciones, logos, capturas
└── iconos/     iconos pequeños para botones, menús y ventanas
```

## Cómo usarlos

Las rutas se arman desde `core/configuracion.py` para no repetir rutas en las ventanas:

```python
from core import configuracion

ruta = configuracion.ruta_de_imagen("portada_biblioteca.png")
ruta = configuracion.ruta_de_icono("libro.svg")
```

## Formatos recomendados

- `PNG` o `JPG` para imágenes.
- `SVG` o `PNG` para iconos.
- Nombres en minúsculas, sin espacios y con guion bajo: `logo_biblioteca.png`.

## Por ahora

La interfaz se está trabajando sin estilos ni imágenes. Esta carpeta queda preparada para cuando se agreguen los recursos visuales al final.
