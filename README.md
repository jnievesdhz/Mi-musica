# Mi música

Un sitio donde llevo registros de mi música en Spotify. Tiene dos partes que se enlazan entre sí con la barra de arriba:

- **Wrapped** (`index.html`): un Wrapped propio con todo lo que he escuchado desde 2019. Arriba puedes elegir el periodo (todos los años o uno en concreto) y toda la página se actualiza: horas escuchadas, artista y canción top, reparto por género, horas por año, top 10 de artistas y canciones, top 5 de discos y un reloj con las horas del día en que más escucho. Al final hay una entrada al análisis de letras.
- **Letras** (`letras.html`): "Las letras de mi música, 2024 a 2026". Es el análisis de qué dicen las canciones y los discos que más escucho, en cinco capítulos, con gráficas interactivas (temas por año con dos lentes, el último año en horas, "Born in Winter" por año y las canciones que dejaron rastro), tablas que se pueden buscar y ordenar, y la fuente de cada lectura al lado de la frase.

## Qué cuenta

La cuenta de Spotify es compartida, así que solo entra mi música: metal, rock pesado afín (Three Days Grace, Fit For Rivals, Breaking Benjamin y similares), Canserbero y algo de electrónica (Infected Mushroom, Zedd, Eiffel 65 y ZEXSING). "Solo" de Overdry y "Pisces" de Jinjer no se cuentan porque las escuchamos los dos.

Los datos van de enero de 2019 al 18 de noviembre de 2026.

## Archivos

- `index.html`: el Wrapped.
- `letras.html`: el análisis de letras. **No se edita a mano**, se genera (ver abajo).
- `data/portadas.js` y `fuente/portadas-letras.json`: enlaces a las portadas de los discos en Spotify. No hay imágenes guardadas en el repo, el navegador carga cada portada desde Spotify y al tocarla se abre la canción en Spotify. Se generan con `portadas.py` del repo Historial-de-reproduccion (`python portadas.py sitio ../Mi-musica`). Después de regenerarlas hay que volver a correr `construir_letras.py`.
- `assets/sitio.css`: colores, letras, barra de navegación y pie que comparten las dos páginas.
- `data/`: los totales que usa el Wrapped, en JSON. `wrapped-data.js` es lo que carga la página. Los `.json` son los mismos datos por separado. Se generan con `actualizar.py` del repo privado Historial-de-reproduccion.
- `fuente/letras.md`: el texto del análisis de letras, en Markdown con algunos bloques en HTML.
- `fuente/letras.plantilla.html`: el diseño y las gráficas de la página de letras.
- `herramientas/construir_letras.py`: une el texto y la plantilla en `letras.html`.

El historial original no está en este repo porque trae datos personales. Para actualizar el Wrapped, sigue los pasos del README de Historial-de-reproduccion.

## Cómo cambiar el análisis de letras

1. Edita el texto en `fuente/letras.md` o el diseño en `fuente/letras.plantilla.html`.
2. Corre `python3 herramientas/construir_letras.py` (necesita el paquete `markdown`). El script avisa si quedó algún guion largo en el texto.
3. Sube `letras.html` junto con los archivos que cambiaste.

Las cifras de las gráficas están escritas dentro de la plantilla, en las funciones `figTemas`, `figUltimo`, `figBiw` y `figRastro`. Si se rehace el análisis con datos nuevos, hay que cambiarlas ahí.
