"""Registro de fuentes: carga y valida `sources.yaml`, y resuelve citas.

`sources.yaml` es tu única lista blanca de fuentes citables. La regla:
**no se puede citar lo que no está declarado en `sources.yaml`.** Si una tool
intenta citar un id inexistente, `src(...)` se rompe. Así nadie inventa fuentes.

El archivo se busca en el directorio actual de trabajo (CWD). Por eso el ejemplo
de `examples/consumidor/` funciona como una carpeta autónoma y forkeable: tiene
su propio `sources.yaml` al lado de su `my_tools.py`.

Vos NO editás este archivo: solo usás `src("tu_fuente")` en tus tools.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .contract import Source


class _UniqueKeyLoader(yaml.SafeLoader):
    """Loader de YAML que falla si hay ids de fuente repetidos.

    PyYAML normalmente acepta claves duplicadas en silencio (gana la última).
    Para un registro de fuentes eso es peligroso, así que lo prohibimos.
    """


def _no_duplicados(loader: _UniqueKeyLoader, node: yaml.MappingNode) -> dict:
    vistas: set[Any] = set()
    for clave_node, _ in node.value:
        clave = loader.construct_object(clave_node)
        if clave in vistas:
            raise ValueError(
                f"id de fuente repetido en sources.yaml: '{clave}'. "
                "Cada id tiene que ser único."
            )
        vistas.add(clave)
    return loader.construct_mapping(node)


_UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _no_duplicados
)


def _ruta_por_defecto() -> Path:
    """`./sources.yaml`, relativo a donde corrés el programa."""
    return Path.cwd() / "sources.yaml"


def _cargar_registro(ruta: str | Path | None = None) -> dict[str, dict]:
    """Lee `sources.yaml` y devuelve el mapa `id -> {cita, url?, locator?}`."""
    ruta = Path(ruta) if ruta is not None else _ruta_por_defecto()
    if not ruta.exists():
        raise FileNotFoundError(
            f"No encuentro '{ruta}'. Toda carpeta con tools necesita su "
            "sources.yaml al lado, donde declarás las fuentes que vas a citar."
        )
    datos = yaml.load(ruta.read_text(encoding="utf-8"), Loader=_UniqueKeyLoader) or {}
    registro = datos.get("sources")
    if not isinstance(registro, dict):
        raise ValueError(
            f"'{ruta}' tiene que tener una clave 'sources:' con tus fuentes "
            "adentro (un mapa de id -> datos). Mirá el ejemplo del template."
        )
    return registro


def src(id: str, ruta: str | Path | None = None) -> Source:
    """Resuelve una fuente declarada en `sources.yaml` y devuelve un `Source`.

    Esta es la función que usás dentro de tus tools::

        sources=[src("ldc_art_4")]

    Si el id no está declarado en `sources.yaml`, se rompe: no se puede citar
    lo que no está declarado.
    """
    registro = _cargar_registro(ruta)
    if id not in registro:
        disponibles = ", ".join(sorted(registro)) or "(ninguna todavía)"
        raise KeyError(
            f"No se puede citar '{id}': no está declarado en sources.yaml. "
            f"Fuentes declaradas: {disponibles}. "
            "Agregalo primero a sources.yaml y recién después citalo."
        )
    return Source(id=id, **registro[id])


def validate_sources(ruta: str | Path | None = None) -> list[str]:
    """Valida un `sources.yaml` completo. La usa `make check`.

    Comprueba que: el archivo exista, tenga la clave `sources`, los ids sean
    únicos (lo hace el loader), y que cada fuente tenga una `cita` no vacía y
    campos del tipo correcto. Devuelve la lista de ids válidos; si algo está
    mal, se rompe con un mensaje claro.
    """
    registro = _cargar_registro(ruta)
    for id, datos in registro.items():
        if not isinstance(datos, dict):
            raise ValueError(f"La fuente '{id}' tiene que ser un mapa de campos.")
        cita = datos.get("cita")
        if not isinstance(cita, str) or cita.strip() == "":
            raise ValueError(
                f"La fuente '{id}' necesita un campo 'cita' con texto no vacío."
            )
        for campo in ("url", "locator"):
            valor = datos.get(campo)
            if valor is not None and not isinstance(valor, str):
                raise ValueError(
                    f"En la fuente '{id}', el campo '{campo}' tiene que ser "
                    "texto (o quedar vacío)."
                )
        sobrantes = set(datos) - {"cita", "url", "locator"}
        if sobrantes:
            raise ValueError(
                f"La fuente '{id}' tiene campos no reconocidos: {sorted(sobrantes)}. "
                "Campos válidos: cita, url, locator."
            )
    return list(registro)
