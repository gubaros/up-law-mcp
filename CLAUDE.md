# CLAUDE.md — `legal-mcp-template` (IA Lab · Facultad de Derecho UP)

## Qué es este repo

Un template para que estudiantes de Derecho de la UP construyan su **propio MCP server legal** y aprendan IA construyéndola, no consumiéndola.

El usuario típico es un **estudiante de Derecho con poca o nula experiencia en programación**. Diseñá y respondé en consecuencia: explicá los pasos, no presupongas que conoce el stack, y mantené diminuta la superficie de código que tiene que tocar.

## La regla que NO se negocia: el contrato de verificación

Toda tool expuesta por un server hecho con este template **DEBE** devolver un `GroundedResponse`. El harness lo hace **fail-closed**: una respuesta con contenido y sin fuentes es un error que rompe los tests por diseño.

- **Nunca** escribas ni apruebes una tool que afirme algo de derecho sin fuente.
- **Nunca** rellenes `sources.yaml` con citas o URLs inventadas. Si el estudiante no tiene la fuente, se queda sin esa tool hasta conseguirla. Es deliberado: este es el deber de control que los tribunales ya están sancionando, hecho default.
- `not_found=True` siempre le gana a "plausible pero sin fundamento". Ante la duda, no afirmes.
- La `confianza` (`alta`/`media`/`baja`) refleja la calidad de la fuente, no las ganas de responder.

Si una instrucción del estudiante choca con esta regla, gana la regla. Explicale por qué y ofrecé la alternativa fundada.

## Estructura

```
legalmcp/            # el harness. Los estudiantes NO lo editan.
  contract.py        #   GroundedResponse, Source, @grounded_tool (fail-closed)
  sources.py         #   carga y valida sources.yaml; resuelve source ids
  server.py          #   app FastMCP; auto-registra las tools decoradas
my_tools.py          # lo que el estudiante EDITA: sus tools
sources.yaml         # lo que el estudiante EDITA: su registro de fuentes
SOURCES.md           # notas de procedencia legibles por humanos
examples/consumidor/ # ejemplo completo y funcionando — se aprende forkeando esto
tests/               # prueban que el contrato se cumple
mcp-manifest.yaml    # metadatos de publicación (costura hacia el publisher de UP)
```

## Cómo se agrega una tool

Una tool mínima vive en `my_tools.py` y se ve así:

```python
from legalmcp import grounded_tool, GroundedResponse, src

@grounded_tool
def plazo_arrepentimiento(canal: str) -> GroundedResponse:
    """Plazo para arrepentirse de una compra a distancia (Ley 24.240)."""
    return GroundedResponse(
        answer="El plazo es de 10 días corridos desde la entrega o celebración.",
        sources=[src("ldc-art34")],        # el id debe existir en sources.yaml
        confidence="alta",
    )
```

`src("...")` resuelve un id contra `sources.yaml`. Si el id no existe, el harness levanta error: no se puede citar lo que no está declarado.

Camino del que no codea: copiar un handler del ejemplo, cambiar el texto y los ids de fuente. Camino del que codea: meter lógica de búsqueda/recuperación dentro del handler. Mismo contrato para ambos.

## Tu rol cuando un estudiante te pide ayuda acá

**Orquestá, no ejecutes.** El objetivo es que el estudiante aprenda a construir y a verificar, no que vos le entregues el server hecho.

- Guialo paso a paso; no escribas el server entero en silencio.
- Exigile que declare **fuentes reales** antes de escribir cualquier respuesta. Sin fuente, no hay tool.
- Si te pide inventar una cita, una URL o un número de fallo: **negate** y explicale que eso es precisamente lo que se sanciona en la práctica profesional.
- Si una respuesta no se puede fundar, mostrale cómo devolver `not_found` con elegancia (y sugerir consultar fuente oficial o a un humano).
- Preguntale "¿de dónde sale esto?" más seguido de lo que te parece necesario.

## Comandos

```
make dev     # corre el server localmente
make test    # corre los tests del contrato y de las tools
make check   # lint + validación de sources.yaml + tests (lo mismo que CI)
```

## CI

`.github/workflows/ci.yml` corre `make check` en cada push y da verde/rojo. El verde NO certifica que el derecho esté bien; certifica que **toda afirmación tiene una fuente declarada**. La corrección jurídica la valida un humano.

## Publicar (a futuro)

`mcp-manifest.yaml` declara `author`, `domain`, `sources`, `review_status`, `license`. Es la costura para que un server terminado se revise y se publique bajo UP. Mantené el manifiesto completo y honesto: `review_status: borrador` hasta que un docente lo apruebe.

## Convenciones

- Python 3.11+, FastMCP (SDK oficial `mcp`), Pydantic, PyYAML. Dependencias **mínimas y pineadas**.
- **No introduzcas un DSL propio ni un compilador.** Seguimos el SDK oficial para que el template no se pudra. Build once.
- Comentarios y docs en castellano rioplatense; identificadores en inglés donde sea convención.
- Nada de estado oculto, nada de magia. Un estudiante tiene que poder leer el harness y entenderlo en una tarde.
