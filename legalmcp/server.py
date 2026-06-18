"""Construye el servidor MCP sobre el SDK oficial (FastMCP) y lo corre.

Acá no hay magia ni DSL propio: usamos FastMCP directo. Este archivo importa tu
`my_tools.py` (lo que dispara el registro de tus tools decoradas con
`@grounded_tool`) y las engancha al servidor.

Vos NO editás este archivo. Lo corrés con `make dev`.
"""

from __future__ import annotations

import os
import sys

from mcp.server.fastmcp import FastMCP

from .contract import _REGISTRY


def build_app(name: str = "legal-mcp") -> FastMCP:
    """Crea la app FastMCP y registra todas las tools de tu `my_tools.py`."""
    app = FastMCP(name)

    # Buscamos tu my_tools.py en el directorio actual (CWD), sin importar desde
    # dónde se haya lanzado el server (un cliente como Claude lo lanza solo).
    cwd = os.getcwd()
    if cwd not in sys.path:
        sys.path.insert(0, cwd)

    # Importar my_tools ejecuta su código, y cada @grounded_tool se agrega
    # al _REGISTRY.
    import my_tools  # noqa: F401  (el import es por su efecto: registrar tools)

    for fn in _REGISTRY:
        # app.tool() es el decorador oficial de FastMCP. Le pasamos cada tool
        # ya envuelta por @grounded_tool (que conserva nombre y docstring).
        app.tool()(fn)

    return app


def run() -> None:
    """Levanta el servidor MCP. Es lo que ejecuta `make dev`."""
    build_app().run()


if __name__ == "__main__":
    run()
