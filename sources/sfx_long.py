#!/usr/bin/env python3
"""Piste de bruitages de la version longue, mixée avec voix + musique dans mix_L.wav."""
import json, os, subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
SFX = os.path.join(ROOT, "sfx_lib")
words = json.load(open(os.path.join(ROOT, "src", "transcript_L.json")))
s = lambda i: words[i]["start"]

CLICK, WHOOSH, POP, PING = "sfx_001.mp3", "sfx_002.mp3", "sfx_003.mp3", "sfx_004.mp3"
M3, M5 = s(69) - 0.1, 48.85
events = [
    # transitions
    (WHOOSH, 3.95, 0.30), (WHOOSH, s(34) - 0.1, 0.30), (WHOOSH, 18.78, 0.28), (WHOOSH, M3, 0.30),
    (WHOOSH, 34.78, 0.28), (WHOOSH, 40.98, 0.28), (WHOOSH, M5, 0.32),
    # contrats qui tombent, curseur, sticker
    (POP, 4.4, 0.45), (POP, 5.0, 0.45), (POP, 5.7, 0.45), (POP, 6.4, 0.45),
    (CLICK, s(31) + 0.35, 0.55), (POP, s(33), 0.6),
    # relevé : frais entourés, cadenas
    (POP, s(46) + 0.1, 0.5), (CLICK, s(51) + 0.15, 0.6), (CLICK, s(52), 0.5),
    # bascule en banque + coches
    (CLICK, M3 + 0.6, 0.65), (POP, s(69), 0.45), (POP, s(72), 0.45), (POP, s(75), 0.45),
    # alerte + écart
    (PING, s(85), 0.4), (POP, s(101) + 0.1, 0.5),
    # pastilles du CTA face caméra
    (POP, s(138), 0.45), (POP, s(140), 0.45),
    # carte de fin : créneau puis tap sur le bouton
    (CLICK, M5 + 1.1, 0.5), (CLICK, M5 + 1.35, 0.6), (CLICK, M5 + 1.8, 0.85),
]

inputs, chains, labels = [], [], []
for k, (f, t, vol) in enumerate(events):
    inputs += ["-i", os.path.join(SFX, f)]
    ms = int(round(t * 1000))
    chains.append(f"[{k}]aresample=48000,volume={vol},adelay={ms}|{ms}[e{k}]")
    labels.append(f"[e{k}]")
filt = ";".join(chains) + f";{''.join(labels)}amix=inputs={len(events)}:normalize=0,apad=whole_len={52 * 48000},atrim=0:52[out]"
out = os.path.join(ROOT, "src", "assets", "sfx_L.wav")
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *inputs, "-filter_complex", filt,
                "-map", "[out]", "-ac", "2", "-ar", "48000", out], check=True)
print("ok", out, len(events), "events")
