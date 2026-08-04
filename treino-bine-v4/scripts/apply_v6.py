from pathlib import Path
import base64
import gzip
import re

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "app" / "src" / "main" / "assets"
BUILD = ROOT / "app" / "build.gradle"
CHUNKS = ROOT / "scripts" / "v6_chunks"

parts = sorted(CHUNKS.glob("part_*.txt"))
if not parts:
    raise RuntimeError("Nenhuma parte da interface v6 foi encontrada")

encoded = "".join(part.read_text(encoding="utf-8").strip() for part in parts)
html = gzip.decompress(base64.b64decode(encoded))

ASSETS.mkdir(parents=True, exist_ok=True)
(ASSETS / "index.html").write_bytes(html)

build_text = BUILD.read_text(encoding="utf-8")
build_text = re.sub(r"versionCode\s+\d+", "versionCode 6", build_text)
build_text = re.sub(r"versionName\s+'[^']+'", "versionName '6.0'", build_text)
BUILD.write_text(build_text, encoding="utf-8")

print(f"Treino da Bine v6 aplicado: {len(html)} bytes")
