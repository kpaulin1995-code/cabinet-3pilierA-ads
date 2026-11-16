import re, subprocess, sys
def tighten(src, out, keep=0.28, tempo=1.0, thr="-40dB", d="0.3"):
    err = subprocess.run(["ffmpeg","-hide_banner","-i",src,"-af",f"silencedetect=n={thr}:d={d}","-f","null","-"],capture_output=True,text=True).stderr
    st=[float(x) for x in re.findall(r"silence_start: ([0-9.]+)",err)]; en=[float(x) for x in re.findall(r"silence_end: ([0-9.]+)",err)]
    dur=float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",src],capture_output=True,text=True).stdout)
    segs=[]; cur=0.0
    for s,e in zip(st,en):
        if s<0.05: cur=max(0,e-0.05); continue
        if e>=dur-0.05: segs.append((cur,s+0.05)); cur=None; break
        segs.append((cur,s+keep/2)); cur=e-keep/2
    if cur is not None: segs.append((cur,dur))
    f=";".join(f"[0]atrim={a:.3f}:{b:.3f},asetpts=N/SR/TB[s{i}]" for i,(a,b) in enumerate(segs))+";"+"".join(f"[s{i}]" for i in range(len(segs)))+f"concat=n={len(segs)}:v=0:a=1"+(f",atempo={tempo}" if tempo!=1 else "")+"[o]"
    subprocess.run(["ffmpeg","-v","error","-y","-i",src,"-filter_complex",f,"-map","[o]","-ar","48000","-ac","1",out],check=True)
tighten("../pilier/voix_Algenib.wav","intro_t.wav",keep=0.45,tempo=1.0)
tighten("suite_b.wav","suite_t.wav",keep=0.3,tempo=1.07)
