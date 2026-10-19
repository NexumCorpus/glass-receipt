# Glass Receipt: triage of uvsmtid/protoprimer#143

`report.md` ranks 13 competing pull requests. Don't trust it; check it:

    python verify.py

Standard library only, offline, about one second. It checks the file hashes, then recomputes every ranking-table cell it
has raw logs for (test-suite counts, `./prime` clean, referee score, own tests vs planted breaks) from `evidence/`
and compares them with the report. `VERDICT: VERIFIED` means the table says what the logs say. It does not re-run the
13 test suites (about 2 hours on WSL); the logs are what those runs printed. The `Diff` column and the prose are not
replayed. `ROOT` is the hash of the manifest; compare it with the root published alongside the bundle.

Built by Claude (Assay), directed by NexumCorpus.
