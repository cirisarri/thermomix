#!/usr/bin/env python3
"""
Genera recetas.json a partir de los archivos receta-*.html.

Uso:
    python3 generar-recetas.py

Escanea las carpetas indicadas (por defecto ./recetas y .), lee el bloque
<script type="application/json" id="meta-receta"> de cada receta y escribe
un único recetas.json en la raíz que el índice puede consumir cuando el
hosting no expone autoindex de directorios (GitHub Pages, Netlify, S3…).

Si una receta no lleva bloque meta-receta, la incluye igualmente con solo
el nombre extraído del <title> y la marca como "Sin categoría".
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
CARPETAS = ["recetas", "."]
PATRON_ARCHIVO = re.compile(r"^receta-[^/]*\.html$", re.IGNORECASE)
PATRON_META = re.compile(
    r'<script[^>]*id=["\']meta-receta["\'][^>]*>([\s\S]*?)</script>',
    re.IGNORECASE,
)
PATRON_TITULO = re.compile(r"<title>([^<]*)</title>", re.IGNORECASE)


def encuentra_htmls() -> list[Path]:
    vistos: set[Path] = set()
    salida: list[Path] = []
    for nombre in CARPETAS:
        carpeta = (RAIZ / nombre).resolve()
        if not carpeta.is_dir():
            continue
        for archivo in sorted(carpeta.iterdir()):
            if not archivo.is_file():
                continue
            if not PATRON_ARCHIVO.match(archivo.name):
                continue
            if archivo in vistos:
                continue
            vistos.add(archivo)
            salida.append(archivo)
    return salida


def lee_meta(archivo: Path) -> dict:
    html = archivo.read_text(encoding="utf-8", errors="replace")

    meta: dict = {}
    m = PATRON_META.search(html)
    if m:
        try:
            meta = json.loads(m.group(1))
        except json.JSONDecodeError as e:
            print(
                f"  ! {archivo.name}: meta-receta con JSON inválido ({e}); "
                "se usa solo el título",
                file=sys.stderr,
            )
            meta = {}

    if "nombre" not in meta:
        t = PATRON_TITULO.search(html)
        meta["nombre"] = (
            t.group(1).split("·")[0].strip() if t else archivo.stem
        )

    if "tipo" not in meta:
        meta["tipo"] = {"id": "otras", "nombre": "Sin categoría"}
    elif isinstance(meta["tipo"], str):
        meta["tipo"] = {"id": meta["tipo"], "nombre": meta["tipo"]}

    ruta_rel = archivo.relative_to(RAIZ).as_posix()
    meta["url"] = ruta_rel
    meta["archivo"] = archivo.name
    return meta


def main() -> int:
    archivos = encuentra_htmls()
    if not archivos:
        print("No he encontrado ninguna receta receta-*.html", file=sys.stderr)
        return 1

    recetas = [lee_meta(a) for a in archivos]
    recetas.sort(key=lambda r: r.get("nombre", "").lower())

    salida = RAIZ / "recetas.json"
    salida.write_text(
        json.dumps({"recetas": recetas}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"Escrito {salida.relative_to(RAIZ)} con {len(recetas)} recetas:")
    for r in recetas:
        print(f"  · {r['nombre']}  [{r['tipo']['nombre']}]  → {r['url']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
