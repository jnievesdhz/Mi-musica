"""Genera letras.html a partir de fuente/letras.md y fuente/letras.plantilla.html.

Uso: python3 herramientas/construir_letras.py
"""
import json
import re
from pathlib import Path

import markdown

RAIZ = Path(__file__).resolve().parent.parent
FUENTE = RAIZ / "fuente" / "letras.md"
PLANTILLA = RAIZ / "fuente" / "letras.plantilla.html"
SALIDA = RAIZ / "letras.html"
PORTADAS = RAIZ / "fuente" / "portadas-letras.json"  # lo genera portadas.py del repo Historial-de-reproduccion

NNBSP = " "  # espacio fino que no corta línea, entre número y unidad


def convertir(md_texto: str) -> str:
    html = markdown.markdown(
        md_texto,
        extensions=["tables", "attr_list", "md_in_html"],
        output_format="html5",
    )
    # Enlaces externos: fuente pequeña que abre en otra pestaña
    html = re.sub(
        r'<a href="(https?://[^"]+)">',
        r'<a class="src" href="\1" target="_blank" rel="noopener">',
        html,
    )
    html = re.sub(r'<a href="(#[^"]+)">', r'<a class="int" href="\1">', html)
    # Número y unidad juntos: 52 % y 3,6 h
    html = re.sub(r"(\d) %", lambda m: m.group(1) + NNBSP + "%", html)
    html = re.sub(r"(\d) h\b", lambda m: m.group(1) + NNBSP + "h", html)
    # Tablas con envoltura para desplazamiento horizontal en móvil
    html = html.replace("<table>", '<div class="tabla-scroll"><table>').replace("</table>", "</table></div>")
    return html


def secciones(html: str):
    for m in re.finditer(r'<section class="cap[^"]*"[^>]*>', html):
        attrs = dict(re.findall(r'([\w-]+)="([^"]*)"', m.group(0)))
        yield m, attrs


def indice(html: str) -> str:
    items = []
    for _, a in secciones(html):
        num = a.get("data-num", "")
        items.append(
            f'<li><a href="#{a["id"]}" data-sec="{a["id"]}"><span class="toc-n">{num}</span>'
            f'<span class="toc-t">{a["data-toc"]}</span></a></li>'
        )
    return "\n".join(items)


def titulos_de_capitulo(html: str) -> str:
    # Antepone "Capítulo N" a cada título de capítulo numerado
    partes, pos = [], 0
    for m, a in secciones(html):
        if "data-num" not in a:
            continue
        partes.append(html[pos:m.end()])
        partes.append(f'\n<p class="cap-n">Capítulo {a["data-num"]}</p>')
        pos = m.end()
    partes.append(html[pos:])
    return "".join(partes)


def main():
    cuerpo = convertir(FUENTE.read_text(encoding="utf-8"))
    toc = indice(cuerpo)
    cuerpo = titulos_de_capitulo(cuerpo)
    for ch in "—–":
        if ch in cuerpo:
            raise SystemExit(f"Hay un guion largo ({ch!r}) en el contenido. Cámbialo antes de publicar.")
    pagina = PLANTILLA.read_text(encoding="utf-8")
    portadas = PORTADAS.read_text(encoding="utf-8") if PORTADAS.exists() else "[]"
    portadas = json.dumps(json.loads(portadas), ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    pagina = pagina.replace("{{INDICE}}", toc).replace("{{PORTADAS}}", portadas).replace("{{CONTENIDO}}", cuerpo)
    SALIDA.write_text(pagina, encoding="utf-8")
    print(f"Listo: {SALIDA.relative_to(RAIZ)} ({len(pagina):,} bytes)")


if __name__ == "__main__":
    main()
