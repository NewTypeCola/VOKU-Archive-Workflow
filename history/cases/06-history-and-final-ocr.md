# 6. Tokens outside the latest receipt, and OCR following images

[한국어](../../korean/history/cases/06-history-and-final-ocr.md)

[History](../HISTORY.md)

## Completion was reported, but 8 tokens were unchanged

After a token-typography edit, the user first asked why one page had been missed. Investigation found that production-credit tokens in the latest revision record had changed, but 8 tokens already composed from an earlier revision of the later-year name-repair path (supplement) were absent from the list. Pixels in those regions matched the backup, confirming they were unchanged. The cause was **preparation logic that read only the latest receipt without replaying earlier revisions**. [E25](../reference/evidence.md#e25)

The user then specified changing only those 8 tokens on one page to 2+2 syllables at 13px, leaving existing four-syllable tokens untouched. Historical glyphs were replayed exactly and removed before drawing the new tokens; untargeted regions and the other 66,009 pages were preserved. This was bounded repair tracing resolved historical operations, not new judgment or renewed candidate discovery.

Another typography path had old private-individual protection blocking current token regions. Simply taking a union of protection masks could not represent event order. Landscape, production-credit, and portrait layouts used different criteria, and the user set sizes and exceptions, so they were not reduced to one global font size.

## Strokes outside exact bboxes were a separate decision

A later staff correction on 15 pages processed 26 input regions: 21 new tokens, 3 masks only, and 2 horizontal shifts. The user specified **applying only the supplied bboxes exactly**. Boxes were not automatically expanded to cover residual strokes outside them, and verification recorded 0 changes outside authorized regions. A tool broadening scope by declaring such residuals “incomplete” would override the user's decision. [E25](../reference/evidence.md#e25)

## From original-OCR substitution to fresh OCR of final images

The initial sensitive-form substitution plan (P0-5A) proposed replacing sensitive forms in original OCR. The August 21 revision changed this to fresh OCR of final WebP images, with old OCR used for mapping and QA, because public text should match final images. The observation that no complete run existed in the contemporary input-material folder (`game`) does not contradict the later observation of actual complete OCR in the final composition/OCR folder (`final-tri-force`). It is **a connection between a plan and its later execution**. [E02, E24](../reference/evidence.md#e24)

Both complete-generation records cover 66,010 pages / 5,330 documents: the first produced 1,990,913 lines and the next 1,992,139. A comparison records 21,314 changed final images between them. This count is not calculated by adding overlapping correction-batch sizes. [Actual Swift OCR code](../historical/ocr/vision_ocr_multiprocess.swift)

Subsequent specified name corrections on 62 pages and contact corrections on 52 pages each updated 39 episode JSON files. The updates respectively preserved 633 and 447 untargeted page objects within the same JSON files, and each preserved the remaining 5,291 JSON files. The current direct recount is 1,992,165 lines.

## Not mistaking a verification failure for an output failure

Path comparison failed because Python and Swift handled Unicode normalization of macOS filenames differently. Normalization and `samefile` comparison were improved instead of renaming files or rerunning all OCR. Seven blank originals received explanatory notes after user confirmation, while original values were preserved for 15 lines on 13 pages whose normalized bboxes extended slightly outside boundaries. Coordinates were not silently clamped. [E24](../reference/evidence.md#e24)

Current images, historical top-level manifests, later receipts, and OCR `sourceSHA256` may refer to different points in time. Mismatches in old manifest samples are explained by later backups, application receipts, and current image/OCR hashes. [E26](../reference/evidence.md#e26)

The final state remained a connection among current image sets, OCR generated from them, local correction receipts, and review states, rather than a single `done=true`.
