# T1 Glass Receipt, trial 1 (2026-10-19, Assay)

Plan: Fable meta-pass 2026-10-19 §2 T1 + §4 Day 1-2. Kill rule (written before the trial, in that plan): a fresh Haiku
with zero estate context cannot verify the bundle in <= 5 min, or fails to catch a one-line tamper of the report.

**Bundle.** `make_bundle.py`: report.md (= E:\bounties\triage\SAMPLE-REPORT.md) + 40 raw log files (ci-*/summary.tsv,
pr-*/git_status_after_prime.txt, referee_proto.log, mutation.tsv) + one Night Adversary ledger-v2 row + `verify.py`
(stdlib, offline: SHA-256 manifest, then recomputes 53 ranking-table cells from the raw logs, then row consistency).

**Self-check (code).** clean: VERIFIED, 53/53 cells match. naive tamper (#147 "**2 failed**, 1474 pass" -> "1476 pass",
manifest untouched): NOT VERIFIED (hash + replay). rehash tamper (same edit, manifest rebuilt): NOT VERIFIED (replay only).

**Blind trial.** One Haiku 5.5 subagent, no estate context, prompt = two folder paths + "decide whether you can trust
each report". bundle-A = rehash tamper, bundle-B = clean (labels not revealing).
- Verdicts: A DO NOT TRUST (named the exact #147 cell); B TRUST. Both correct.
- Time: 55 s wall (6 tool calls, ~109k subagent tokens). Limit was 5 min.
- **Result: PASS. T1 survives its first kill test.**

**What the stranger found that we had not.** The report's summary said "4 of 13 PRs have a substantive defect" but named
3 unique PRs (#144, #151, #152). Real error in a report not yet sent; fixed in SAMPLE-REPORT.md (backup
SAMPLE-REPORT.md.bak-20261019-assay), clean bundle rebuilt and re-verified (root 4c32816a...). It also noted honest limits:
ROOT is uncheckable without a published anchor; verify.py is the author's own code (it read it and hand-checked cells);
prose claims (similarity, CI run ids, action_required) are not replayed.

**Limits of this trial.** n = 1 verifier, 1 tamper type (a number in the table). A prose-only tamper would pass replay
and be caught only by the published ROOT. Next: publish the root with the bundle (a git commit), a prose tamper, and a
second, different verifier model.
