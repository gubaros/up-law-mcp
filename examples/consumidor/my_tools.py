"""Ejemplo completo y funcionando: derechos del consumidor (Ley 24.240).

Este archivo es un MCP server real, chico pero de verdad. Tiene dos tools que
responden consultas sobre la Ley de Defensa del Consumidor (LDC). Podés forkear
toda la carpeta `examples/consumidor/` y usarla como punto de partida.

Convención del template: toda tool legal recibe una `consulta: str` (lo que
pregunta la persona) y devuelve un `GroundedResponse`.
"""

# Importamos las tres piezas del harness que vamos a usar.
from legalmcp import GroundedResponse, grounded_tool, src


@grounded_tool
def derecho_a_informacion(consulta: str) -> GroundedResponse:
    """Explica el derecho del consumidor a recibir información clara y veraz.

    Útil para preguntas sobre precios, etiquetado, publicidad y características
    de un producto o servicio.
    """
    # Palabras que indican que la consulta es sobre información al consumidor.
    palabras_clave = ("informaci", "publicidad", "precio", "etiqueta", "datos")

    # Si la consulta NO es sobre este tema, no inventamos: devolvemos not_found.
    if not any(palabra in consulta.lower() for palabra in palabras_clave):
        return GroundedResponse(
            answer=None,
            not_found=True,
            confidence="alta",
        )

    # Si es sobre este tema, respondemos CITANDO la fuente con src(...).
    return GroundedResponse(
        answer=(
            "El proveedor debe darte información cierta, clara y detallada sobre "
            "las características esenciales de los bienes y servicios que ofrece. "
            "Es un derecho del consumidor, no una cortesía."
        ),
        sources=[src("ldc_art_4")],  # ← la cita sale de sources.yaml
        confidence="alta",
    )


@grounded_tool
def plazo_de_garantia(consulta: str) -> GroundedResponse:
    """Explica la garantía legal sobre cosas muebles no consumibles.

    Esta tool muestra a propósito el camino `not_found=True`: si la consulta cae
    fuera del dominio (no es sobre garantía), NO fabrica una respuesta.
    """
    palabras_clave = ("garant", "defecto", "falla", "repar", "vicio")

    # Camino "fuera de dominio": preferimos decir "no encontré" antes que inventar.
    if not any(palabra in consulta.lower() for palabra in palabras_clave):
        return GroundedResponse(
            answer=None,
            not_found=True,
            confidence="alta",
        )

    return GroundedResponse(
        answer=(
            "Las cosas muebles no consumibles tienen garantía legal por sus "
            "defectos o vicios. La garantía corre desde la entrega del bien y el "
            "vendedor responde por ella aunque no la haya ofrecido."
        ),
        sources=[src("ldc_art_11")],  # ← la cita sale de sources.yaml
        confidence="media",
    )
