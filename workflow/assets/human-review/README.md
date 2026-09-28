# Human Review · Public sample

[한국어](../../../korean/workflow/assets/human-review/README.md)

[App HTML](index.html) · [Execution demo](../../demo.md) · [Overall flow](../../pipeline.md#review-and-repair) · [Project introduction](../../../README.md)

This app is a **static review-tool sample** to open from the downloaded repository in your own environment. The creator does not plan to host and operate it. GitHub's HTML link displays source, so follow the local startup instructions below.

It reuses the existing Human Review interface, review flow, and coordinate calculations as a static web app. It connects **inputs already prepared for publication with synthetic personal identifiers and their final outputs**: 1994 pages 1 and 8; 2003 pages 5, 7, and 15; and 2017 pages 6, 7, and 13. It excludes originals containing real personal information, operational databases, and earlier visitors' review records. Names, tokens, applied regions, and evidence remain linked to the existing public demo.

## Usage

1. Switch between **Public input / Final output**. Zoom, fit-to-screen, fit-to-width, and rotation help inspect the same location. Review and BBOX entry operate on the final output.
2. Record status, issue types, and a note. Click **Add BBOX**, then drag to create a region. Selected regions can be moved, resized with eight handles, or deleted. Coordinates use original-resolution image pixels regardless of rotation or zoom.
3. In **Needs review**, draw a region, confirm by clicking or pressing Enter, and enter a synthetic name. Enter inside a name field finishes entry; Enter outside input fields saves feedback and moves to the next page needing review. Empty names block this next step.
4. Use **Find files** to search by year, filename, page ID, and status. Previous/next buttons navigate without changing status. During general review, arrow keys save OK and Space saves Needs review, then move to the next target. These shortcuts do not change status while typing, composing Korean text, or editing a BBOX.
5. View and download records through **Previous reviews and change history** and **Export JSONL**. Changing status to OK and clearing regions still retains before/after save history. **Public decisions and operations** are evidence from the prepared demo, distinct from feedback newly written by visitors.

Feedback and history are stored in browser IndexedDB; drafts, including unconfirmed BBOXes, use localStorage. They are not shared with other visitors' browsers or sent to a server. Tabs in the same device/browser profile/site path use the same records; revision checks prevent stale tabs from overwriting them. Records survive reloads. Clearing site data or closing a private window may remove them, so download anything to retain as JSONL. Environments blocking storage display errors.

Review records opinions and coordinates. Saving or exporting does not modify images, invoke an agent, or change actual archive approval states. If an image version changes, earlier feedback stays in history and the image returns to review. The app does not separately archive the old image itself.

## Run locally

The app uses only HTML/CSS/JavaScript and static JSON/WebP. It needs no separate login, operational database, API key, or application backend, and requests no external libraries or fonts. Feedback remains only in browser storage as described above.

After downloading the repository, run this from the **repository root**. This example uses Python 3's static file server; other static servers also work.

```sh
python3 -B -m http.server 8000 --bind 127.0.0.1
```

Open the [local review app](http://127.0.0.1:8000/workflow/assets/human-review/) in your browser. The command serves static files only on your computer. Press Ctrl+C in the terminal when finished. Opening HTML directly through `file://` is unsupported because of JSON loading and browser-storage restrictions.

## Place on static hosting · optional

You may also publish it on static hosting such as GitHub Pages. Copy only files in [public-files.txt](../../../public-files.txt) and retain the relative structure of the root, `workflow/`, `history/`, and `korean/`. Copying only the app folder omits neighboring `assets/demo/` images and document links. No separate build is required.

If choosing GitHub Pages, see its [publishing-source guide](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site). Keeping the root `.nojekyll` also serves Markdown paths unchanged. Open the app at `workflow/assets/human-review/` under the site path; relative links work when the repository is hosted beneath a URL subpath. This is an optional setup example.

On GitHub, Markdown is read as documents; on a simple static server, it opens as raw Markdown. The app and images share the same file structure in both cases. There is no procedure to register a running address or connect to the creator's server.

## Maintenance and checks

- `index.html`, `style.css`, `app.js`: the existing review UI adapted to public inputs, with before/after switching, sample guidance, and public evidence links.
- `geometry.js`: existing coordinate calculations retained unchanged.
- `browser-store.js`: replaces server storage interfaces with browser storage, search, conflict checks, and downloads. `/api/…` strings distinguish internal operations and are not HTTP requests.
- `samples.json`: relative paths, input/output SHA-256 hashes, and public application regions for the selected 8 panels. It neither duplicates images nor reads the original database.
- `tests/`: existing geometry and keyboard tests plus actual browser checks under static subpaths. Commands and results are in the [verification record](VERIFICATION.md).

Running `python3 -B tools/verify_public.py` from the repository root checks the explicit public list including app/documents/demo, local links, current manifests, OCR input hashes, and the History baseline. Browser profiles, downloads, and screenshots in `workflow/.review-check/` are excluded from distribution; adding them to the public list fails verification. The [2026-09-27 integration checks](VERIFICATION.md#integration-20260927) are recorded separately from earlier checks.

Current repository checks following photograph/document edits are in the [2026-09-27 public release verification record](../../../history/reference/publication-check.md).
