# Demo assets

[한국어](../../../korean/workflow/assets/demo/README.md)

The three episode folders contain all 49 physical PDF pages as 53 upright logical images. The four two-up sheets also have safe/final reassemblies. Protected personal identifiers are synthetic; public figures, departments and entry years are retained.

## Inspect

Open an ordinary folder or its image index: [1994](1994/complete/README.md), [2003](2003/complete/README.md), [2017](2017/complete/README.md). No extraction is required. Each folder contains `demo-source-safe/` and `final/` WebP images, `page-map.json`, resolved `operations.json`, unedited Apple Vision results in `ocr/`, and `manifest.json`.

All 158 former PNGs preserve their resolution. The 114 complete-episode images use lossy WebP quality=90, method=6; the 44 representative figures use lossless WebP. [Conversion records](format-conversion.json) retain the previous PNG hashes, the intermediate lossless WebP hashes, and the current file and decoded-pixel hashes. The quality-90 images are not pixel-identical to their earlier lossless versions.

The finalized operations were rerun from the delivered compact safe inputs, and the resulting final images were encoded at quality 90. The composition changes pixels only in its declared regions before encoding. Historical layer hashes in operations.json refer to the original run-v4 PNG intermediates; compact-input replay and its pre-encoding pixel hashes are recorded separately. Corrected 2017 pages also record `current_layers` pixel hashes. Two-up sheets are exactly reassembled from delivered logical panels before their own quality-90 encoding.

The safe and final WebP images were actually read by Apple Vision. After the cancellation fix, only the seven changed final pages were read again; untouched page objects were retained. Every OCR sourceSHA256 matches the file named by sourceRel, relative to this directory. OCR text and coordinates were not manually rewritten.

## Replay the protected result

Use Python 3 with Pillow and numpy, plus the recorded macOS Apple SD Gothic Neo font. The font is not redistributed. The script checks its SHA-256 and stops if it differs. For byte-identical WebP output, use the Pillow/libwebp versions in operations.json; the script also checks decoded pixel hashes.

From the shared `workflow/assets/demo/` directory in the repository root:

```sh
python3 -m pip install Pillow numpy
python3 replay.py 2017/complete --out rebuilt-2017
```

This replays name erasures/tokens, approval-cell processing and contact masks, composes their regions, and checks every final WebP hash. Identity decisions are already resolved. Replay does not run OCR; the fresh OCR was separately produced with the [preserved Swift implementation](../../../history/historical/ocr/vision_ocr_multiprocess.swift).

The [demo's work process](../../demo.md#decisions-to-repair) and `decisions.json` explain where those decisions came from and what changed after review. Replay is the resolved-operation renderer, not the agent's reading or judgment process. It erases all names before placing tokens, then draws new 1 px cancellation strokes in the name layer for `input_cancelled` staff tokens. A 2+2 token receives one stroke per row. No original name ink is restored.

The private preparation, original crops, real-to-synthetic maps and ImageGen reference prompts are excluded. The public source-safe images are the starting point for replay.

## Visuals and evidence

`overview.webp`, scene comparisons and `2017/composition.gif` are derived from actual processing pixels. The GIF shows two separate PDF pages. `*-regions.webp` files are explanatory geometry overlays. The replacement-name and credits comparisons, plus the GIF's name scene, reflect the cancellation fix. Other unaffected figures retain their earlier processing pixels.

`2017/input-review.webp` is a frozen comparison from safe-input preparation. `2017/token-repair.webp` is the frozen earlier/corrected comparison from the erase-before-token repair; it predates the cancellation fix. These historical images are retained as evidence, not relabelled as current finals. Raw OCR excerpts are never hand-corrected. [Revision verification](revision-verification.json) records the changed outputs, unchanged inputs, representative-image provenance and checks.

`execution-summary.json` states actual scope, versions, code reuse, adaptation, review and checks. `decisions.json` contains fictional identities and public decision examples. `asset-manifest.json` lists the final public allowlist and hashes.
