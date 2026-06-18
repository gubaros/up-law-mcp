"""El contrato de fundamentación (grounding). Este es el corazón del template.

La idea es simple y estricta: **una respuesta que afirma algo sobre el derecho
no puede existir sin citar de dónde lo saca.** Si intentás construir una
respuesta con texto pero sin fuentes, el programa se rompe a propósito
(fail-closed). Así, por construcción, no podés shippear una tool que afirme
derecho sin fundamento.

Como estudiante NO necesitás editar este archivo. Solo lo usás:
- `GroundedResponse` es lo que tus tools devuelven.
- `Source` es una fuente citada (la obtenés con `src(...)`, ver sources.py).
- `@grounded_tool` es el decorador que ponés arriba de cada tool.
"""

from __future__ import annotations

import functools
from typing import Callable, Literal

from pydantic import BaseModel, model_validator

# Registro global de las tools decoradas con @grounded_tool.
# Cada vez que Python "lee" una tool decorada, la función se agrega acá.
# Después, server.py recorre esta lista para registrarlas en el servidor MCP.
# (Vos no tocás esto.)
_REGISTRY: list[Callable] = []


class Source(BaseModel):
    """Una fuente jurídica citada.

    No la construís a mano: la obtenés con `src("id_de_tu_fuente")`, que la
    resuelve desde `sources.yaml`. Así te asegurás de que toda cita esté
    declarada en un solo lugar.
    """

    id: str  # identificador corto, p. ej. "ldc_art_4"
    cita: str  # texto de la cita, p. ej. "Ley 24.240, art. 4 — Información"
    url: str | None = None  # URL oficial (InfoLEG, etc.) si la verificaste
    locator: str | None = None  # ubicación fina: "art. 4", "considerando 12", "p. 7"


class GroundedResponse(BaseModel):
    """La respuesta que devuelve toda tool legal.

    Campos:
    - `answer`: el texto de la respuesta (o `None` si no hay respuesta).
    - `sources`: la lista de fuentes que respaldan la respuesta.
    - `confidence`: tu nivel de confianza ("alta" | "media" | "baja").
    - `not_found`: poné `True` cuando NO encontraste fundamento para responder.

    La regla de oro la aplica el validador de abajo.
    """

    answer: str | None = None
    sources: list[Source] = []
    confidence: Literal["alta", "media", "baja"] = "media"
    not_found: bool = False

    @model_validator(mode="after")
    def _toda_respuesta_necesita_fuentes(self) -> "GroundedResponse":
        # ¿Hay texto de respuesta de verdad? (None o espacios en blanco = no hay)
        hay_texto = self.answer is not None and self.answer.strip() != ""

        # FAIL-CLOSED: si afirmás algo (hay texto) y no marcaste not_found,
        # entonces TENÉS que citar al menos una fuente. Si no, se rompe.
        if hay_texto and not self.not_found and not self.sources:
            raise ValueError(
                "Una respuesta con texto NO puede ir sin fuentes.\n"
                "  → Agregá al menos un Source usando src(\"tu_fuente\"), o\n"
                "  → devolvé GroundedResponse(not_found=True) si no encontraste "
                "fundamento jurídico para responder.\n"
                "Esto es a propósito: en derecho, afirmar sin fuente no vale."
            )
        return self


def grounded_tool(fn: Callable) -> Callable:
    """Decorador que convierte una función en una tool legal del servidor MCP.

    Hace tres cosas:
    1. Registra la función para que el servidor la exponga como tool.
    2. Valida que lo que devolvés sea un `GroundedResponse` (si devolvés un
       diccionario, lo convierte y valida por vos).
    3. Propaga el fail-closed: si la respuesta no cumple el contrato, se rompe.

    Conserva el nombre y el docstring de tu función para que el cliente MCP los
    vea tal cual los escribiste.

    Uso::

        @grounded_tool
        def mi_tool(consulta: str) -> GroundedResponse:
            "Explicá acá qué hace tu tool."
            ...
    """

    @functools.wraps(fn)  # conserva nombre y docstring de tu función
    def wrapper(*args, **kwargs) -> GroundedResponse:
        resultado = fn(*args, **kwargs)
        # Si ya es un GroundedResponse, quedó validado al construirse.
        # Si devolviste un dict, lo validamos acá (y rompe si no cumple).
        if not isinstance(resultado, GroundedResponse):
            resultado = GroundedResponse.model_validate(resultado)
        return resultado

    _REGISTRY.append(wrapper)
    return wrapper
