"""Acá escribís TUS tools. Es el único archivo de código que vas a tocar.

Esto es una plantilla: abajo hay UNA tool de ejemplo, comentada, para que la
copies, le cambies el texto y las fuentes, y la descomentes. Cuando termines,
declará tus fuentes en `sources.yaml` (al lado de este archivo) y corré
`make check`.

Para ver un ejemplo completo y funcionando antes de empezar, mirá
`examples/consumidor/my_tools.py`.

Convención del template: toda tool recibe una `consulta: str` y devuelve un
`GroundedResponse`.
"""

# Estas tres piezas vienen del harness (la carpeta legalmcp/). No las toques;
# solo usalas.
from legalmcp import GroundedResponse, grounded_tool, src  # noqa: F401


# --------------------------------------------------------------------------
# TU PRIMERA TOOL  (descomentá las líneas de abajo y completá los huecos)
# --------------------------------------------------------------------------
#
# @grounded_tool
# def mi_primera_tool(consulta: str) -> GroundedResponse:
#     """Describí en una frase qué responde esta tool."""
#
#     # 1) Si la consulta cae FUERA de tu dominio, no inventes: devolvé not_found.
#     if "palabra_que_no_corresponde" in consulta.lower():
#         return GroundedResponse(answer=None, not_found=True, confidence="alta")
#
#     # 2) Si podés responder, hacelo SIEMPRE citando una fuente con src(...).
#     #    El id ("mi_fuente_ejemplo") tiene que estar declarado en sources.yaml.
#     return GroundedResponse(
#         answer="Tu respuesta jurídica, en lenguaje claro.",
#         sources=[src("mi_fuente_ejemplo")],
#         confidence="media",
#     )
