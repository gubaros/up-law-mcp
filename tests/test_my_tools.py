"""Prueba TODOS los servers del repo de punta a punta: tu `my_tools.py` (raíz) y
el ejemplo `examples/consumidor/`.

Para cada tool registrada, sobre varias consultas de fixture, verifica que:
  1. devuelve un GroundedResponse válido,
  2. está fundamentada (tiene fuentes) o es honesta (not_found=True),
  3. y que toda fuente citada existe en el sources.yaml de ESE directorio.

Esto es lo que hace honesto al checkpoint 5 del README: si en TU `my_tools.py`
citás una fuente que no declaraste, o escribís una respuesta sin fuente,
`make check` se pone en rojo. No solo el ejemplo queda protegido: tu código
también.

La raíz recién generada trae su tool de ejemplo comentada (cero tools): en ese
caso no hay nada que ejecutar y el test pasa, validando igual que tu sources.yaml
esté bien formado.
"""

from __future__ import annotations

import inspect

from legalmcp import GroundedResponse
from legalmcp.sources import validate_sources

# Consultas de fixture: distintas, para ejercitar tanto el camino fundamentado
# como el camino not_found en el conjunto de tools.
CONSULTAS_FIXTURE = [
    "¿Tengo derecho a información clara sobre el precio de un producto?",
    "¿Qué garantía tengo si el producto sale con un defecto?",
    "¿Cuál es la capital de Francia?",  # claramente fuera de dominio
]


def _invocar(fn, consulta):
    """Llama a una tool pasando la consulta a cada parámetro de texto que tenga."""
    parametros = inspect.signature(fn).parameters
    return fn(**{nombre: consulta for nombre in parametros})


def test_el_ejemplo_registra_tools(directorio_con_tools):
    """El ejemplo de consumidor tiene que aportar al menos una tool real."""
    directorio, tools = directorio_con_tools
    if directorio.name == "consumidor":
        assert tools, "El ejemplo de consumidor debería registrar al menos una tool."


def test_toda_tool_devuelve_grounded_o_not_found(directorio_con_tools):
    directorio, tools = directorio_con_tools

    # CWD ya es `directorio`, así que esto valida y lee SU sources.yaml.
    ids_declarados = set(validate_sources("sources.yaml"))

    for fn in tools:
        for consulta in CONSULTAS_FIXTURE:
            resp = _invocar(fn, consulta)

            # 1) Es un GroundedResponse válido.
            assert isinstance(resp, GroundedResponse)

            # 2) O está fundamentado (tiene fuentes) o es honesto (not_found).
            assert resp.not_found or resp.sources, (
                f"En '{directorio.name}', la tool '{fn.__name__}' devolvió una "
                "respuesta sin fuentes y sin marcar not_found."
            )

            # 3) Toda fuente citada existe en el sources.yaml de este directorio.
            for fuente in resp.sources:
                assert fuente.id in ids_declarados, (
                    f"En '{directorio.name}', la tool '{fn.__name__}' citó "
                    f"'{fuente.id}', que no está declarado en sources.yaml."
                )
