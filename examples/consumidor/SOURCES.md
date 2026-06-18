# Procedencia de las fuentes — ejemplo "consumidor"

Acá anotamos de dónde sale cada fuente declarada en `sources.yaml` y qué falta
verificar. La regla del template: **no inventamos URLs ni citas**. Si una URL no
está verificada, queda en blanco y se anota como pendiente acá abajo.

## Fuentes

### `ldc_art_4` — Información al consumidor

- **Norma:** Ley 24.240 (Ley de Defensa del Consumidor), artículo 4.
- **Tema:** obligación del proveedor de informar de forma cierta, clara y
  detallada las características esenciales de bienes y servicios.
- **URL oficial:** ⚠️ **pendiente de verificar.** Falta confirmar la URL del
  texto actualizado de la Ley 24.240 en InfoLEG y pegar el enlace exacto al
  artículo. Hasta entonces el campo `url` queda vacío en `sources.yaml`.

### `ldc_art_11` — Garantía legal

- **Norma:** Ley 24.240 (Ley de Defensa del Consumidor), artículo 11.
- **Tema:** garantía legal por defectos o vicios en cosas muebles no
  consumibles.
- **URL oficial:** ⚠️ **pendiente de verificar.** Mismo caso que arriba: falta
  confirmar y pegar la URL oficial de InfoLEG.

## Cómo verificar una URL (para completar lo pendiente)

1. Buscá el texto actualizado de la Ley 24.240 en el sitio oficial de InfoLEG.
2. Confirmá que el artículo y su contenido coinciden con la cita.
3. Pegá la URL en el campo `url:` de la fuente en `sources.yaml`.
4. Sacá el ⚠️ de este archivo y dejá anotada la fecha de verificación.
