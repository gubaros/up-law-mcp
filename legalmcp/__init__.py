"""legalmcp — el harness fino sobre FastMCP que hace el grounding no-bypasseable.

Todo lo que necesitás como estudiante se importa desde acá::

    from legalmcp import grounded_tool, GroundedResponse, Source, src

- `grounded_tool`: decorador para tus tools.
- `GroundedResponse`: lo que tus tools devuelven.
- `Source`: una fuente citada (la obtenés con `src`).
- `src`: resuelve una fuente declarada en sources.yaml.
- `run`: levanta el servidor (lo usa `make dev`).
"""

from .contract import GroundedResponse, Source, grounded_tool
from .server import run
from .sources import src

__all__ = ["grounded_tool", "GroundedResponse", "Source", "src", "run"]
