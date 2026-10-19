# Swarm triage: uvsmtid/protoprimer#143 (13 competing PRs)

**Issue:** [uvsmtid/protoprimer#143](https://github.com/uvsmtid/protoprimer/issues/143), "Add `ShellDriverSh`: use `/bin/sh` when `SHELL` is not set". Bounty: $75 (BountyHub), paid for a merged PR that meets the acceptance criteria.
**PRs triaged:** #144 to #156, all open. Every PR was tested at its head commit as of 2026-10-16 05:30 EDT, on base `main` @ `a33aced`.
**Prepared by:** NexumCorpus. This is an unsolicited sample. Nobody was contacted and nothing was posted. All runs were local.

> **Revision 2026-10-19 (Assay):** issue #143 closed 2026-10-16 17:29Z and the bounty went to #159, which keeps `bash` when installed. Our referee check R2 had scored that behaviour as a defect; R2 v2 accepts it (#144 13->14/17, #152 10->11/17; v1 logs kept as `referee_*.v1.log`). The summary count of defective PRs is corrected (it said 4, named 3, now 2).

## Summary

- **Recommendation: merge #148** (head `e13e23f`). It passes every check we ran, and its changes stay within the issue's scope:
  - full suite in CI mode: 1462 passed, 0 failed;
  - `./prime` leaves the tree clean, so the CI "no local changes" step should pass;
  - it passes all 17 checks in our independent referee test, including a real `dash` run with the venv activated;
  - its own tests catch the inertness mask and all 4 planted breaks, including through a real interactive-shell test;
  - it is the earliest PR in its code cluster.
- **#155 contains the same `ShellDriverSh` code as #148** (only placement and one comment differ) and was opened 6 h 45 min later. **#150 is a near-copy of #147**: 4 lines differ, all comments or log text.
- **2 of 13 PRs (#151, #152) have a substantive defect against the issue text:**
  - (revised 2026-10-19) #144 and #152 keep `bash` when `SHELL` is unset and bash is installed. We first scored this as a defect; the maintainer merged #159, which does the same, so it is acceptable and referee R2 now allows it.
  - #151 and #152 write `source` into the `sh` init file. Under a real POSIX `sh` (`dash`) this fails with `source: not found`, so the venv is never activated. Both PRs' own tests pass anyway.
- **5 of 13 PRs hand-edited the generated `proto_kernel.py`** instead of regenerating it: #144, #145, #146, #151 and #153. `./prime` rewrites the file, so the repo's CI step `test -z "$(git status --porcelain)"` would fail. That step already failed in the maintainer's CI on an earlier commit of #152.
- **The maintainer currently has almost no CI signal.** On 12 of 13 PRs the test workflow sits at `action_required` (waiting for maintainer approval to run on a fork). The green check on each PR comes only from the Read the Docs build. The one test run that did execute, on #147, failed: 2 failed, 579 passed.

## Ranking

The referee score counts our 17 independent checks (2 more are skipped because `busybox` is not installed). "Own tests vs breaks" is how many of the 5 masks and planted breaks the PR's own tests catch. "n/a" means the planted break is already present in the PR.

| Rank | PR | Author | Full suite (CI=true) | `prime` clean | Referee (17) | Own tests vs breaks | Diff | One-line reason |
|---|---|---|---|---|---|---|---|---|
| 1 | #148 | - | 1462 pass | yes | 17/17 | 5/5, real-shell test catches the init break | 5 files, +248/−48 | Correct, minimal, synced, well tested; earliest in its cluster |
| 2 | #150 | - | 1461 pass | yes | 17/17 | 5/5, real shell | 6 files, +276/−71 | Correct; code is a near-copy of #147 with the broken test fixed |
| 3 | #155 | - | 1469 pass | yes | 17/17 | 5/5, real shell (strongest: 13 failures under the mask) | 5 files, +286/−48 | Correct, best tests; kernel code is a duplicate of #148 opened ~7 h later |
| 4 | #156 | - | 1455 pass | yes | 17/17 | 5/5, real shell | 4 files, +168/−47 | Smallest correct diff. Its real `sh -i` test lives in the "mocked" suite without stdin isolation and hung in our harness when a TTY was attached |
| 5 | #154 | - | 1460 pass | yes | 17/17 | 5/5, real shell | 5 files, +233/−47 | Correct and clean; nothing distinguishing |
| 6 | #149 | - | 1462 pass | yes | 15/17 | 5/5, real shell | 9 files, +395/−127 | Correct; also follows the repo's TODO-doc conventions. Changes the `bash`/`zsh` init file too (quotes the venv path), which is a fix but outside the strict scope |
| 7 | #147 | - | **2 failed**, 1474 pass | yes | 17/17 | 5/5, real shell | 5 files, +422/−71 | Correct code, but 2 of its own tests fail in the full suite (`KeyError: 'internal'`), which the maintainer's CI also shows |
| 8 | #145 | - | 1457 pass | **no** | 14/17 | 5/5 | 5 files, +306/−47 | Behaviour correct; generated file not regenerated; venv path unquoted |
| 9 | #153 | - | 1454 pass | **no** | 14/17 | 5/5, text checks only | 4 files, +186/−48 | Not regenerated. Init file sources `~/.profile`. Its real-shell test never calls the driver |
| 10 | #146 | - | 1455 pass | **no** | 10/17 | 5/5 | 7 files, +227/−50 | Not regenerated; rewrites the shared base init file, so `bash`/`zsh` output changes |
| 11 | #144 | - | 1459 pass | **no** | 14/17 | 5/5, text checks only | 7 files, +380/−50 | Keeps `bash` when installed (acceptable, see revision); its integration test did not catch the planted init break |
| 12 | #151 | - | 1457 pass | **no** | 11/17 | n/a (bug already present) | 4 files, +191/−48 | **Venv not activated under `dash`** (`source`); no integration test |
| 13 | #152 | - | 1453 pass | yes | 11/17 | n/a (bug already present) | 4 files, +134/−36 | **`source` defect** (venv not activated under `dash`); keeps the `bash` fallback (acceptable); no integration test |

Base `main` passes the same full suite: 1448 passed, 0 failed (CI=true). No PR adds dependencies, install scripts or CI changes. None removes a public function or changes an existing signature. The test functions they remove are the two that the issue says to replace.

## Per-PR evidence

Notation: referee checks are named R1 to R8 (see Method). "Unquoted path" means the referee check R7 fails only when the venv path contains a space; base `bash` has the same pre-existing weakness.

- **#144:** `_get_shell_driver` keeps `shutil.which("bash")` and returns `ShellDriverBash` when bash exists. Referee R2 v1 failed (v2 passes, see revision): with no `SHELL` and `bash` on the PATH it returns `ShellDriverBash`. Other findings:
  - R7 fails when the venv path contains a space (unquoted path).
  - `./prime` rewrites `proto_kernel.py` (129-line diff).
  - With planted break M1, only the text check `test_write_init_file` failed; its `test_op_shell` integration test still passed.
- **#145:** Unconditional `/bin/sh` fallback, plus an `sh`-specific init file using `.`. Not regenerated (`./prime` produces a 146-line diff). R7 fails when the venv path contains a space.
- **#146:** Replaces `source` with `.` in `ShellDriverBase.write_init_file`, which changes the `bash` and `zsh` init files too (R8 fails: output differs from base). The behaviour is equivalent in those shells, but it is a change to code that was out of scope. It also removes the fallback warning log, is not regenerated, and has the unquoted path.
- **#147:** The code is correct (referee 17/17). `test_get_shell_driver_environment_isolation[*-None-ShellDriverSh]` fails with `KeyError: 'internal'`. It fails in the full suite but passes in isolation, so it is order-dependent. The test clears the environment, and that breaks the kernel's log filter. The maintainer's CI run 38765853845 reports the same 2 failures.
- **#148:** `ShellDriverSh` overrides `write_init_file` with POSIX `.`, uses `"$HOME/.shrc"`, and quotes the activate path with `shlex.quote`. The fallback to `/bin/sh` is unconditional. Other findings:
  - `SHELL` with basename `sh` is recognised.
  - The integration test `test_slow_integrated/test_ShellDriverSh.py` runs the exact `run_shell` command line with `ENV` under a real `/bin/sh`.
  - The tree is clean after `./prime`.
- **#149:** Adds a `get_source_builtin()` hook to the base class, which returns `.` for `sh`. It also quotes the activate path for all shells: this is why R8 differs from base, and only for paths with spaces. Other findings:
  - It deletes the resolved TODO doc and updates two docs, following repo conventions.
  - Its 13 commits include two "sync proto_kernel" commits.
  - The PR body discloses Claude use.
- **#150:** The kernel code differs from #147 only in one comment and the log message. The test that fails in #147 is fixed here. It adds tests to `test_ShellDriverBash.py`.
- **#151:** `ShellDriverSh` inherits the base `write_init_file`, which uses `source`. Under `dash` the init file errors with `source: not found` and the venv is not activated: R6 and R7 fail with `plain-path` (no space in the venv path). Its own tests pass, and planted break M1 cannot apply because the bug is already present. It is not regenerated and has no integration test.
- **#152:** It has the #144 `bash` fallback and the #151 `source` init file. It has no integration test. It is synced at its head commit; its earlier commit `f53104c` failed the maintainer CI's porcelain step.
- **#153:** The init basename is `.profile`, and the init file sources the user's `~/.profile`, a login file, on every interactive shell. Other findings:
  - Its real-shell test builds its own `ENV` file and never exercises the driver.
  - It is not regenerated and has the unquoted path.
- **#154:** Correct and synced. Uses an `if [ -f ... ]; then . ...; fi` form. Nothing negative found.
- **#155:** Kernel code identical to #148 (see genealogy). Most thorough tests in the set: 31 tests, 13 of which fail under the inertness mask. Correct and synced.
- **#156:** Correct and synced, with the smallest correct diff. Its `test_sh_interactive_init_applied` calls `subprocess.run([... "-i", "-c", ...])` with no `stdin=DEVNULL`. In our first cross-run, which had a TTY attached, this test hung for more than 4 minutes against rival code until we killed it: interactive `dash` took the terminal. With stdin detached it completes in about 1 s. Recommend adding `stdin=subprocess.DEVNULL` before merging.

## Alien checks

### 1. Cross-examination matrix: the tests confirm no PR has decorative tests, but they are tightly coupled to their own implementations

Every PR's new or changed test files were run against every other PR's code and against `main`, in CI mode. Cell values:
- E: collection error (`ShellDriverSh` does not exist on main);
- P: all pass;
- W: fails only on log-message wording;
- n: n substantive failures.

```
tests\code main  144  145  146  147  148  149  150  151  152  153  154  155  156
       144    E    P    W    W    1    1    W    1    1    1    4    1    1    1
       145    E    W    P    W    1    1    W    1    2    1    2    1    1    1
       146    E    2    1    P    1    1    1    1    2    3    4    1    1    1
       147    E    8    5    6    P    W    1    W    9   12   14    1    W    1
       148    E    4    4    4    W    P    2    P    6    5    7    2    P    2
       149    E    4    3    5    3    3    P    3    6    6    9    3    3    3
       150    E    3    3    3    W    P    1    P    4    4    8    1    P    1
       151    E    W    P    W    W    P    W    P    P    W    3    W    P    W
       152    E    P    W    W    W    W    W    W    W    P    2    W    W    W
       153    E    3    3    3    3    3    3    3    3    3    P    3    3    3
       154    E    1    1    2    W    W    W    W    2    2    7    P    W    W
       155    E    6    6    6    W    P    2    P   10   10   11    2    P    2
       156    E    2    2    2    W    W    W    W    3    3    3    W    W    P
```

- No PR's tests pass on unpatched `main`, so none are purely decorative.
- Most cross-failures come from exact-text assertions: warning wording, or literal init-file content. That makes the grid a weak correctness oracle on its own. We report this plainly rather than dress it up.
- The useful signals:
  - The 151 and 152 tests accept nearly every rival, including each other's `dash`-broken code.
  - The 153 code is rejected by all 12 rival suites.
  - The 147, 148, 150 and 155 code is accepted by 7 of 12 rival suites, the most of any PR.

### 2. Inertness (counterfactual masking): every PR's tests detect that the `_get_shell_driver` hunk was reverted

For each PR we replaced only `_get_shell_driver` with the base version, keeping the new `ShellDriverSh` class and the PR's own tests. Every PR's tests failed under this mask, with between 2 failures (#149, #152, #153) and 17 (#147).

A second, natural mask exists already: in #151 and #152, the `sh` init file still contains the non-POSIX `source`, and both PRs' tests pass. Their tests cannot see the defect that matters most for this issue.

### 3. Planted breaks: catch rates are high, but 2 PRs catch the key break only by text matching, and 2 cannot catch it at all

Four breaks were planted on top of each PR, and each PR's own tests were run in CI mode:
- **M1:** `.` changed to `source` in the `sh` init file;
- **M2:** the `ENV` assignment dropped;
- **M3:** `sh` basename recognition broken;
- **M4:** the no-`SHELL` fallback returns `ShellDriverBash`.

| PR | Catch rate | How M1 was caught |
|---|---|---|
| #144, #153 | 4/4 | Only by an init-file text assertion. Their real-shell or integration tests still passed. |
| #151, #152 | 3/3 | M1 not applicable: the bug is already there and their tests pass with it. |
| All 9 others | 4/4 | Also by a real interactive-shell test. |

### 4. Swarm genealogy: 13 PRs come down to 4 code clusters, and 2 PRs are near-copies

Method:
- normalised `difflib` similarity of the added kernel lines and of the added test lines;
- a direct `git diff` between PR heads;
- PR open times (2026-10-15/16 UTC).

| Cluster | PRs (open time) | Approach |
|---|---|---|
| A: `sh` override, `$HOME/.shrc`, `shlex.quote` | #147 (16:04) → **#150 (19:44): 4 differing lines, comments/log only**; #148 (19:08) → **#155 (01:53+1): identical `ShellDriverSh` code, only block placement and a comment differ**; #154 (23:24) and #156 (04:10+1) are independent variants | The correct, majority design |
| B: `sh` override, `~/` and unquoted path | #144 (15:17), #145 (15:37), #153 (20:57). Kernel similarity 89–94%; #144 keeps the `bash` fallback; #153 uses `.profile` | Early and close to the TODO doc's wording |
| C: no override, base init file reused | #146 (15:44), #151 (20:19, 91% similar to #146 minus its base edit), #152 (20:36, adds the `bash` fallback) | Leads to `source` under `dash` unless the base is edited |
| D: base-class hook | #149 (19:12) | Unique |

- Test files are far less similar than kernel code. The highest pairs are 148/155 at 62% and 144/146 at 64%. So cross-PR similarity sits mostly in the small solution space of the kernel change.
- We cannot tell copying apart from the same tool given the same prompt. The table shows only near-identity and timing.
- For review, one PR per cluster is enough: #148 (A), #145 (B), #146 (C), #149 (D).

### 5. Consensus vs. truth: the majority was right on design, but the PRs' own tests do not show which code is correct

| Decision | Majority | Minority | Who is right |
|---|---|---|---|
| No-`SHELL` fallback | 11 of 13 use an unconditional `/bin/sh`, matching the issue text | #144 and #152 keep `bash` | The majority |
| Init file | 9 of 13 override it in `ShellDriverSh` with `.` | #146 and #149 edit the base and still work; #151 and #152 inherit `source` and break under `dash` | The two inheriting PRs are wrong |
| Venv path | 7 of 13 quote it | 6 leave it unquoted | Quoting is safer |

- "Swarm consensus is not correctness" shows up most clearly in test quality. Our referee test (R7, a real `dash` run) catches the broken PRs at once.
- The tests of #151 and #152, which make up the "accept everything" rows in the grid, pass every rival including each other.
- The single check that best separates the PRs is the oldest one: run the real shell.

## Method

1. **Isolation.**
   - Cloned into `E:\bounties\triage\protoprimer` and fetched `pull/<n>/head` for each PR into local branches `pr-<n>`. All 13 are based on `main` @ `a33aced`.
   - Ran each PR in its own git worktree (`E:\bounties\triage\wt\pr-<n>`) inside WSL Ubuntu 24.04, where `/bin/sh` is `dash`.
   - Nothing was pushed, commented or opened.
2. **Pre-execution screen.**
   - Every diff touches only `primer_kernel.py`, `proto_kernel.py`, tests, and, for #149, docs.
   - No dependency, packaging, CI or install-script changes. `subprocess` calls appear only in tests.
   - With nothing suspicious found, we ran each PR's code.
3. **Build and suite.**
   - Ran the repo's own bootstrap `./prime` per worktree: it creates a uv venv on Python 3.14.0 and regenerates `proto_kernel.py`.
   - Then `git status --porcelain`, which is the repo CI's "no local changes" step.
   - Then the full `pytest` suite with `CI=true`, which enables `test_slow_integrated`, under `setsid` with `</dev/null`.
4. **Referee test.** We wrote `E:\bounties\triage\tools\test_referee.py` independently of all PRs, from the issue's acceptance criteria. It ran against both kernel copies and gave identical results.
   - R1: no `SHELL` returns `ShellDriverSh`.
   - R2: same when `bash` is on the PATH.
   - R3: `SHELL=/bin/sh` returns `ShellDriverSh`.
   - R4: `SHELL=/bin/fish` raises `ValueError`.
   - R5: exact argv `["/bin/sh","-i","-c",cmd]`, `ENV` set, no `--init-file`.
   - R6: no bashisms in the init file.
   - R7: a real interactive `/bin/sh`, `dash` and `bash --posix` apply the init file and activate a fake venv, for a plain path and a path with a space.
   - R8: `bash` and `zsh` argv, env and init file are byte-identical to base.
   - Validation: on base `main` it fails 12 checks and passes 5.
5. **Alien checks.**
   - The N×N cross-run (`tools/cross.sh`).
   - The inertness mask and planted breaks (`tools/mutate.py`, `tools/run_mut.sh`).
   - Similarity clustering (`logs/gen/`).
6. **Raw evidence.** Everything is under `E:\bounties\triage\logs\`:
   - `ci-<n>/pytest_ci.log`;
   - `pr-<n>/{prime.log,git_status_after_prime.txt,referee_*.log,ci/mutation.tsv}`;
   - `cross_ci/`.

## Limits

- **One Python version.** Suites ran on Python 3.14 only (the max). Criterion 3 also requires the minimum, 3.7. We did not run it (Docker was not running), and only checked that the changed files parse under the 3.7 grammar, which they all do.
- **One `sh` implementation.** We tested `dash`, plus `bash --posix`. `busybox ash` was not installed, so those two referee cases were skipped.
- **Text-coupled tests.** Cross-matrix failures are dominated by text-coupled assertions, so the grid ranks test portability more than correctness. We relied on the independent referee test and the planted breaks for correctness.
- **Narrow planted breaks.** The four planted breaks target this one change. A high catch rate does not show the tests are good in general.
- **No intent detection.** Genealogy shows similarity and timing, not intent or authorship.
- **Not a maintainer decision.** Ranking within the correct group (#148, #150, #155, #156, #154, #149) depends on our judgement of minimality, provenance and test hygiene. Style preferences, the maintainer's view on #149's doc edits, and contributor history are left to the maintainer.
- **Point-in-time snapshot.** PRs may have been updated after 05:30 EDT 2026-10-16.
