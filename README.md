# legal-mcp-template

**IA Lab · Facultad de Derecho — Universidad de Palermo (UP)**

Una herramienta para que estudiantes de Derecho construyan su **propio conector
MCP legal** y aprendan IA construyéndola, no consumiéndola.

Un conector MCP (Model Context Protocol) es un programa que le da herramientas a
un asistente de IA como Claude. Este template te deja construir el tuyo: un
servidor que responde consultas jurídicas y que, **por construcción, no puede
afirmar nada del derecho sin citar la fuente**. Si una respuesta no tiene
fundamento declarado, el programa se rompe a propósito.

Esa disciplina —el *grounding*— es justamente lo que **reduce el riesgo de
alucinación**: el asistente no puede "inventar" una norma o un fallo, porque toda
afirmación viaja con su cita o no sale. Es el deber de control que los tribunales
ya están exigiendo, convertido en el comportamiento por defecto.

No hace falta saber programar. Vas a tocar **dos archivos** nada más:
`my_tools.py` (tus respuestas) y `sources.yaml` (tus fuentes).

> **Qué certifica el check (y qué no).** Cuando `make check` da verde, eso
> significa **"toda afirmación tiene una fuente declarada"**. **No** significa que
> el contenido jurídico sea correcto: eso lo revisa un humano. El verde es sobre
> la disciplina de citar, no sobre el derecho.

---

## Instalación

Necesitás **Python 3.11 o más nuevo**. Elegí tu sistema operativo.

### La forma más fácil: GitHub Codespaces (sin instalar nada)

