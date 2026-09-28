# Public review app verification record

[한국어](../../../korean/workflow/assets/human-review/VERIFICATION.md)

Checked on 2026-09-26. **Local Chromium verification; no external deployment was performed.**

## Behaviors checked

- App and relative links loaded under `/review-preview/repository/workflow/assets/human-review/` and another site subpath. The 16 input/output WebP images for 8 selected panels were compared with public-demo SHA-256 hashes.
- Switching between public input and final output, preventing input-view edits and hiding output BBOXes there, and binding review records to the output image.
- Autosaving status, multiple issue types, and notes; recovery after reload; recovery of unconfirmed BBOX drafts.
- Actual pointer creation, movement, and resizing of regions; preservation of image-pixel coordinates after zoom and 90-degree rotation. Existing pure geometry tests also checked 6 scales, 4 rotations, and 8 resize handles.
- BBOX confirmation, name entry, and empty-name blocking in rereview mode; prevention of status changes in fields and during Korean composition. All 18 existing keyboard/IME scenarios also passed.
- Search, status filters, empty lists, list-page boundaries, and previous/next navigation. Earlier notes and coordinates remain in history even when switching to OK clears current regions.
- JSONL download for current reviews and full change history, and JSON download for conflicting drafts.
- Rejection of stale-tab saves and atomic revision checks for concurrent saves. Records remain isolated across browser contexts and deployment paths on the same host.
- Failure displays and draft-preservation paths when storage is blocked or quota errors occur. Invalid coordinate saves rejected.
- A 1440×1000 desktop and 390px-wide mobile layout. The [documentation screenshot](review-screen.png) was captured with example interaction notes on public data; those example reviews were not preloaded into the app.
- No server API, POST, or external-service requests during review, and no JavaScript runtime errors on normal review paths.

Browser checks passed 15 functional groups. This verifies public-sample UI/storage behavior, not exhaustive reading of actual scripts or approval to publish the archive. Safari, Firefox, and actual remote hosting were not tested.

## Preservation and file checks

The existing app's `static/index.html`, `style.css`, `app.js`, and `geometry.js` were the starting point. Interface, editing, shortcuts, and history flow were retained while server connections were replaced with `browser-store.js`. `geometry.js` is byte-identical to the reference app. Actual operational databases and records were neither copied nor run.

Before/after SHA-256 comparisons preserved 33 History-baseline/manifest files, 193 existing public demo files, 4 reference-app UI files, and 8 analysis materials read. Only `README.md` and `pipeline.md` changed among existing workflow documents; the existing demo and human–agent documents remained unchanged. New app-specific static checks passed for 8 panels, 16 images, 105 local links, and 12 app text files. File hashes, syntax, and obvious personal-path/operational-ID/credential patterns were also checked.

The existing repository-wide `verify_public.py` reported these 3 pre-existing missing paths, with no History hash errors. The parent README and public list still described Workflow/Demo as empty future areas. Those files lay outside that edit's boundary and were not updated. Passing app-specific checks was not represented as passing repository-wide packaging verification.

- Parent `README.md` link to `demo/`
- Parent `public-files.txt` entry `demo/.gitkeep`
- Parent `public-files.txt` entry `workflow/.gitkeep`

## Recheck

Run these from this app folder. Pure geometry/keyboard tests require only Node.js; browser tests use Playwright and Chromium in the development environment. Browser tests start a temporary read-only server, save profiles/test records only in `workflow/.review-check/`, and close the server and browser on exit. Since 2026-09-27, new test screenshots also go there, preserving the 2026-09-26 documentation screenshot `review-screen.png` during those checks. If needed, set `CHROME_BIN` to an installed Chromium-family browser executable. These tools are not runtime dependencies of the distributed app.

```sh
node --check app.js
node --check browser-store.js
node tests/geometry.test.cjs
node tests/shortcuts.test.cjs
python3 -B tests/verify_static.py
node tests/browser.test.cjs
```

