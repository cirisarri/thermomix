# Recetario Thermomix

Recetario web estático, cero dependencias, pensado para el móvil. Cada receta
es una página HTML autónoma con temporizadores, escalado de raciones y checks
de ingredientes. El índice se descubre solo las recetas al cargar.

Estado actual: **258 recetas en 13 categorías** (37 marcadas como Thermomix,
221 tradicionales).

## Ramas y flujo de trabajo

- `main` — rama de producción, la que sirve GitHub Pages.
- Las nuevas recetas o cambios se hacen en ramas de trabajo (feature branches)
  y se abren como pull request contra `main`.

## Estructura

```
.
├── index.html                 # Índice / buscador / filtro Thermomix
├── recetas/
│   ├── receta-pisto.html      # Una página por receta
│   └── receta-*.html
├── recetas.json               # Manifiesto para hostings sin autoindex
├── generar-recetas.py         # Escanea recetas/ y produce recetas.json
└── scripts/
    ├── build-recetas.py       # Fuente de verdad: datos + genera todas las HTML
    └── plantilla-receta.md    # Plantilla para dictar una receta nueva
```

## Ver el recetario en local

Abrirlo con doble clic (`file://`) NO vale: el navegador bloquea la lectura de
la carpeta. Levantar un servidor mínimo:

```bash
python3 -m http.server 8000
# abrir http://localhost:8000
```

Para publicarlo (GitHub Pages, Netlify, S3…) basta con subir la carpeta tal
cual; `recetas.json` sirve como plan B cuando el hosting no expone autoindex.

## Cómo añadir una receta nueva

Hay dos formas, elige la que te resulte más cómoda.

### Camino corto (recomendado): pásame la receta

Envíame la receta como quieras — un `.docx`, un `.doc`, un `.txt`, un párrafo
pegado en el chat, una foto de una página de recetario, un link a una web —
y yo la convierto, la meto en `scripts/build-recetas.py`, regenero, valido y
empujo. En cada tanda te digo qué he añadido, qué he descartado por falta de
datos y en qué categoría cae.

Formato ideal para no perder información:

- Nombre.
- Aparato (Thermomix / tradicional). Si es Thermomix, qué modelos (TM7/6/5/31).
- Categoría sugerida (o «tú decides»).
- Raciones base.
- Tiempos de preparación y totales.
- Lista de ingredientes con cantidades y unidades.
- Pasos numerados. Para cada paso Thermomix: tiempo, temperatura, velocidad,
  giro inverso si aplica.
- Sugerencia de servicio y notas al final.

Si algún dato falta lo estimo con criterio y lo marco en las notas.

### Camino técnico: editar el generador

Toda la información de las recetas vive en la lista `RECETAS` del script
`scripts/build-recetas.py`. El proceso es:

1. Abre `scripts/build-recetas.py` y añade un diccionario a la lista `RECETAS`
   siguiendo la misma forma que las de al lado (ver
   [`scripts/plantilla-receta.md`](scripts/plantilla-receta.md) para la
   plantilla comentada).
2. Regenera las páginas:

   ```bash
   python3 scripts/build-recetas.py
   ```

   Esto sobrescribe todas las `recetas/receta-*.html` a partir de los datos.

3. Regenera el manifiesto que consume el índice cuando no hay autoindex:

   ```bash
   python3 generar-recetas.py
   ```

4. Commit y push.

### Categorías activas

Se listan solas en el índice a partir del campo `tipo` de cada receta. Las que
hay ahora mismo:

- Aliños y salsas · Aperitivos · Arroces y risottos · Carnes · Cremas y sopas
  · Ensaladas · Guarniciones · Pastas y arroces · Pescados · Postres ·
  Primeros y otros · Pudines y pasteles · Verduras

Para crear una categoría nueva basta con usar un `tipo` nuevo en el
diccionario de una receta. El nombre visible sale del segundo elemento de la
tupla (`("id", "Nombre visible")`).

### Filtro Thermomix

El índice muestra una insignia **TM** en las recetas que declaren al menos un
modelo Thermomix en el campo `modelos`. Los tres chips de arriba filtran
entre «Todas», «Thermomix» y «Tradicional». La preferencia se guarda en
`localStorage` del navegador.

## Convención de unidades

Estas unidades saben pluralizarse y reescalarse al cambiar raciones (ver
`cantidad()` en `receta-pisto.html`):

`g`, `ml`, `cdta`, `cda`, `diente`, `hoja`, `vaina`, `pastilla`, `ramita`,
`manojo`, `lata`, `sobre`, `pellizco`, `u` (unidad).
