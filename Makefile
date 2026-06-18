# Comandos del template. Usá: make dev | make test | make check
#
# PYTHON: por defecto python3. Si usás un entorno virtual, podés sobrescribirlo:
#   make check PYTHON=.venv/bin/python

PYTHON ?= python3

.PHONY: install dev test check lint sources

# Instala el harness y las dependencias de desarrollo (editable).
install:
	$(PYTHON) -m pip install -e ".[dev]"

# Levanta tu servidor MCP (usa el my_tools.py de este directorio).
dev:
	$(PYTHON) -m legalmcp.server

# Corre los tests.
test:
	$(PYTHON) -m pytest

# Valida los sources.yaml del template y del ejemplo.
sources:
	$(PYTHON) -m legalmcp sources.yaml examples/consumidor/sources.yaml

# Lint del código.
lint:
	$(PYTHON) -m ruff check .

# El check completo: lint + validación de fuentes + tests.
# Verde acá = "toda afirmación tiene una fuente declarada". NO certifica
# corrección jurídica.
check: lint sources test
