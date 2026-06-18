"""CLI del harness: `python -m legalmcp <archivo.yaml> [...]`.

Valida cada `sources.yaml` indicado (por defecto, ./sources.yaml). Sale con
código distinto de cero si alguno es inválido. Lo invoca `make check`.
"""

from __future__ import annotations

import sys

from .sources import validate_sources


def main() -> int:
    rutas = sys.argv[1:] or ["sources.yaml"]
    hubo_error = False
    for ruta in rutas:
        try:
            ids = validate_sources(ruta)
        except (FileNotFoundError, ValueError) as e:
            print(f"✗ {ruta}: {e}")
            hubo_error = True
        else:
            print(f"✓ {ruta}: {len(ids)} fuente(s) declarada(s): {', '.join(ids)}")
    return 1 if hubo_error else 0


if __name__ == "__main__":
    sys.exit(main())
