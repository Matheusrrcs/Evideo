from __future__ import annotations

import base64
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
import urllib.request
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "app" / "src" / "main" / "assets"
MEDIA = ASSETS / "media"
PHOTO_REPO = ROOT / ".cache" / "free-exercise-db"
VIDEO_REPO = ROOT / ".cache" / "free-exercise-db-with-videos"

CONFIG = {
    "hip_thrust": {
        "photo": ["Barbell Hip Thrust", "Hip Thrust"],
        "video": ["Hip Thrust", "Bridge Pose"],
        "exact": False,
    },
    "leg_press": {
        "photo": ["Leg Press"],
        "video": ["Close Feet Leg Press", "Leg Press"],
        "exact": True,
    },
    "abductor": {
        "photo": ["Thigh Abductor", "Hip Abduction"],
        "video": ["Band Hip Abduction", "Hip Abduction"],
        "exact": False,
    },
    "leg_extension": {
        "photo": ["Leg Extensions", "Leg Extension"],
        "video": ["Band Seated Leg Extension", "Leg Extension"],
        "exact": False,
    },
    "lateral_raise": {
        "photo": ["Machine Lateral Raise", "Side Lateral Raise"],
        "video": ["Cable Lateral Raise", "Dumbbell Lateral Raise"],
        "exact": False,
    },
    "shoulder_press": {
        "photo": ["Machine Shoulder Military Press", "Leverage Shoulder Press"],
        "video": ["Dumbbell Alternating Shoulder Press", "Dumbbell Arnold Press"],
        "exact": False,
    },
    "lying_leg_curl": {
        "photo": ["Lying Leg Curls", "Lying Leg Curl"],
        "video": ["Band Prone Leg Curl", "Prone Leg Curl"],
        "exact": False,
    },
    "seated_leg_curl": {
        "photo": ["Seated Leg Curl", "Lying Leg Curls"],
        "video": ["Seated Leg Curl", "Band Prone Leg Curl"],
        "exact": False,
    },
    "glute_kickback": {
        "photo": ["Standing Hip Extension", "Glute Kickback"],
        "video": ["Band One-Leg Kickback", "Kickback"],
        "exact": False,
    },
    "lat_pulldown": {
        "photo": ["Wide-Grip Lat Pulldown", "Wide Grip Lat Pulldown"],
        "video": ["Cable Pulldown", "Cable Close Grip Lat Pulldown"],
        "exact": False,
    },
    "chest_supported_row": {
        "photo": ["Dumbbell Incline Row", "Chest Supported Row"],
        "video": ["Dumbbell Incline Row", "Dumbbell Hammer Grip Incline Bench Row"],
        "exact": False,
    },
    "rear_delt": {
        "photo": ["Reverse Machine Flyes", "Reverse Flyes"],
        "video": ["Cable Crossover Reverse Fly", "Band Bent-Over Rear Lateral Raise"],
        "exact": False,
    },
    "hack_squat": {
        "photo": ["Hack Squat"],
        "video": ["Close Feet Leg Press", "Barbell Front Squat"],
        "exact": False,
    },
    "seated_calf": {
        "photo": ["Seated Calf Raise"],
        "video": ["Seated Calf Raise", "Donkey Calf Raise", "Band Standing Calf Raise"],
        "exact": False,
    },
}


