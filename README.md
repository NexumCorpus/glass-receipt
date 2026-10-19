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

## Files

- `verify.py`: the verifier (also copied into each bundle).
- `make_bundle.py`: how the bundle is built from the triage logs (author paths are local; shown for transparency).
- `TRIAL-1.md`: the trial protocol, kill rule written before it ran, and result.

Built by Claude (Assay), directed by [NexumCorpus](https://github.com/NexumCorpus).
