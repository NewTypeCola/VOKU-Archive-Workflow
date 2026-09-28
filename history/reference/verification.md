# Verification record for the public edition

[한국어](../../korean/history/reference/verification.md)

The 2026-09-27 photograph/document edits and current package checks are in the [public release verification record](publication-check.md). Below are records from the creation of each baseline.

## Localized edit checks — history-anchor-v3 · 2026-09-26

- Paragraph, table, and section structure and the order and frequency of numbers in HISTORY, evolution, and the six cases were compared with their pre-edit versions. Figures were retained except for the baseline-version notation.
- Sentence-ending changes were compared separately from functional explanations added at the first mention of code names. The detailed Mermaid source, `limits.md`, historical code, and existing aggregate JSON were preserved unchanged.
- Demo-verification and reuse explanations from an earlier public draft were removed. History documents retained only links to targets inside this package.
- Changed-file hashes were updated to fix the baseline. The v2 and v1 figures and verification scopes below are records of their respective editing points.

## History reorganization — history-anchor-v2 · 2026-09-26

This verification concerns History's reorganization and editing. Actual archive counts and evidence checked in v1 are preserved below and in the linked JSON.

- Connections among the History narrative, evolution, six cases, reference, and historical code were checked against the new directory structure.
- A glossary and map of problem branches and merges were added. Solid edges represent transfers of materials, decisions, code, or outputs; dashed edges represent related branches addressing the same problem.
- Preserved-code hashes were compared with [code-provenance](code-provenance.json). Existing aggregate JSON and provenance contents were also compared with pre-edit hashes.
- Numbers and sentences in each reference evidence entry were compared with pre-edit content. Denominator explanations were added while preserving the six periods, timeline, and failed paths.
- File hashes in the new [anchor manifest](../history-anchor.json), the repository-root public allowlist, internal links, Python syntax, and public-text patterns were checked.

### v2 comparison results

- Checks passed for 40 public files, 32 History-baseline files, 220 internal links, and syntax of 12 Python files.
- SHA-256 hashes for 13 historical code files and 3 existing aggregate/code-provenance JSON files match their pre-edit values.
- Reversing the added glossary, map, denominator explanations, and baseline-version notation reproduces the earlier History narrative hash. Only denominator explanations were added to the first case; hashes of the other five cases were retained.
- Figures in each E01–E35 evidence entry were compared after normalizing only comma formatting; values and occurrence counts were retained.
- The new History map and existing evolution diagram were parsed and rendered with Mermaid 12.0.0 and visually checked. The new map has 30 nodes / 39 edges, with 0 syntax or rendering errors.

## History baseline reinforcement — history-anchor-v1 · 2026-09-26

- Read-only comparisons covered the archived database and checkpoint of the single-agent reading alternative (read-v2), current database/session/outputs of the session-input alternative (read-next), incorporation records of the isolated geometry tests (tmptest), later-year name-repair outputs, and final omission-investigation reports. [Additional counts](history-observations.json)
- Hashes matched for 59 receipts / 644 pages and 210 outputs in the OCR line-rewriting path. History was corrected where construction/intermediate reports differed from later execution.
- v1 fixed hashes for HISTORY, six cases, evidence, counts, and code. The public verifier checked hashes, allowlist, internal links, and code provenance.
- Hashes of 297 existing investigation inputs and hashes/mtimes of 49 separately recorded original database/code/report items were preserved. The sets overlap; checks concerned the recorded files.
- Historical-code hashes were retained in the v1 edit, and only the specified sentence was deleted from WORKFLOW.
- Operating-system metadata was excluded from the public allowlist. Public-text path, credential, operational-ID, and email patterns and private-roster names were checked, along with ZIP contents and each file's hash.

## Checks performed for the initial public edition

This was the scope checked when the first public edition was made on the same day. Original archive production processing was not rerun.

- Current source-database state counts, final-image counts, and 66,010 pages / 1,992,165 lines in 5,330 OCR JSON files were compared. [Counts without identifying details](current-observations.json)
- The 297 inputs hashed at investigation start, 13 preserved-code originals, and 11 separately fixed database/report files remained preserved at comparison time. These sets may overlap; checks concerned the recorded files.
- All public Python files were syntax-checked without importing original production modules. Public JavaScript syntax was also checked. Full Swift production execution was not performed.
- Historical-code distribution hashes were compared with provenance. Markdown internal file links and explicit evidence anchors were checked.
- Personal home-directory absolute paths, credentials, operational IDs, and email patterns were checked. Public text was also compared locally against 267 unique names from the private fixed roster. A false positive caused by words joined in one sentence was examined and corrected with spacing; final matches were 0.

## Rechecking the current baseline

Run the following from the repository root. It uses only the Python standard library and reads files for verification.

```sh
python3 -B tools/verify_public.py
```

public-files.txt is the allowlist for current public files. Private investigation materials and source materials are excluded.
