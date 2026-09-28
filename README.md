# VOKU Archive

[한국어](korean/README.md)

VOKU (Voice of Kyonggi University) is a student-run university broadcasting station whose activities span radio broadcasting, video production, and stage and live event production. This archive focuses on cue sheets created for its student-produced campus radio broadcasts. VOKU Archive is an individual project to digitize and prepare for public access **66,010 pages of internally produced broadcast cue sheets from 1988–2019, a span of 32 years**.

This repository contains the **Workflow, History, a three-episode execution demo, and a review web app** from that work. While redacting parts of the scripts that needed protection, I used pseudonym tokens to retain, where possible, repeated participation by the same producer and collaboration within episodes. The documents explain how judgment, processing, review, and correction actually connected.

![Cue sheets on a bookshelf, a transport cart, boxes loaded in a car, materials stored at home, and the scanning desk](history/assets/photos/archive-process-strip.webp)

Bookshelf → packing → transport → storage at home → scanning. [18 photographs of the materials and workspaces](history/photos/README.md)

## Where to start

- [Workflow](workflow/README.md): the entry point to the working method. Follow [human and agent judgments and corrections](workflow/human-agent-workflow.md) and [the connections between materials and outputs](workflow/pipeline.md).
- [Three-episode execution demo](workflow/demo.md): inputs, outputs, decisions, corrections, and OCR for **49 physical pages / 53 logical panels** from 1994, 2003, and 2017.
- [Public review web app guide](workflow/assets/human-review/README.md) · [App HTML](workflow/assets/human-review/index.html): a static sample for comparing **8 panels** from the demo and recording feedback. Download the repository and run it in your own environment.
- [History](history/README.md): a record of events, failures, changes, and evidence from the work. Case links in Workflow also lead to the relevant evidence.
- [VOKU Archive dataset on Hugging Face](https://huggingface.co/datasets/NewTypeCola/VOKU-Archive): the prepared 66,010-page corpus, including images, OCR, and token annotations.

## Why and how I made it

As a former station member, I did not want cue sheets made by earlier members to remain abandoned in storage. Paper folders held the sentences and handwriting used to prepare broadcasts, along with traces of changes in assigned roles. I saw bringing those materials into a readable form as a kind of broadcasting in itself.

I packed the cue sheets from the bookshelves into boxes and bags and moved them on a cart. With help from a senior alumnus, I loaded them into a car and brought them home. I distributed the materials across the living room, another room, and the entryway, then opened the scripts on my desk and scanned them one page at a time with a multifunction printer. The process is recorded in [transport photographs](history/photos/transport.md), [storage at home](history/photos/storage.md), and [the scanning workspace](history/photos/scanning.md).

Scanning began on February 17, 2026, and ended on June 6. After scanning and initial sorting, I took about two months off because of burnout and resumed on August 15. Working alone with Codex (GPT-6 Astra), I planned and ran the redaction and token pipeline, completing this round of processing on September 25.

I paid all costs myself. I am grateful to the senior alumnus who helped carry the cue-sheet boxes. The dates and circumstances above are the creator's confirmed account; the processing supported by contemporary code and records continues in [Workflow](workflow/pipeline.md#source-and-ocr) and History.

## Public scope and remaining limits

This repository **does not distribute the full 66,010-page dataset.** Public files consist of explanatory documents, selected code, prepared photographs, a demo with synthetic personal identifiers, and the review web app, managed through the [public file list](public-files.txt). They do not include images or OCR of the complete real scripts, operational databases, real-name mappings, or private review records. [History's scope and counts](history/reference/status-and-counts.md) explains the processing scope and counting rules.

Errors may remain in classification, identity resolution, region processing, and OCR. Redaction and tokens do not guarantee complete anonymity or a complete reconstruction of production relationships. September 25 marks the end of this local processing round; technical verification, human review, publication decisions, and actual distribution are separate. Checks for this repository edit are recorded in the [public release verification record](history/reference/publication-check.md#current-edition).

The review web app is a public tool sample to run in your own environment. I do not plan to host and operate it myself. It works without a separate login, operational database, or API key, and new feedback stays only in the visitor's browser storage. See [the app guide](workflow/assets/human-review/README.md#run-locally) for startup and storage behavior.

## Whose project is this, and where are the originals?

**Creator credit: Jeoung Geunyeong** — independent creator of this digital archive and former station member.

This is **an individually led project carried out with permission from the alumni association**. It was neither led nor funded by the university. The association's permission does not mean that every producer individually consented or that all rights to the scripts have been secured. The original paper documents are now stored at the university broadcasting station again.

The public materials in this repository use **MIT-0**. They may be used, modified, and redistributed without attribution. See [LICENSE](LICENSE.md) for the scope by material type and the distinction from separate script and third-party rights, and [NOTICE](NOTICE.md) for preserved code provenance and external components.

🎵 *If I Didn't Have You* — Thank you for reading.