Desde GitHub: botón **Code → Codespaces → Create codespace**. El entorno se arma
solo y corre `make check` al final. Si lo viste terminar en verde, ya está todo
listo y podés saltar a [Construí tu propio conector](#construí-tu-propio-conector).

### macOS

1. **Python.** Verificá que tengas 3.11+:
   ```bash
   python3 --version
   ```
   Si no lo tenés, instalalo desde [python.org](https://www.python.org/downloads/)
   o con [Homebrew](https://brew.sh): `brew install python`.

2. **Herramientas de compilación** (para `make`). Si nunca las instalaste:
   ```bash
   xcode-select --install
   ```

3. **Descargá el proyecto y entrá a la carpeta:**
   ```bash
   git clone <URL-del-repo> legal-mcp-template
   cd legal-mcp-template
   ```

4. **Creá un entorno virtual e instalá** (en Mac conviene siempre usar un venv):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   make install
   ```

5. **Comprobá que todo funciona:**
   ```bash
   make check
   ```
   Tiene que terminar en verde.

> Cada vez que vuelvas a trabajar, reactivá el entorno con
> `source .venv/bin/activate` desde la carpeta del proyecto.

### Windows

1. **Python.** Instalalo desde [python.org](https://www.python.org/downloads/) y,
   en el instalador, **tildá "Add Python to PATH"**. Verificá en PowerShell:
   ```powershell
   py --version
   ```

2. **Descargá el proyecto y entrá a la carpeta:**
   ```powershell
   git clone <URL-del-repo> legal-mcp-template
   cd legal-mcp-template
   ```

3. **Creá un entorno virtual e instalá:**
   ```powershell
   py -m venv .venv
   .venv\Scripts\activate
   pip install -e ".[dev]"
   ```

4. **Comprobá que todo funciona.** Windows no trae `make`, así que corré los tres
   pasos a mano (es exactamente lo que hace `make check`):
   ```powershell
   python -m ruff check .
   python -m legalmcp sources.yaml examples\consumidor\sources.yaml
   python -m pytest
   ```
   Los tres tienen que pasar.

> ¿Querés usar `make` en Windows? Podés instalarlo con
> [Scoop](https://scoop.sh) (`scoop install make`) o
> [Chocolatey](https://chocolatey.org) (`choco install make`). No es obligatorio.

---

## Probá el ejemplo

El proyecto trae un conector **completo y funcionando** sobre derechos del
consumidor (Ley 24.240). Con el entorno activado:

```bash
cd examples/consumidor
python -m legalmcp.server
```

(Esto levanta el servidor; cortalo con `Ctrl+C`.) Abrí
`examples/consumidor/my_tools.py`: son dos tools cortas, comentadas línea por
línea. Fijate cómo una de ellas, cuando la consulta cae fuera de su tema,
devuelve `not_found=True` en vez de inventar una respuesta. Ese es el patrón.

### Conectarlo a Claude Desktop

Para usar tu conector dentro de la app **Claude Desktop**, editá su archivo de
configuración:

- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

El archivo debe contener **solo** la clave `mcpServers` en el nivel superior.
Reemplazá `/ruta/a/legal-mcp-template` por la ruta real donde clonaste el
proyecto.

**macOS:**
```json
{
  "mcpServers": {
    "consumidor": {
      "command": "/bin/sh",
      "args": [
        "-c",
        "cd /ruta/a/legal-mcp-template/examples/consumidor && exec /ruta/a/legal-mcp-template/.venv/bin/legal-mcp"
      ]
    }
  }
}
```

**Windows:**
```json
{
  "mcpServers": {
    "consumidor": {
      "command": "cmd",
      "args": [
        "/c",
        "cd /d C:\\ruta\\a\\legal-mcp-template\\examples\\consumidor && C:\\ruta\\a\\legal-mcp-template\\.venv\\Scripts\\legal-mcp.exe"
      ]
    }
  }
}
```

Guardá, **cerrá Claude Desktop por completo y volvé a abrirlo**. Vas a ver las
tools del conector disponibles. Probá: *"¿qué garantía tengo si compro algo y
sale fallado?"* — debería citarte el artículo correspondiente.

> El `cd` del comando es necesario porque Claude lanza el servidor desde una
> carpeta cualquiera, y el servidor busca `my_tools.py` y `sources.yaml` en el
> directorio actual.

---

## Construí tu propio conector

### 1. Copiá una tool a tu `my_tools.py` y cambiale el texto

Abrí el `my_tools.py` de la raíz. Tiene una tool de ejemplo comentada.
Descomentala (sacale los `#`), poné tu propia respuesta jurídica en `answer` y
elegí un id de fuente para citar. Guiate por el ejemplo de consumidor.

La regla que no podés saltear: si escribís una respuesta en `answer`, **tenés
que** citar al menos una fuente con `src("...")`. Si no encontrás fundamento,
devolvé `GroundedResponse(not_found=True)`.

### 2. Declará tu fuente en `sources.yaml`

`src("mi_fuente")` solo funciona si `mi_fuente` está declarada en `sources.yaml`.
Abrí `sources.yaml`, copiá el bloque de ejemplo y completá la `cita`. Si tenés la
URL oficial verificada, ponela; si no, **dejala vacía** y anotala como pendiente
en `SOURCES.md`. **Nunca inventes una URL.**

### 3. `make check` en verde

```bash
make check
```

(En Windows, los tres comandos de la sección de instalación.) Esto corre el
linter, la validación de tus fuentes y los tests. Si citaste una fuente que no
declaraste, o escribiste una respuesta sin fuente, queda en rojo. Arreglalo hasta
que dé verde.

### 4. Completá el manifiesto

Abrí `mcp-manifest.yaml` y poné tu nombre, tu dominio y la lista de ids de
fuentes que usás. Dejá `review_status: borrador` hasta que un humano revise el
contenido jurídico.

¡Listo! Tenés un conector MCP legal con grounding garantizado.

---

## Cómo está armado (para curiosos)

```
.
├── my_tools.py          ← TU código (lo editás vos)
├── sources.yaml         ← TUS fuentes (las declarás vos)
├── SOURCES.md           ← de dónde sale cada fuente
├── mcp-manifest.yaml    ← metadatos de tu conector
├── legalmcp/            ← el harness (NO se toca)
│   ├── contract.py      ← GroundedResponse, Source, @grounded_tool (fail-closed)
│   ├── sources.py       ← carga/valida sources.yaml; src(id) resuelve o se rompe
│   └── server.py        ← arma el server FastMCP y registra tus tools
├── tests/               ← prueban que el contrato sirve
└── examples/consumidor/ ← ejemplo completo y forkeable
```

El harness es fino y se apoya **directo en el SDK oficial de MCP (FastMCP)**: no
hay lenguaje propio ni compilador que se pueda pudrir cuando el SDK evolucione.

### Comandos

| Comando | Qué hace |
|---|---|
| `make install` | Instala el harness y las dependencias |
| `make dev` | Levanta tu servidor MCP |
| `make test` | Corre los tests |
| `make check` | Linter + validación de fuentes + tests (lo que mira CI) |

---

## Seguridad

¿Encontraste una vulnerabilidad? Por favor reportala **en privado** antes de
divulgarla. Mirá [SECURITY.md](SECURITY.md) — el contacto es
**gbarosio@gmail.com**.

## Autores

- Guido Barosio
- Juan Cruz Romano
- Hernán Quadri
- Aníbal Ramírez

## Licencia

Distribuido bajo la licencia **BSD 3-Clause**. Ver [LICENSE](LICENSE).
