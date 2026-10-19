"""make_bundle.py - assemble the Glass Receipt bundle for protoprimer#143 (T1 cheapest experiment, Assay 2026-10-19).

    python make_bundle.py OUT_DIR [--tamper naive|rehash]

naive: one table cell edited, manifest left as built.  rehash: same edit, manifest rebuilt (a careful forger).
"""
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

SRC = Path("E:/bounties/triage")
HERE = Path(__file__).resolve().parent
ADV_ROW = Path("E:/station/prophet/night-adversary/ledger-v2.jsonl")
PRS = [str(n) for n in range(144, 157)]
TAMPER = ("| 7 | #147 | jmass-ggg | **2 failed**, 1474 pass |", "| 7 | #147 | jmass-ggg | 1476 pass |")


def manifest(out: Path):
    lines = []
    for p in sorted(out.rglob("*")):
        rel = p.relative_to(out).as_posix()
        if p.is_file() and rel != "MANIFEST.sha256":
            lines.append(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {rel}")
    (out / "MANIFEST.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def build(out: Path, tamper: str | None = None):
    if out.exists():
        shutil.rmtree(out)
    ev = out / "evidence"
    for pr in PRS + ["main"]:
        (ev / f"ci-{pr}").mkdir(parents=True)
        shutil.copy(SRC / "logs" / f"ci-{pr}" / "summary.tsv", ev / f"ci-{pr}" / "summary.tsv")
    for pr in PRS:
        (ev / f"pr-{pr}").mkdir(parents=True)
        for f in ("git_status_after_prime.txt", "referee_proto.log", "mutation.tsv"):
            text = (SRC / "logs" / f"pr-{pr}" / f).read_text(encoding="utf-8", errors="replace")
            (ev / f"pr-{pr}" / f).write_text(text.replace("pytest-of-dalea", "pytest-of-user"), encoding="utf-8", newline="\n")  # local username out
    rep = (SRC / "SAMPLE-REPORT.md").read_text(encoding="utf-8", newline="\n")
    # public rail (E:/station/OUTBOX.md): PRs by number, never by author -> blank the Author column, keep the columns
    rep = re.sub(r"^(\| \d+ \| #\d+ \| )[^|]+(\|)", r"\1- \2", rep, flags=re.M)
    (out / "report.md").write_text(rep, encoding="utf-8", newline="\n")
    shutil.copy(HERE / "verify.py", out / "verify.py")
    shutil.copy(HERE / "README-bundle.md", out / "README.md")
    rows = [json.loads(l) for l in ADV_ROW.read_text(encoding="utf-8", newline="\n").splitlines() if l.strip()]
    pick = next(r for r in rows if r.get("kind") == "SIG" and r.get("nex_flagged"))
    (out / "adversary-row.json").write_text(json.dumps(pick, indent=1), encoding="utf-8", newline="\n")
    manifest(out)
    if tamper:
        rep = out / "report.md"
        text = rep.read_text(encoding="utf-8", newline="\n")
        assert TAMPER[0] in text, "tamper anchor not found"
        rep.write_text(text.replace(TAMPER[0], TAMPER[1], 1), encoding="utf-8", newline="\n")
        if tamper == "rehash":
            manifest(out)


if __name__ == "__main__":
    t = sys.argv[sys.argv.index("--tamper") + 1] if "--tamper" in sys.argv else None
    build(Path(sys.argv[1]), t)
    print("built", sys.argv[1], "tamper=" + str(t))
