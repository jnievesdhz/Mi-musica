# Mi música

Una página donde llevo registros de mi música en Spotify: un Wrapped propio con todo lo que he escuchado desde 2019.

Abre `index.html` en el navegador para verla. Arriba puedes elegir el periodo (todos los años o uno en concreto) y toda la página se actualiza: horas escuchadas, artista y canción top, reparto por género, horas por año, top 10 de artistas y canciones, top 5 de discos y un reloj con las horas del día en que más escucho.

## Qué cuenta

La cuenta de Spotify es compartida, así que solo entra mi música: metal, rock pesado afín (Three Days Grace, Fit For Rivals, Breaking Benjamin y similares), Canserbero y algo de electrónica (Infected Mushroom, Zedd, Eiffel 65 y ZEXSING). "Solo" de Overdry y "Pisces" de Jinjer no se cuentan porque las escuchamos los dos.

Los datos van de enero de 2019 al 18 de noviembre de 2026.

## Archivos

- `index.html`: la página.
- `data/`: los totales que usa la página, en JSON. `wrapped-data.js` es lo que carga la página. Los `.json` son los mismos datos por separado.
- Los datos se generan con `actualizar.py` del repo privado Historial-de-reproduccion.

El historial original no está en este repo porque trae datos personales. Para actualizar la página, sigue los pasos del README de Historial-de-reproduccion.
