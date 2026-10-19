"""selftest.py - show that verify.py catches a forgery, instead of asking you to believe it.

    python selftest.py          # Python 3.8+, standard library only, offline, a few seconds; exit 0 = all as expected

Copies the published bundle to a temporary folder three times and runs this repo's verify.py on each, with
--root set to the published root:
  1. untouched                                         -> expect VERIFIED, ROOT matches
  2. one ranking-table number forged, MANIFEST rebuilt -> expect NOT VERIFIED (REPLAY names the cell)
  3. one prose word forged, MANIFEST rebuilt           -> expect NOT VERIFIED, caught only because ROOT differs
Case 3 is the limit, stated: replay cannot see prose. Without --root the verdict for case 3 would be
"VERIFIED (root not checked)"; only the published root protects prose.
"""
import hashlib
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUNDLE = HERE / "bundle-protoprimer-143"
PUBLISHED_ROOT = "209eab8facfd85798cd08f557224e48a55bf3ba76982f814568b1c0a49658be2"


def rebuild_manifest(b):
    man = b / "MANIFEST.sha256"
    lines = []
    for line in man.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rel = line.split("  ", 1)[1]
            lines.append(f"{hashlib.sha256((b / rel).read_bytes()).hexdigest()}  {rel}")
    man.write_bytes(("\n".join(lines) + "\n").encode("utf-8"))


def forge(b, old, new):
    rep = b / "report.md"
    text = rep.read_bytes().decode("utf-8")
    assert old in text, f"selftest out of date: {old!r} not in report.md"
    rep.write_bytes(text.replace(old, new, 1).encode("utf-8"))
    rebuild_manifest(b)


def verify(b):
    out = subprocess.run([sys.executable, "-I", str(HERE / "verify.py"), "--bundle", str(b), "--root", PUBLISHED_ROOT],
                         capture_output=True, text=True).stdout
    root = re.search(r"ROOT: (\w+)", out)
    return "VERDICT: VERIFIED" in out, (root.group(1) if root else None), out


def main():
    cases = [
        ("untouched", None, True, True),
        ("table cell forged: #148 suite 1462 -> 1463 pass", ("| 1462 pass |", "| 1463 pass |"), False, False),
        ("prose forged: 'Correct, minimal' -> 'Correct, elegant'", ("Correct, minimal", "Correct, elegant"), False, False),
    ]
    failed = 0
    with tempfile.TemporaryDirectory() as tmp:
        for i, (name, edit, want_verified, want_root_match) in enumerate(cases, 1):
            b = Path(tmp) / f"case{i}"
            shutil.copytree(BUNDLE, b)
            if edit:
                forge(b, *edit)
            verified, root, out = verify(b)
            ok = verified == want_verified and (root == PUBLISHED_ROOT) == want_root_match
            failed += not ok
            print(f"{'ok  ' if ok else 'FAIL'} case {i}, {name}: "
                  f"{'VERIFIED' if verified else 'NOT VERIFIED'}, ROOT {'matches' if root == PUBLISHED_ROOT else 'differs'}")
            for line in out.splitlines():
                if line.startswith("  - "):
                    print("       " + line.strip())
    print("SELFTEST:", "PASS" if not failed else f"FAIL ({failed} case(s) not as expected)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
