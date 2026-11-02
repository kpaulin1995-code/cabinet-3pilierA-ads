# Sources de montage

Tout ce qu'il faut pour refaire un rendu des vidéos avec HyperFrames, sans régénérer les voix ni les clips FLORA.

| Script | Vidéo | Sortie |
|---|---|---|
| `build.py A 916` / `build.py A 45` | Version A (typographique) | `out/A_916`, `out/A_45` |
| `build_soft.py 916` / `45` | Version C (soft 3D) | `out/C_*` |
| `build_long.py 916` / `45` | Long « vendu » | `out/L_*` |
| `build_ab.py 916` / `45` | AB-hookA « Et la banque ? » | `out/AB_*` |

Rendu : `cd out/AB_916 && npx hyperframes@0.8.185 check && npx hyperframes@0.8.185 render -o ../../AB_916.mp4`

## Contenu

- `src/` : gabarits HTML (version A), transcriptions mot à mot (`transcript_*.json`), polices, voix (`voix_*.wav`) et mix finaux (`mix_*.wav` = voix + musique + bruitages).
- `clips/` : clips face caméra FLORA de la version Long (muets au montage).
- `abA/clips/` : clips face caméra de la version AB-hookA (`a_f1` à `a_f6`).
- `abA/` : segments de voix envoyés au lip-sync (`a*.wav`, `b*.wav` avec silence en tête), images clés de la femme (`k*.png`), voix complète et transcription.
- `soft/scenes/` : images des scènes de la version C.
- `sfx_lib/` : bruitages (clic, whoosh, pop, ping) utilisés par `sfx_long.py` et `sfx_ab.py`.
- `musique/` : piste 2 (ElevenLabs minimal) et sa version prolongée `M2_ext52.wav`.

## Refaire un mix (AB)

```
python3 sfx_ab.py   # recrée src/assets/sfx_AB.wav
ffmpeg -i src/assets/voix_A2.wav -i musique/M2_ext52.wav -i src/assets/sfx_AB.wav -filter_complex "
[0]aresample=48000,loudnorm=I=-15:TP=-1.5:LRA=7,apad=pad_dur=4,asplit=2[v][sc];
[1]atrim=0:46.5,asetpts=N/SR/TB,aresample=48000,loudnorm=I=-22:TP=-3:LRA=11,afade=t=in:d=0.3,afade=t=out:st=44:d=2.5[m];
[m][sc]sidechaincompress=threshold=0.03:ratio=6:attack=40:release=450:makeup=1[md];
[v][md][2]amix=inputs=3:duration=longest:normalize=0,alimiter=limit=0.89" -ar 48000 -t 46.5 src/assets/mix_AB.wav
```
