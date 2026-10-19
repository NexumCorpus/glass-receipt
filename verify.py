"""verify.py - check a Glass Receipt bundle without trusting its author. Python 3.8+, standard library only, offline.

    python verify.py            # run inside the bundle folder; exit 0 = VERIFIED, 1 = NOT VERIFIED
    python verify.py --root <hex>   # also require ROOT to equal the root the author published (e.g. in a git commit)

Three checks:
  1. INTEGRITY  every file listed in MANIFEST.sha256 exists and matches its SHA-256; no unlisted evidence files.
  2. REPLAY     every cell of the report's ranking table that has raw evidence in this bundle is recomputed from the
                raw logs (full test suite, `./prime` clean, referee score, own tests vs planted breaks) and compared
                with what the report says. A report edited after the fact fails here even if the manifest was rebuilt.
  3. ROW        the attached Night Adversary ledger row is well-formed and its verdict follows from its own fields.
The ROOT line is the SHA-256 of MANIFEST.sha256. Compare it with the root the author published elsewhere (e.g. a git
commit); a match means you hold exactly the bundle that was published. Pass it as --root to have the verdict check it;
without --root the verdict says "VERIFIED (root not checked)", because the checks above prove the bundle is consistent,
not that it is the bundle that was published.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EV = HERE / "evidence"


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def integrity():
    problems, listed = [], set()
    man = HERE / "MANIFEST.sha256"
    if not man.exists():
        return ["MANIFEST.sha256 missing"], None
    for line in man.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, rel = line.split("  ", 1)
        listed.add(rel)
        p = HERE / rel
        if not p.exists():
            problems.append(f"listed file missing: {rel}")
        elif sha(p) != digest:
            problems.append(f"hash mismatch: {rel}")
    for p in HERE.rglob("*"):
        rel = p.relative_to(HERE).as_posix()
        if p.is_file() and rel not in listed and rel != "MANIFEST.sha256" and "__pycache__" not in rel:
            problems.append(f"unlisted file: {rel}")
    return problems, sha(man)


def suite(pr):
    f = EV / f"ci-{pr}" / "summary.tsv"
    if not f.exists():
        return None
    text = f.read_text(encoding="utf-8").split("\t")[-1]
    passed = int(re.search(r"(\d+) passed", text).group(1))
    m = re.search(r"(\d+) failed", text)
    return passed, int(m.group(1)) if m else 0


def prime_clean(pr):
    f = EV / f"pr-{pr}" / "git_status_after_prime.txt"
    return None if not f.exists() else f.read_text(encoding="utf-8").strip() == ""


def referee(pr):
    f = EV / f"pr-{pr}" / "referee_proto.log"
    if not f.exists():
        return None
    last = [l for l in f.read_text(encoding="utf-8").splitlines() if l.strip()][-1]
    m = re.search(r"(\d+) passed", last)
    return int(m.group(1)) if m else 0


def own_tests(pr):
    f = EV / f"pr-{pr}" / "mutation.tsv"
    if not f.exists():
        return None
    rows = [l.split("\t") for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]
    breaks = [r for r in rows if r[1] != "CLEAN"]
    if any(r[2] == "NA" for r in breaks):
        return "n/a"
    return f"{sum(1 for r in breaks if r[2] != '0')}/{len(breaks)}"


def table_rows(report):
    rows = {}
    for line in report.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 8 and re.fullmatch(r"#\d+", cells[1]):
            rows[cells[1][1:]] = cells
    return rows


def replay():
    report = (HERE / "report.md").read_text(encoding="utf-8")
    rows, problems, checked = table_rows(report), [], 0
    if not rows:
        return ["ranking table not found in report.md"], 0
    for pr, c in sorted(rows.items()):
        full, clean, ref, own = c[3], c[4], c[5], c[6]
        s = suite(pr)
        if s is not None:
            checked += 1
            p_ok = re.search(r"(\d+) pass", full)
            f_m = re.search(r"(\d+) failed", full)
            said = (int(p_ok.group(1)) if p_ok else -1, int(f_m.group(1)) if f_m else 0)
            if said != s:
                problems.append(f"#{pr} full suite: report says {full!r}, logs say {s[0]} passed, {s[1]} failed")
        pc = prime_clean(pr)
        if pc is not None:
            checked += 1
            said = clean.strip("*").lower()
            if said != ("yes" if pc else "no"):
                problems.append(f"#{pr} prime clean: report says {clean!r}, logs say {'yes' if pc else 'no'}")
        r = referee(pr)
        if r is not None:
            checked += 1
            m = re.match(r"(\d+)/17", ref)
            if not m or int(m.group(1)) != r:
                problems.append(f"#{pr} referee: report says {ref!r}, logs say {r}/17")
        o = own_tests(pr)
        if o is not None:
            checked += 1
            if not own.startswith(o):
                problems.append(f"#{pr} own tests vs breaks: report says {own!r}, logs say {o}")
    base = suite("main")
    if base is not None:
        checked += 1
        m = re.search(r"Base `main` passes the same full suite: (\d+) passed, (\d+) failed", report)
        if not m or (int(m.group(1)), int(m.group(2))) != base:
            problems.append(f"base main: report line does not match logs ({base[0]} passed, {base[1]} failed)")
    return problems, checked


def row():
    f = HERE / "adversary-row.json"
    if not f.exists():
        return ["adversary-row.json missing"]
    r = json.loads(f.read_text(encoding="utf-8"))
    need = {"case", "pr", "kind", "change", "should_flag", "nex_flagged", "nex_exit"}
    if not need <= set(r):
        return [f"adversary row missing fields: {sorted(need - set(r))}"]
    if r["nex_flagged"] != (r["nex_exit"] == 1):
        return ["adversary row inconsistent: nex_flagged does not match nex_exit"]
    return []


def run_bundles():
    """run from the repo root: check every bundle folder below with THIS file's code, never with the bundle's own
    verify.py (a bundle is untrusted input). Any nonzero or signal exit counts as a failure."""
    import subprocess
    bundles = sorted(p.parent for p in HERE.glob("*/MANIFEST.sha256"))
    if not bundles:
        print("no bundle here: cd into a bundle folder (one with MANIFEST.sha256) and run python verify.py")
        return 2
    failed = False
    for b in bundles:
        print(f"== {b.name}", flush=True)
        extra = ["--root", arg("--root")] if arg("--root") else []
        rc = subprocess.run([sys.executable, "-I", str(Path(__file__).resolve()), "--bundle", str(b), *extra]).returncode
        failed = failed or rc != 0
    return 1 if failed else 0


def arg(flag):
    return sys.argv[sys.argv.index(flag) + 1].strip().lower() if flag in sys.argv[:-1] else None


def main():
    global HERE, EV
    if "--bundle" in sys.argv:
        HERE = Path(sys.argv[sys.argv.index("--bundle") + 1]).resolve()
        EV = HERE / "evidence"
    elif not (HERE / "report.md").exists():
        return run_bundles()
    ip, root = integrity()
    rp, n = replay()
    ap = row()
    for name, probs, extra in (("INTEGRITY", ip, ""), ("REPLAY", rp, f" ({n} cells recomputed from raw logs)"),
                               ("ROW", ap, "")):
        print(f"{name}: {'PASS' if not probs else 'FAIL'}{extra}")
        for p in probs:
            print(f"  - {p}")
    want = arg("--root")
    print(f"ROOT: {root}")
    if want:
        print(f"ROOT CHECK: {'PASS' if want == root else 'FAIL'} (published root {want})")
    ok = not (ip or rp or ap) and (want is None or want == root)
    note = "" if not ok else (" (root matches the published root)" if want else " (root not checked: pass --root <published hex>)")
    print("VERDICT:", ("VERIFIED" if ok else "NOT VERIFIED") + note)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
