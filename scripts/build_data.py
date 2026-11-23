# Construye los datasets del Wrapped a partir del historial extendido de Spotify.
# Solo se cuenta la música de José: metal, rock pesado afín, Canserbero y algo de electrónica.
# Se excluyen "Solo" (Overdry) y "Pisces" (Jinjer), que escuchan los dos.
import pandas as pd, json, os
me = pd.read_pickle('/home/claude/me.pkl')
me['anio'] = me.ts.dt.year.astype(str)
me['h'] = me.ms_played / 3.6e6
A, T, AL = 'master_metadata_album_artist_name', 'master_metadata_track_name', 'master_metadata_album_album_name'
code = open(__file__, encoding='utf-8').read()
out = '/home/claude/wrapped'
def save(name, rows, desc):
    meta = [{"label": "build_data.py", "value": code, "type": "code", "lang": "python"},
            {"label": "Entrada", "value": "my_spotify_data.zip (Streaming_History_Audio_*.json)"},
            {"label": "Contenido", "value": desc}]
    json.dump({"rows": rows, "meta": meta}, open(f'{out}/{name}.json', 'w', encoding='utf-8'), ensure_ascii=False)
groups = [('Todos', me)] + [(y, g) for y, g in me.groupby('anio')]
res, art, can, alb, hd = [], [], [], [], []
for y, g in groups:
    q = g[g.ms_played >= 30000]
    ta = g.groupby(A).h.sum().sort_values(ascending=False)
    tc = q.groupby([T, A]).size().sort_values(ascending=False)
    gh = g.groupby('gen').h.sum()
    res.append({"anio": y, "horas": round(g.h.sum(), 1), "artistas": int(g[A].nunique()),
                "canciones": int(g.spotify_track_uri.nunique()), "dias": int(g.ts.dt.date.nunique()),
                "horas_metal": round(gh.get('Metal', 0), 1), "horas_rock": round(gh.get('Rock pesado', 0), 1),
                "horas_rap": round(gh.get('Rap', 0), 1), "horas_electronica": round(gh.get('Electrónica', 0), 1),
                "artista_top": ta.index[0], "cancion_top": tc.index[0][0], "cancion_top_artista": tc.index[0][1]})
    for i, (a, v) in enumerate(ta.head(10).items(), 1):
        art.append({"id": f"{y}-{i:02d}", "anio": y, "puesto": i, "artista": a, "horas": round(v, 1)})
    for i, ((t, a), v) in enumerate(tc.head(10).items(), 1):
        can.append({"id": f"{y}-{i:02d}", "anio": y, "puesto": i, "cancion": t, "artista": a, "reproducciones": int(v)})
    tb = g.groupby([AL, A]).h.sum().sort_values(ascending=False)
    for i, ((al, a), v) in enumerate(tb.head(5).items(), 1):
        alb.append({"id": f"{y}-{i:02d}", "anio": y, "puesto": i, "album": al, "artista": a, "horas": round(v, 1)})
    hh = g.groupby(g.ts.dt.hour).h.sum().reindex(range(24), fill_value=0)
    for h, v in hh.items():
        hd.append({"id": f"{y}-{h:02d}", "anio": y, "hora": int(h), "horas": round(v, 1)})
save('resumen', res, 'Totales por año (y "Todos"): horas, artistas, canciones, días, % de saltos, horas por género, artista y canción top.')
save('artistas', art, 'Top 10 artistas por horas, por año y en total.')
save('canciones', can, 'Top 10 canciones por reproducciones de 30 s o más, por año y en total.')
save('albumes', alb, 'Top 5 álbumes por horas, por año y en total.')
save('horas_dia', hd, 'Horas escuchadas por hora del día (hora de Bogotá), por año y en total.')
print(json.dumps(res, ensure_ascii=False, indent=0)[:1500])
for f in os.listdir(out): print(f, os.path.getsize(f'{out}/{f}'))
