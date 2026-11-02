#!/usr/bin/env python3
"""Piste de bruitages de la version longue, mixée avec voix + musique dans mix_L.wav."""
import json, os, subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
SFX = os.path.join(ROOT, "sfx_lib")
words = json.load(open(os.path.join(ROOT, "src", "transcript_A2.json")))
s = lambda i: words[i]["start"]

CLICK, WHOOSH, POP, PING = "sfx_001.mp3", "sfx_002.mp3", "sfx_003.mp3", "sfx_004.mp3"
M3, M5 = s(56) - 0.1, 43.45
events = [
    (WHOOSH, 3.64, 0.30), (WHOOSH, 9.08, 0.26), (WHOOSH, 10.46, 0.30), (WHOOSH, 38.68, 0.26), (WHOOSH, M3, 0.30),
    (WHOOSH, 24.08, 0.28), (WHOOSH, 26.90, 0.30), (WHOOSH, 32.48, 0.28), (WHOOSH, M5, 0.32),
    (POP, 4.2, 0.45), (POP, 4.75, 0.45), (POP, 5.3, 0.45), (POP, 5.85, 0.45),
    (CLICK, s(27) + 0.35, 0.55), (POP, s(29), 0.6),
    (POP, s(48) + 0.1, 0.5), (POP, s(53), 0.45), (CLICK, s(55), 0.6), (CLICK, s(55) + 0.2, 0.5),
    (CLICK, M3 + 0.6, 0.65), (POP, s(58), 0.45), (POP, s(61), 0.45), (POP, s(64), 0.45),
    (PING, s(74), 0.4), (POP, s(83), 0.4), (POP, s(90) + 0.1, 0.5),
    (POP, s(117), 0.45), (POP, s(118), 0.45),
    (CLICK, M5 + 1.1, 0.5), (CLICK, M5 + 1.35, 0.6), (CLICK, M5 + 1.8, 0.85),
]

inputs, chains, labels = [], [], []
for k, (f, t, vol) in enumerate(events):
    inputs += ["-i", os.path.join(SFX, f)]
    ms = int(round(t * 1000))
    chains.append(f"[{k}]aresample=48000,volume={vol},adelay={ms}|{ms}[e{k}]")
    labels.append(f"[e{k}]")
filt = ";".join(chains) + f";{''.join(labels)}amix=inputs={len(events)}:normalize=0,apad=whole_len={int(46.5 * 48000)},atrim=0:46.5[out]"
out = os.path.join(ROOT, "src", "assets", "sfx_AB.wav")
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *inputs, "-filter_complex", filt,
                "-map", "[out]", "-ac", "2", "-ar", "48000", out], check=True)
print("ok", out, len(events), "events")
