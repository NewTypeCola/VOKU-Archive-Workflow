# Public release finishing edits and verification

[한국어](../../korean/history/reference/publication-check.md)

The v4–v6 and English-default edition checks below are retained as historical records. See [current edition checks](#current-edition) for the latest local verification.

2026-09-27 · `history-anchor-v6`

The root introduction was expanded with physical transport, storage, scanning circumstances, and a representative photograph strip. Eighteen photographs, a five-image strip, and four groups of photo documents were added, and public-material licensing was standardized as MIT-0. The review app is described as a static sample to run in the reader's own environment.

## Check results

| Check | Result |
|---|---|
| Public file list and text checks | Passed: 275 files, 96 text files, 14 Python syntax checks, and 33 JSON files |
| Internal links and document anchors | 581 passed; no broken links |
| Current file hashes | Matched: 57 History files, 209 Workflow files, and 130 episode-manifest entries |
| New photograph files | 18 individual photographs and 1 strip decoded successfully; English slugs and WebP format checked |
| Internal image metadata | All 19 had no EXIF, XMP, ICC, comments, or other additional chunks |
| Image dimensions | Individual photographs: longest side at most 1,600px; strip: 2,520×1,080px, 21:9 |
| Photo-verifier rejection conditions | Passed 7 cases including 4 metadata/unknown chunk types, truncation, appended bytes, and invalid signature |
| Existing demo connections | 53 panel operation records, 106 image–OCR hash bindings, and 6 OCR mirrors matched |
| Static review-app checks | 8 public sample panels, 16 input/output images, and linked documents checked |
| App syntax, geometry, and keyboard | Passed JavaScript syntax, 6 scales / 4 rotations / 8 handles, and 18 keyboard/IME scenarios |
| Browser checks | Existing 15 functional groups passed in installed Chrome; local subpaths, storage, before/after switching, region editing, and export checked |
| Document display | Local Markdown rendering loaded README and 4 photo documents with 19 images; checked 1,440px desktop and root README at 390px mobile |

All 18 photographs retained the full original composition and aspect ratio. Only four faces in recording-room reflections and the car background were blurred; before resizing/encoding, pixels outside those regions were confirmed unchanged. The strip was adjusted to show more of the trunk and toppled cue sheets in the third panel and the cue-sheet pile in the fourth.

After orientation was applied, images were converted to sRGB and saved as new RGB images so capture metadata would not carry over. Individual photographs use WebP quality 86; the strip uses quality 88. Metadata checks concern the WebP file contents; hashes are recorded in the [History manifest](../history-anchor.json). Public, photo, and document-display checks were rerun for v5. App-function checks were run for v4; app execution code and samples were unchanged afterward.

## Preservation checks at the v4/v5 edits

SHA-256 hashes of all 18 original photographs match before and after the work. Bytes are also identical for 13 preserved code files, 192 existing demo files excluding current distribution manifests, six cases and `evolution.md`, 7 evidence/aggregate/provenance documents, 10 review-app logic/sample/test/existing-screen files, and the human–agent document. Only the first paragraph's baseline/photo links changed in `HISTORY.md`; the rest of the narrative and Mermaid source were retained.

Finishing edits modified 18 existing public files and added 26. The v5 composition adjustments replaced existing files and updated related documents and hashes while retaining filenames and the public list. No existing public file was deleted. Original filename mappings, enlarged working images, and browser-test records are excluded from the public list. These results concern local editing and checks, without actual external-hosting tests.

## v6 style edits and checks

Explanatory prose and sentence-style headings were standardized in polite Korean. LICENSE, NOTICE, actual quotations, code, and data were retained. Existing content and document structure were compared apart from endings, first-person/question wording, and baseline guidance; link anchors were updated for changed headings.

Photographs, demo images, OCR, execution code, and historical verification data are byte-identical to v5. After updating the current History/Workflow manifests, public-file, link, and hash checks passed. App-function tests were not rerun for this style edit.

## Rechecking

Run the following from the repository root. It uses only the Python standard library and reads files for verification.

```sh
python3 -B tools/verify_public.py
```

Review-app test commands and required development tools are in the [verification guide](../../workflow/assets/human-review/VERIFICATION.md#recheck). General users can follow the [local startup guide](../../workflow/assets/human-review/README.md#run-locally); distribution scope is in the [file list](../../public-files.txt).

<a id="english-edition"></a>

## 2026-09-27 · English-default edition

The current local v6 source was copied into a separate repository root. Its 35 explanatory documents now have English defaults and corresponding Korean versions under `korean/`, with reciprocal language links. Code, images, OCR, demo data, and the review app remain shared. VOKU's broader role as a university broadcasting station is distinguished from this archive's radio cue-sheet scope in both introductions.

Mermaid labels, image descriptions, and the app's controls and guidance are in English. Saved demo figures retain their original pixels and manuscript text, with English explanations alongside them. The current [English app screenshot](../../workflow/assets/human-review/review-screen-en.png) is separate from the preserved historical screenshot. App execution logic, sample operations, identifiers, tokens, coordinates, and stored status values were retained.

| Check | English-default edition result (`en1`) |
|---|---|
| Public inventory, links, anchors, and hashes | Passed for 312 public files, 35 document pairs, and all local references; [SHA256SUMS](../../SHA256SUMS) covers the other 311 public files |
| Manifests at that edit | `history-anchor-v6-en1`: 79 History entries; 210 Workflow entries and 130 episode-manifest entries matched |
| Read-only source preservation | All 608 source entries, including 503 files, retained their contents, modification times, types, and permissions |
| Preserved public evidence | 227 existing files were byte-identical, including all 179 existing images and 13 historical code files; operation records, OCR, historical verification data, and the MIT-0 grant were retained |
| Demo replay | All 53 panels from 1994, 2003, and 2017 matched recorded final pixel and WebP hashes; 106 OCR-image bindings and 6 OCR mirrors passed |
| Review app | Static checks for 8 panels / 16 images, JavaScript syntax, geometry at 6 scales / 4 rotations / 8 handles, 18 keyboard/IME scenarios, and 15 browser groups passed in installed Chrome |
| Document display | 70 documents, 10 Mermaid diagrams, and 64 image references rendered successfully; desktop and 390px mobile introduction layouts were inspected |
| Independent release copy | A copy of the 312 public files passed repository/static-app checks and all 53 replay checks with Python reads of the source repository blocked; no source access was attempted |

`public-files.txt`, the current manifests, and release checksums were refreshed for this edition. Earlier run records and their original figures above were retained as historical evidence. The replay applied already resolved operations; it did not repeat agent judgments or run OCR. The documented font and Pillow/libwebp requirements still apply. Local checks did not include Safari, Firefox, or external deployment.

<a id="current-edition"></a>

## 2026-09-28 · History reading order and verification references

The six-period narrative now precedes the glossary and map, as recorded in `history-anchor-v6-en2`. The `history-anchor-v6-en3` edit updates the current verification links and separates this check from the earlier English-default edition record. Historical narrative paragraphs, diagrams, cases, figures, evidence, and scope statements are preserved.

| Check | Current edition result |
|---|---|
| Public inventory and release hashes | Passed for 312 public files; the 311 entries in [SHA256SUMS](../../SHA256SUMS) matched |
| Current manifests | `history-anchor-v6-en3`: 79 History entries, 210 Workflow entries, and 130 episode-manifest entries matched |
| Document navigation | Local links and anchors passed; all 35 English/Korean document pairs have reciprocal language links; both History narratives use the same reading order |
| Demo image and OCR bindings | 53 panel records, 106 image–OCR hash bindings, and 6 OCR mirrors matched |
| Preservation | The `en2` narrative, cases, diagrams, images, OCR, code, and demo data are unchanged by this verification-reference edit |

These are local file, structure, link, and hash checks. The earlier replay, app-function, and browser results remain dated records above; those tests were not rerun for this documentation edit.
