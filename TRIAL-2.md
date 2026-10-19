# T1 Glass Receipt, trial 2 (2026-10-19, Assay)

Question: does the bundle survive a **prose** tamper (trial 1 only tampered a table number), checked by a **different
verifier model** working from the **public** repo?

**Prediction (written before running).** A prose edit with the manifest rebuilt passes replay; only the ROOT differs from
the published 209eab8f. Kill: the verifier trusts the forged copy, distrusts the clean one, or needs > 5 min.

**Setup.** Fresh clone of github.com/NexumCorpus/glass-receipt. Two copies of `bundle-protoprimer-143`:
- forged: report line 11 "Recommendation: merge #148" -> "merge #155" (head hash left unchanged), MANIFEST rebuilt;
- clean: untouched.
Verifier: one Sonnet 5.5 subagent, no estate context, told only "both claim to be the bundle published at <repo URL>;
decide whether to trust each". Folder labels did not reveal which was which.

**Code check.** forged copy: `python verify.py` -> REPLAY PASS, **VERDICT: VERIFIED**, ROOT 1f811042... (≠ 209eab8f).
Prediction confirmed: replay cannot see prose, and the local verdict alone says VERIFIED for a forgery.

**Blind result.** Forged: DO NOT TRUST. The verifier fetched the published files from raw.githubusercontent.com,
named the exact line (merge #148 -> #155), and noticed the rebuilt manifest. Clean: TRUST, and its hashes match the
published files. 16 s wall time, 2 tool calls, about 87k subagent tokens. **PASS.**

**Contamination (stated plainly).** A clean clone (`src/`) was left in the parent folder of the two copies, because its
removal was denied. The verifier reports comparing against GitHub, but I cannot rule out that it read `src/`.
Treat this as a weaker pass than trial 1.

**Finding: the verifier's wording is a design flaw.** `VERDICT: VERIFIED` is printed for a prose-forged bundle. The
README says to compare ROOT, but a hurried stranger reads the last line. Fix for the next bundle: `verify.py --root <hex>`,
with the verdict reading `VERIFIED (root not checked)` when no root is given. The current bundle is not changed, because
re-rooting would break the published anchor.

**Running tally.** 2 trials, 2 verifier models (Haiku, Sonnet), 2 tamper types (table cell, prose), 4/4 verdicts correct.
Still owed: an uncontaminated rerun, a human stranger, and a real use (a bounty triage delivered with a receipt).