def norm(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def best_match(items: list[dict], candidates: list[str]) -> dict | None:
    if not items:
        return None
    for candidate in candidates:
        c = norm(candidate)
        exact = [x for x in items if norm(x.get("name", "")) == c]
        if exact:
            return exact[0]
    scored = []
    for item in items:
        name = norm(item.get("name", ""))
        aliases = " ".join(norm(a) for a in item.get("aliases", []) if isinstance(a, str))
        hay = f"{name} {aliases}"
        score = max(SequenceMatcher(None, norm(c), name).ratio() for c in candidates)
        for c in candidates:
            words = norm(c).split()
            if words and all(w in hay for w in words):
                score += 0.55
        scored.append((score, item))
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[0][1]


def download(url: str, destination: Path) -> bool:
    destination.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": "TreinoDaBine/4.0"})
    try:
        with urllib.request.urlopen(request, timeout=60) as response, destination.open("wb") as out:
            shutil.copyfileobj(response, out)
        return destination.stat().st_size > 1000
    except Exception as exc:
        print(f"Falha no download {url}: {exc}", file=sys.stderr)
        destination.unlink(missing_ok=True)
        return False


def prepare_video(url: str, destination: Path) -> bool:
    with tempfile.TemporaryDirectory() as td:
        raw = Path(td) / "raw.mp4"
        if not download(url, raw):
            return False
        ffmpeg = shutil.which("ffmpeg")
        if ffmpeg:
            command = [
                ffmpeg, "-y", "-i", str(raw), "-t", "10",
                "-vf", "scale='if(gt(iw,480),480,iw)':-2,fps=24",
                "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "29",
                "-movflags", "+faststart", str(destination),
            ]
            result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if result.returncode == 0 and destination.exists() and destination.stat().st_size > 1000:
                return True
        shutil.copy2(raw, destination)
        return True


def placeholder() -> None:
    # Pequeno JPEG cinza válido para situações em que uma mídia falha.
    jpeg = base64.b64decode(
        "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAP//////////////////////////////////////////////////////////////////////////////////////"
        "2wBDAf//////////////////////////////////////////////////////////////////////////////////////wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAX/"
        "xAAUEAEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIQAxAAAAH/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/9oACAEBAAEFAqf/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/"
        "9oACAEDAQE/Aaf/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oACAECAQE/Aaf/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/9oACAEBAAY/Aqf/xAAUEAEAAAAAAAAA"
        "AAAAAAAAAAAA/9oACAEBAAE/IV//2gAMAwEAAgADAAAAEP/EABQRAQAAAAAAAAAAAAAAAAAAABD/2gAIAQMBAT8QH//EABQRAQAAAAAAAAAAAAAAAAAAABD/"
        "2gAIAQIBAT8QH//EABQQAQAAAAAAAAAAAAAAAAAAABD/2gAIAQEAAT8QH//Z"
    )
    (MEDIA / "placeholder.jpg").write_bytes(jpeg)


def main() -> None:
    MEDIA.mkdir(parents=True, exist_ok=True)
    placeholder()

    photos = json.loads((PHOTO_REPO / "dist" / "exercises.json").read_text(encoding="utf-8"))
    videos = json.loads((VIDEO_REPO / "data" / "exercises.json").read_text(encoding="utf-8"))
    mapping: dict[str, dict] = {}

    for exercise_id, config in CONFIG.items():
        print(f"Preparando {exercise_id}")
        photo_item = best_match(photos, config["photo"])
        video_item = best_match(videos, config["video"])
        entry = {
            "photo1": "media/placeholder.jpg",
            "photo2": "media/placeholder.jpg",
            "thumb": "media/placeholder.jpg",
            "video": "",
            "sourceName": "Mídia não encontrada",
            "exact": bool(config["exact"]),
        }

        if photo_item:
            image_paths = photo_item.get("images") or []
            for index, relative in enumerate(image_paths[:2], start=1):
                source = PHOTO_REPO / "exercises" / relative
                suffix = source.suffix.lower() if source.suffix else ".jpg"
                target = MEDIA / f"{exercise_id}_{index}{suffix}"
                if source.exists():
                    shutil.copy2(source, target)
                    entry[f"photo{index}"] = f"media/{target.name}"
            entry["sourceName"] = photo_item.get("name", entry["sourceName"])

        if video_item:
            video_url = (video_item.get("videos") or {}).get("female") or (video_item.get("videos") or {}).get("male")
            thumb_url = (video_item.get("thumbnails") or {}).get("female") or (video_item.get("thumbnails") or {}).get("male")
            if thumb_url:
                thumb = MEDIA / f"{exercise_id}_thumb.jpg"
                if download(thumb_url, thumb):
                    entry["thumb"] = f"media/{thumb.name}"
            if video_url:
                target_video = MEDIA / f"{exercise_id}.mp4"
                if prepare_video(video_url, target_video):
                    entry["video"] = f"media/{target_video.name}"
            entry["sourceName"] = video_item.get("name", entry["sourceName"])

        if entry["thumb"].endswith("placeholder.jpg"):
            entry["thumb"] = entry["photo1"]
        mapping[exercise_id] = entry

    notice = {
        "photoSource": "yuhonas/free-exercise-db (Unlicense / domínio público)",
        "videoSource": "arhxam/free-exercise-db-with-videos (vídeos demonstrativos)",
    }
    payload = "window.MEDIA_MAP=" + json.dumps(mapping, ensure_ascii=False, separators=(",", ":")) + ";\n"
    payload += "window.MEDIA_CREDITS=" + json.dumps(notice, ensure_ascii=False) + ";\n"
    (ASSETS / "media-map.js").write_text(payload, encoding="utf-8")
    (ASSETS / "MEDIA_LICENSES.txt").write_text(
        "Fotos: Free Exercise DB, Unlicense. https://github.com/yuhonas/free-exercise-db\n"
        "Vídeos: Free Exercise DB with Videos. https://github.com/arhxam/free-exercise-db-with-videos\n"
        "As demonstrações podem mostrar variações próximas quando não há a mesma máquina da ficha.\n",
        encoding="utf-8",
    )
    print(json.dumps(mapping, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
