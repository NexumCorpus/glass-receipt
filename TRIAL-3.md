# Trial 3: uncontaminated blind rerun (Assay, 2026-10-19)

Question: with NO clean copy anywhere in the trial folder's ancestry, does a context-free Haiku catch a prose forgery
that has a rebuilt manifest, while still trusting the clean copy?

**Prediction (written before running).** Forged copy: DO NOT TRUST, by comparing ROOT or files against the public repo.
Clean copy: TRUST. Kill: it trusts the forgery, distrusts the clean copy, or needs > 5 min.

**Setup.** Two copies of `bundle-protoprimer-143` in an otherwise empty scratch folder (`t3/`, with nothing in its parent).
Labels copy-x / copy-y assigned by `random.shuffle`. One narrative sentence was edited in the forged report and its
MANIFEST rebuilt, so local `verify.py` prints VERIFIED for both copies. The key was sealed outside the trial folder.
Verifier: one Haiku 5.5 subagent with no estate context. It got the two paths and the public repo URL, and was asked to
list every path and URL it touched (the contamination audit).

**Key (unsealed after the verdict).** copy-y was the forgery: report.md line 73, "Correct and synced" became "Correct and,
notably, synced". My meaning-changing regex found no match, so a meaning-neutral fallback edit was used instead. That
makes this the hardest kind of tamper to see by reading, and the easiest to miss. Local `verify.py`: VERIFIED for both
copies. ROOT: copy-x 209eab8f (the published root), copy-y f2ae349e.

**Blind result.** copy-x: TRUST, because all 58 files are byte-identical to public `master`. copy-y: DO NOT TRUST; it
named report.md line 73 ("and" -> "and, notably,") and the matching rebuilt MANIFEST line. 116 s, 13 tool calls, about
117k subagent tokens. **PASS**, inside the 5-minute kill line.

**Contamination audit (self-reported).** It read only `t3/copy-x` and `t3/copy-y`, plus GitHub API and raw URLs. One
stray write to `/tmp_pub_list_unused` failed with permission denied. No clean local copy existed anywhere in the trial
folder's ancestry. Limits: the audit is the verifier's own account, not a syscall trace. My prompt said branch `main`; the
repo's only branch is `master`, and the verifier found that itself.

**Running tally.** 3 trials, 2 verifier models, 3 tamper types (table cell, meaningful prose, meaning-neutral prose), 6/6
verdicts correct, and 1 run uncontaminated. Still owed: a human stranger, and a real use. Since d69c77a, `verify.py --root`
turns "VERIFIED" for a forgery into "VERIFIED (root not checked)" or NOT VERIFIED (this is not pushed yet).
