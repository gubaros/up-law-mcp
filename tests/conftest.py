"""Configuración de los tests.

La suite exige el contrato sobre servers REALES y, sobre todo, sobre **el código
que vos editás**. Por eso recorre dos directorios:

- la raíz del repo (tu `my_tools.py` + tu `sources.yaml`), y
- el ejemplo `examples/consumidor/` (completo y funcionando).

Cada directorio es un server autónomo: el fixture se para adentro (CWD), lo pone
en el path e importa su `my_tools.py`, devolviendo las tools registradas junto
con el directorio. Así `make check` certifica también lo que vos escribís.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Raíz del repo (la carpeta que contiene este `tests/`) y el ejemplo.
RAIZ = Path(__file__).resolve().parent.parent
EJEMPLO = RAIZ / "examples" / "consumidor"

# Los directorios que la suite trata como servers a verificar.
DIRECTORIOS = [RAIZ, EJEMPLO]


def _cargar_tools(monkeypatch, directorio: Path) -> list:
    """Se para en `directorio`, importa su `my_tools.py` y devuelve sus tools."""
    import legalmcp.contract as contract

    monkeypatch.chdir(directorio)
    monkeypatch.syspath_prepend(str(directorio))

    # Estado limpio: vaciamos el registro global y descacheamos my_tools, para
    # que cada directorio cargue el suyo sin mezclarse con otro.
    contract._REGISTRY.clear()
    sys.modules.pop("my_tools", None)

    import my_tools  # noqa: F401  (importarlo registra sus tools)

    return list(contract._REGISTRY)


@pytest.fixture(params=DIRECTORIOS, ids=lambda p: p.name or "raiz")
def directorio_con_tools(request, monkeypatch):
    """Devuelve `(directorio, tools)` para cada server del repo (raíz y ejemplo)."""
    directorio: Path = request.param
    tools = _cargar_tools(monkeypatch, directorio)

    yield directorio, tools

    # Limpieza para el resto de la suite.
    import legalmcp.contract as contract

    contract._REGISTRY.clear()
    sys.modules.pop("my_tools", None)
