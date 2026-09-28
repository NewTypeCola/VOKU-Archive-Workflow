"""Read-only checks for the public review assets, linked images and document links."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import hashlib
import json
import re

APP = Path(__file__).resolve().parents[1]
WORKFLOW = APP.parents[1]
ROOT = WORKFLOW.parent
errors = []
counts = {"sample_pages": 0, "images": 0, "local_links": 0, "app_text_files": 0}


def check_link(source, ref):
    parts = urlsplit(ref.strip("<>"))
    if parts.scheme or ref.startswith("//"):
        return
    counts["local_links"] += 1
    target = (source.parent / unquote(parts.path)).resolve() if parts.path else source
    if not target.is_relative_to(ROOT) or not target.is_file():
        errors.append(f"Missing local link: {source.name}: {ref}")


class Links(HTMLParser):
    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in {"href", "src"}:
                if value.startswith("/"):
                    errors.append("Root-relative HTML asset: " + value)
                check_link(APP / "index.html", value)


Links().feed((APP / "index.html").read_text())
for source in [ROOT / "README.md", WORKFLOW / "README.md", WORKFLOW / "demo.md", WORKFLOW / "pipeline.md", APP / "README.md", APP / "VERIFICATION.md"]:
    for ref in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", source.read_text()):
        check_link(source, ref)

catalog = json.loads((APP / "samples.json").read_text())
assert catalog["sample"] is True
assert {row["year"] for row in catalog["pages"]} == {"1994", "2003", "2017"}
assert len({row["page_id"] for row in catalog["pages"]}) == len(catalog["pages"]) == 8
for row in catalog["pages"]:
    counts["sample_pages"] += 1
    for view, ref in row["images"].items():
        check_link(APP / "samples.json", ref)
        image = (APP / ref).resolve()
        assert image.is_relative_to(WORKFLOW / "assets/demo")
        expected = row["safe_sha256"] if view == "before" else row["sha256"]
        assert hashlib.sha256(image.read_bytes()).hexdigest() == expected
        counts["images"] += 1
    assert row["fingerprint"] == hashlib.sha256((row["safe_sha256"] + row["sha256"]).encode()).hexdigest()
    for ref in row["evidence"].values():
        check_link(APP / "samples.json", ref)
    operations = json.loads((APP / row["evidence"]["operations"]).read_text())
    current = next(p for p in operations["pages"] if p["filename"] == row["operations"]["filename"])
    assert row["operations"] == {key: current[key] for key in row["operations"]}

patterns = {
    "personal path": r"/(?:Users|home)/[^\s/]+",
    "operational ID": r"\b(?:p|d|R|U)-[0-9a-f]{12,}\b",
    "credential": r"(?:gh[pousr]_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9_-]{24,}|AKIA[A-Z0-9]{16})",
}
for file in APP.rglob("*"):
    assert not file.is_symlink()
    if file.suffix in {".sqlite", ".sqlite3", ".db"} or file.name == ".DS_Store":
        errors.append("Unexpected runtime data: " + str(file.relative_to(APP)))
    if file.suffix not in {".html", ".css", ".js", ".json", ".md", ".cjs", ".py"}:
        continue
    counts["app_text_files"] += 1
    text = file.read_text()
    for name, pattern in patterns.items():
        if re.search(pattern, text):
            errors.append(f"{name}: {file.relative_to(APP)}")

print(json.dumps({"passed": not errors, **counts, "errors": errors}, ensure_ascii=False, indent=2))
raise SystemExit(bool(errors))
