"""Verify the static GitHub Pages entry point and its configuration resources."""
from pathlib import Path
from html.parser import HTMLParser
import json

root = Path(__file__).resolve().parents[1] / "web"
class Assets(HTMLParser):
    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key not in ("href", "src") or not value or value.startswith(("http:", "https:", "data:", "#")):
                continue
            relative = value.split("?", 1)[0].split("#", 1)[0]
            assert not relative.startswith("/"), f"Root-relative URL breaks project Pages: {value}"
            assert (root / relative).exists(), f"Missing asset: {value}"
Assets().feed((root / "index.html").read_text())
manifest = json.loads((root / "config/manifest.json").read_text())
for file in manifest["scripts"]:
    assert (root / file).is_file(), f"Missing script: {file}"
for file in manifest["resources"].values():
    json.loads((root / "config" / file).read_text())
print("Static site and configuration resources are complete.")