`workflow/.review-check/` is excluded from distribution. See [local startup and static hosting](README.md) for distributing the existing public demo images and documents together.

<a id="integration-20260927"></a>

## 2026-09-27 · Public repository integration checks

The 2026-09-26 results above were retained as a contemporary record. This integration updated the root introduction and reading path, public list, current distribution manifests, and verification connections. History's `history-anchor-v3` and hashes from historical runs/comparisons were retained.

- Repository check `python3 -B tools/verify_public.py` passed: 249 public entries, 89 text files, 513 local links, syntax for 14 Python files, and 33 JSON files. The current 209-file workflow manifest and 130 episode-manifest entries, operation/page mappings for 53 demo panels, 106 input/final OCR-image hash bindings, and 6 OCR mirrors matched. The current manifest covers workflow public files except itself; `public-files.txt` is the repository-wide distribution list.
- Static app checks confirmed 8 public sample panels, 16 input/output images, hashes, applied regions, and document links.
- JavaScript syntax, existing geometry tests (6 scales / 4 rotations / 8 handles), and 18 keyboard/IME scenarios passed.
- The existing 15 browser-test groups passed in installed Google Chrome. Under two local subpaths serving only allowlisted files, checks covered root → Workflow → demo → app → review/repair History, app return links to the project/documents, images, and JSON. Temporary result paths returned HTTP 404. The 1440×1000 desktop and 390px-wide mobile test screenshots were also inspected.
- Seven rejection conditions were checked through simulated in-memory reads: missing files, browser temporary files/databases entering the list, wrong current-manifest hash/size, OCR-image binding errors, and missing document anchors. Actual inputs and completed files were not modified for these checks.
- Before/after SHA-256 comparisons preserved 33 History files including the baseline, 192 existing demo files excluding current distribution manifests, the human–agent document, existing review screenshot, and `NOTICE.md`. Preserved-file mtimes also matched; no file was deleted. Only the two nonexistent `.gitkeep` entries were removed from the public list. These are file/link preservation checks, not exhaustive script privacy review or OCR-accuracy checks.

Changed files were root `README.md`, `.gitignore`, `public-files.txt`, and `tools/verify_public.py`; workflow `README.md`, `pipeline.md`, `demo.md`, and `assets/demo/asset-manifest.json`; and app `README.md`, `VERIFICATION.md`, `index.html`, `tests/browser.test.cjs`, and `tests/verify_static.py`. One root `.nojekyll` was added to retain static publishing paths. No new fonts or license text were added.

The first browser attempt failed because the sandbox restricted local ports. After access was allowed, the default Playwright browser executable was unavailable, so installed Chrome was specified. Final checks completed in that environment. Safari, Firefox, and actual external deployment were not tested. Original materials and public-demo redaction/OCR were not rerun, and no remote upload, push, or deployment was performed.

## 2026-09-27 · Public wording finalized

Guidance waiting for a directly operated service address was removed and replaced with local static execution and optional static hosting. App review/storage logic and public samples were retained. Results of this recheck are in the [public release verification record](../../../history/reference/publication-check.md).

<a id="english-edition"></a>

## 2026-09-27 · English interface and bilingual documentation

The shared app's display strings and sample descriptions were translated into English, with a link to its Korean guide. Non-string JavaScript syntax trees and sample data outside the display-description fields match the source. Coordinate calculations and styles remain byte-identical.

JavaScript syntax, the existing geometry tests, all 18 keyboard/IME scenarios, static checks for 8 panels and 16 images, and the existing 15 browser groups passed in installed Chrome. The 1440×1000 desktop and 390px mobile screens were inspected. The current [English screenshot](review-screen-en.png) is supplied separately; the 2026-09-26 `review-screen.png` and the historical results above remain unchanged. Full release and source-preservation results are in the [English-edition verification record](../../../history/reference/publication-check.md#english-edition).
