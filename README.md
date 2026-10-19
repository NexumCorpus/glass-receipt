# Glass Receipt

**Work a stranger can check in one command, without trusting us.**

A Glass Receipt is a report bundled with the raw evidence behind it and a small verifier. The verifier does not take the
report's word: it recomputes every number it can from the raw logs and fails if the report disagrees, even when a forger
has rebuilt the hash manifest.

```
cd bundle-protoprimer-143
python verify.py
```

Python 3.8+, standard library only, offline, about one second. Expected output ends with:

```
REPLAY: PASS (53 cells recomputed from raw logs)
ROOT: 209eab8facfd85798cd08f557224e48a55bf3ba76982f814568b1c0a49658be2
VERDICT: VERIFIED
```

`ROOT` is the SHA-256 of the bundle's manifest. This line and the git history are its published anchor.
From the repo root, `python verify.py --root 209eab8facfd85798cd08f557224e48a55bf3ba76982f814568b1c0a49658be2` checks
every bundle with the root copy of the verifier (never the bundle's own) and also requires the published root:
`VERDICT: VERIFIED (root matches the published root)`. Without `--root` it says `VERIFIED (root not checked)`.

**Don't take the verifier's word either.** `python selftest.py` (same requirements, under a second) forges two copies of
the bundle with the manifest rebuilt and checks what the verifier says about each:

```
ok   case 1, untouched: VERIFIED, ROOT matches
ok   case 2, table cell forged: #148 suite 1462 -> 1463 pass: NOT VERIFIED, ROOT differs
       - #148 full suite: report says '1463 pass', logs say 1462 passed, 0 failed
ok   case 3, prose forged: 'Correct, minimal' -> 'Correct, elegant': NOT VERIFIED, ROOT differs
SELFTEST: PASS
```

Case 3 is the limit, stated: replay cannot see prose. The forgery is caught only because its ROOT differs from the
published one, which is why the self-test passes `--root`.
CI runs all three commands on Linux and Windows, Python 3.8 and 3.13.

## The first bundle: 13 competing PRs on uvsmtid/protoprimer#143

`bundle-protoprimer-143/report.md` triages 13 agent-written pull requests for one bounty: full test suite, `./prime` clean
tree, a 17-check referee written from the issue text, and planted breaks to see whether each PR's own tests notice.
The verifier replays the ranking table (test counts, clean tree, referee score, own tests vs breaks) from `evidence/`.
It does not re-run the suites (about 2 hours on WSL), and the prose is not replayed.

What happened after (stated plainly): the issue closed about 8 hours after the report was ready, and the bounty went to a
later PR (#159). That PR keeps `bash` when installed, which our referee had first scored as a defect. The referee check
was wrong, not the maintainer; it is fixed (R2 v2) and the report carries a dated revision. PRs are named by number only.

## Does it work? (trial 1, [TRIAL-1.md](TRIAL-1.md))

A fresh Claude Haiku with no context got two folders, one clean and one with a single table cell forged *and the
manifest rebuilt*. It rejected the forgery (naming the exact cell) and trusted the clean one, in 55 seconds. It also found
a real counting error in our own report ("4 of 13" defective PRs, 3 named), which we fixed. n = 1 verifier, one tamper
type: a start, not a proof.

Trial 2 ([TRIAL-2.md](TRIAL-2.md)) forged prose instead, with a different verifier model (Sonnet) working from this
public repo. The local verdict said VERIFIED for the forgery, as predicted. The model still refused it, because it
compared the files with the published ones and named the changed line. That's why the published ROOT matters, and
why `verify.py` now says "root not checked" unless you give it `--root`. Trial 3 ([TRIAL-3.md](TRIAL-3.md)) re-ran the
blind check with a fresh Haiku and no contamination. It caught a prose forgery that didn't change the meaning, at the
exact line, in 116 s. That makes 6 of 6 correct calls across 3 trials.

## What it does not claim

- It does not re-run the 13 test suites. It checks that the report matches the logs, not that the logs are honest.
- Prose and the `Diff` column are not replayed. Only the published ROOT protects them.
- Three trials, one verifier each, two tamper types. This is evidence that the idea works, not a security proof.

## Files

- `verify.py`: the verifier (also copied into each bundle).
- `make_bundle.py`: how the bundle is built from the triage logs (author paths are local; shown for transparency).
- `selftest.py`: the forgery check above.
- `TRIAL-1.md` to `TRIAL-3.md`: trial protocols, kill rules written before each ran, and results.

## Where it sits

Glass Receipt is the publishing format of [Nexum Corpus](https://github.com/NexumCorpus): instruments for verifiable
machine work. MIT licensed.

Built by Claude, directed by Nexum Corpus.
