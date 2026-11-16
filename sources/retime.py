#!/usr/bin/env python3
"""Recale un clip lip-sync sur la voix off d'origine (gratuit, sans régénération).

Le modèle (MiniMax) réécrit l'audio du clip et étire certains passages : les lèvres suivent SON audio,
pas le nôtre. On aligne l'audio du clip sur la voix d'origine par DTW (spectres), puis on rééchantillonne
les images du clip le long de cette correspondance.

Usage : python3 retime.py voix.wav clip.mp4 sortie.mp4
Affiche la corrélation d'enveloppe avant / après.
"""
import os, shutil, subprocess, sys, tempfile
import numpy as np
from scipy.signal import stft
from scipy.ndimage import median_filter

SR, HOP = 16000, 160          # 10 ms par trame audio


def load(path, video=False):
    cmd = ["ffmpeg", "-v", "error", "-i", path] + (["-vn"] if video else []) + ["-ac", "1", "-ar", str(SR), "-f", "s16le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.int16).astype(np.float32) / 32768


def feats(x):
    _, _, Z = stft(x, SR, nperseg=400, noverlap=400 - HOP)
    P = np.abs(Z) ** 2
    edges = np.unique(np.geomspace(2, P.shape[0] - 1, 30).astype(int))      # bandes log, ~mel
    B = np.stack([P[a:b].sum(0) for a, b in zip(edges[:-1], edges[1:])])
    L = np.log(B + 1e-8)
    energy = L.mean(0)
    L = L - L.mean(1, keepdims=True)
    L = L / (np.linalg.norm(L, axis=0, keepdims=True) + 1e-8)
    return L.T, energy


def dtw(A, B, band=60):
    """DTW avec pente bornée (pas (1,1), (1,2), (2,1)) : pas de figeage ni d'accélération extrême."""
    n, m = len(A), len(B)
    C = 1 - A @ B.T
    D = np.full((n + 1, m + 1), np.inf); D[0, 0] = 0
    ratio = m / n
    for i in range(1, n + 1):
        c = int(i * ratio)
        for j in range(max(1, c - band), min(m, c + band) + 1):
            best = D[i - 1, j - 1]
            if i >= 2 and D[i - 2, j - 1] < best: best = D[i - 2, j - 1]
            if j >= 2 and D[i - 1, j - 2] < best: best = D[i - 1, j - 2]
            D[i, j] = C[i - 1, j - 1] + best
    i, j, path = n, m, []
    if not np.isfinite(D[n, m]):
        j = int(np.argmin(D[n]))
    while i > 0 and j > 0:
        path.append((i - 1, j - 1))
        cand = [(D[i - 1, j - 1], i - 1, j - 1)]
        if i >= 2: cand.append((D[i - 2, j - 1], i - 2, j - 1))
        if j >= 2: cand.append((D[i - 1, j - 2], i - 1, j - 2))
        _, i, j = min(cand)
    return path[::-1]


def corr(a, b):
    a = a - a.mean(); b = b - b.mean()
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9))


def main(voice, clip, out):
    v, c = load(voice), load(clip, video=True)
    FA, EA = feats(v); FB, EB = feats(c)
    n = min(len(EA), len(EB))
    print(f"corrélation avant : {corr(EA[:n], EB[:n]):.2f}")
    path = dtw(FA, FB)
    m = np.zeros(len(FA))
    for i, j in path:
        m[i] = j
    m = np.maximum.accumulate(median_filter(m, 9))          # monotone, lissé
    m = np.convolve(np.pad(m, 6, mode="edge"), np.ones(13) / 13, "valid")
    print(f"corrélation après : {corr(EA[:len(m)], EB[np.clip(m.round().astype(int), 0, len(EB) - 1)]):.2f}")
    dev = (m - np.arange(len(m))) * HOP / SR
    print(f"écart max : {np.abs(dev).max():.2f} s")
    # images : 24 i/s sur la durée de la voix
    fps = float(eval(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=r_frame_rate",
                                      "-of", "csv=p=0", clip], capture_output=True, text=True).stdout.strip()))
    tmp = tempfile.mkdtemp()
    subprocess.run(["ffmpeg", "-v", "error", "-i", clip, os.path.join(tmp, "f%05d.png")], check=True)
    frames = sorted(os.listdir(tmp))
    dur = len(v) / SR
    lst = os.path.join(tmp, "list.txt")
    with open(lst, "w") as fh:
        for k in range(int(round(dur * fps))):
            t = k / fps
            ct = np.interp(t, np.arange(len(m)) * HOP / SR, m * HOP / SR)
            idx = min(len(frames) - 1, int(round(ct * fps)))
            fh.write(f"file '{frames[idx]}'\nduration {1 / fps:.6f}\n")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-r", f"{fps}", "-c:v", "libx264", "-crf", "15",
                    "-preset", "slow", "-pix_fmt", "yuv420p", "-an", out], check=True)
    shutil.rmtree(tmp)
    print("ok", out, f"{dur:.2f} s")


if __name__ == "__main__":
    main(*sys.argv[1:4])
