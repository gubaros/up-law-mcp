"""Prueba que el contrato de grounding es fail-closed.

Este archivo es la EVIDENCIA de que una respuesta sin fuentes se rompe. Si algún
día alguien debilita el contrato, estos tests se ponen en rojo.
"""

from __future__ import annotations

import pytest

from legalmcp import GroundedResponse, Source, grounded_tool


def test_respuesta_con_texto_y_sin_fuentes_rompe():
    """El caso central: texto + sin fuentes + not_found=False → ValueError."""
    with pytest.raises(ValueError):
        GroundedResponse(
            answer="El art. 4 obliga al proveedor a informar.",
            sources=[],
            not_found=False,
        )


def test_not_found_sin_fuentes_pasa():
    """El camino honesto: si no encontraste fundamento, not_found=True pasa."""
    r = GroundedResponse(answer=None, sources=[], not_found=True)
    assert r.not_found is True
    assert r.sources == []


def test_respuesta_con_fuente_pasa():
    """Una respuesta bien hecha (con al menos una fuente) es válida."""
    fuente = Source(id="ejemplo", cita="Ley 24.240, art. 4")
    r = GroundedResponse(answer="Tenés derecho a información.", sources=[fuente])
    assert r.sources[0].id == "ejemplo"


def test_answer_en_blanco_sin_fuentes_no_rompe():
    """Texto vacío o solo espacios no cuenta como afirmación: no necesita fuente."""
    r = GroundedResponse(answer="   ", sources=[])
    assert r.sources == []


def test_grounded_tool_propaga_fail_closed():
    """El decorador valida el retorno: una tool que devuelve un dict mal hecho
    (texto, sin fuentes) rompe al ejecutarse."""

    @grounded_tool
    def tool_mal_hecha(consulta: str):
        # Devuelve un dict sin fuentes: el decorador lo valida y debe romper.
        return {"answer": "Afirmo algo del derecho", "sources": [], "not_found": False}

    with pytest.raises(ValueError):
        tool_mal_hecha("una consulta cualquiera")


def test_grounded_tool_conserva_nombre_y_doc():
    """FastMCP expone el nombre y el docstring de tu función: deben conservarse."""

    @grounded_tool
    def saludo(consulta: str) -> GroundedResponse:
        """Documentación de la tool."""
        return GroundedResponse(not_found=True)

    assert saludo.__name__ == "saludo"
    assert saludo.__doc__ == "Documentación de la tool."
