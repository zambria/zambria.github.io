import re, os
BASE = r"C:\Users\erico\zambria.github.io"
FILES = [os.path.join(BASE, "index.html")] + [
    os.path.join(BASE, "posts", f) for f in [
        "capitulo-1-operacao-prato.html","capitulo-2-operacao-prato.html","capitulo-3-operacao-prato.html",
        "capitulo-4-operacao-prato.html","capitulo-5-operacao-prato.html","capitulo-6-operacao-prato.html",
        "capitulo-7-operacao-prato.html","capitulo-8-operacao-prato.html",
        "capitulo-1-continentes-perdidos.html","capitulo-2-continentes-perdidos.html",
        "capitulo-3-continentes-perdidos.html"]]
OUT = os.path.join(BASE, "logs", "auditor", "probes")
os.makedirs(OUT, exist_ok=True)
n = 0
for p in FILES:
    with open(p, "r", encoding="utf-8") as f:
        c = f.read()
    base = os.path.splitext(os.path.basename(p))[0]
    scripts = re.findall(r'<script[^>]*>(.*?)</script>', c, re.S)
    for i, s in enumerate(scripts):
        tmp = os.path.join(OUT, f"{base}_{i}.js")
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(s)
        n += 1
print(f"scripts extraídos: {n} em {OUT}")
