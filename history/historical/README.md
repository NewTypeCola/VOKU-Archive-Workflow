# Preserved copies of actual tools

[한국어](../../korean/history/historical/README.md)

These are **13 files: 8 complete files and 5 function excerpts**, taken from the source packages as they stood at investigation. The contemporary code form is preserved. Original file hashes and lines, added imports, comment edits, and distribution hashes are recorded in [provenance](../reference/code-provenance.json).

Personal home-directory paths and actual inputs, ledgers, and name/token mappings were excluded. Only a comment explaining an example syllable was generalized; executable statements were retained. Some excerpts have necessary general-purpose imports added.

| Preserved code | Form | Execution-history distinction | Application evidence |
|---|---|---|---|
| [identity/global_identity_v3.py](identity/global_identity_v3.py) | Complete file | Identity reconstruction ran; image redaction was not authorized | aggregate_summary and independent verification for large-scale identity reconstruction (attempt_008) |
| [names/spatial.py](names/spatial.py) | Complete file | Operational use | Current main redaction code and submission, geometry, and export records |
| [names/measured_characters.py](names/measured_characters.py) | Function excerpt | Operational use | Main geometry-stage receipts; conservative segmentation can hold a page |
| [names/program_submission.py](names/program_submission.py) | Function excerpt | Operational use | Whole-program submission patch and actual 47-document submission |
| [names/session_ownership.py](names/session_ownership.py) | Complete file | Operational use | Two-session patch, current reading_sessions database, and main/reverse execution records |
| [names/short_alias.py](names/short_alias.py) | Function excerpt | Operational use | 10 occurrences / 9 pages in the 28-page bounded pilot |
| [repair/render_contract.py](repair/render_contract.py) | Complete file | Implemented and partially applied; did not complete all 2,230 later-year pages | Current artifact history: 58 rows / 18 unique pages; distinct from later hold-resolution path (new-boryu) completion |
| [review/geometry.js](review/geometry.js) | Complete file | Operational use | Review app with 21,009 current image records |
| [approval/masking.py](approval/masking.py) | Complete file | Operational use | Fixed-cell redaction; later call configuration specifies cells 3, 5, and 7 |
| [contacts/paint_union.py](contacts/paint_union.py) | Function excerpt | Operational use | 3,518-page refit and later approved 76-page gap repair |
| [contacts/recover_components.py](contacts/recover_components.py) | Function excerpt | Operational use | Refit comparison of discovery-ledger rows and connected components of actual changed pixels |
| [composition/compose.py](composition/compose.py) | Complete file | Operational use | Initial 66,010-page composition and later integration receipts |
| [ocr/vision_ocr_multiprocess.swift](ocr/vision_ocr_multiprocess.swift) | Complete file | Operational use | Complete/selected OCR of final images and original/image hash links |

## Reading code and execution evidence

- review/geometry.js and contacts/paint_union.py are small functions accepting inputs.
- program_submission, session_ownership, render_contract, and global_identity depend on the original packages' core/storage/reading/database contracts. Private dependencies and operational databases are not distributed, so standalone production execution is not provided.
- composition/compose.py is an actual batch tool that writes files and saves state. It took contemporary plans and later revisions as input; full execution is explained through receipts from that time.
- The Swift OCR file is an actual macOS Vision processor. It requires a prepared plan and source images.
- approval/masking.py defaults to cells 3 and 5, unlike the later actual configuration of 3, 5, and 7. It is preserved without updating the default to the latest scope.

The current public verifier checks distribution hashes and Python syntax. Original production execution is connected through contemporary records. Preserved code also uses [MIT-0](../../LICENSE.md). See [NOTICE](../../NOTICE.md) for provenance and external components.
