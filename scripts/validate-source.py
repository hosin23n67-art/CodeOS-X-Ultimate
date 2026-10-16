#!/usr/bin/env python3
"""Fast source checks run before spending hours building the CodeOS ISO."""
from pathlib import Path
import ast
import subprocess
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
required = [
    "codeos-ui/install-codeos-ui.sh",
    "codeos-ui/codeos-keyboard-setup.sh",
    "codeos-ui/codeos-control-center.py",
    "codeos-ui/codeos-settings.py",
    "codeos-ui/codeos-store.py",
    "codeos-ui/xfce4-panel.xml",
    "codeos-ui/xfce4-desktop.xml",
    "codeos-ui/codeos-wallpaper.svg",
    "security-center/index.html",
]
errors = []
for name in required:
    path = ROOT / name
    if not path.is_file() or path.stat().st_size == 0:
        errors.append(f"missing or empty required file: {name}")

for name in ("codeos-ui/codeos-control-center.py", "codeos-ui/codeos-settings.py", "codeos-ui/codeos-store.py"):
    path = ROOT / name
    if path.exists():
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=name)
            print(f"Python syntax OK: {name}")
        except (SyntaxError, UnicodeError) as exc:
            errors.append(f"Python syntax error in {name}: {exc}")

for name in ("codeos-ui/install-codeos-ui.sh", "codeos-ui/codeos-keyboard-setup.sh"):
    path = ROOT / name
    if path.exists():
        result = subprocess.run(["bash", "-n", str(path)], capture_output=True, text=True)
        if result.returncode:
            errors.append(f"Shell syntax error in {name}: {result.stderr.strip()}")
        else:
            print(f"Shell syntax OK: {name}")

for name in ("codeos-ui/xfce4-panel.xml", "codeos-ui/xfce4-desktop.xml", "codeos-ui/codeos-wallpaper.svg"):
    path = ROOT / name
    if path.exists():
        try:
            ET.parse(path)
            print(f"XML/SVG parse OK: {name}")
        except ET.ParseError as exc:
            errors.append(f"XML/SVG parse error in {name}: {exc}")

installer = ROOT / "codeos-ui/install-codeos-ui.sh"
if installer.exists():
    text = installer.read_text(encoding="utf-8")
    if "codeos-security" not in text or "chmod 0755" not in text:
        errors.append("security-center launcher is not installed as an executable command")

if errors:
    print("\nSOURCE VALIDATION FAILED:", file=sys.stderr)
    for error in errors:
        print(f" - {error}", file=sys.stderr)
    sys.exit(1)
print("All source validation checks passed.")
