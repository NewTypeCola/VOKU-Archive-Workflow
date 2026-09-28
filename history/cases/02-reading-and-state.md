# 2. From changing workers to changing reading units and handoffs

[한국어](../../korean/history/cases/02-reading-and-state.md)

[History](../HISTORY.md) · [Related additional evidence](../reference/evidence.md#e27)

Name processing in early September was not a sequence of upgrades to one engine. Image workers, a separate saved-OCR-only path, isolated geometry tests for main processing, a single-agent alternative, and a session alternative overlapped. Following the actual transfer of outputs and decisions distinguishes changes in agent count from changes in judgment, coordinates, or scope.

## Problems left by image-worker operations

In image-worker-based name processing (`voku-ocr-v3`), the main agent handled OCR and routing, while actual image workers inspected originals, set bboxes, applied masks, and reviewed outputs. Separate from the 172 documents / 2,170 pages in the September 5 stop record, a three-episode specified-model test remained before application because the user stopped it immediately after claim. Newly created tokens and partial work were preserved when stopping. [E10](../reference/evidence.md#e10)

Selective overlay processing (overlay) tested reducing the materials to read. Short standalone production-credit forms and damaged introduction lines were missed by compact selection, requiring selection-rule improvements. Work left by a usage-limit stop resumed in a new location using existing materials. The first 55 pages and later 896 pages were different execution scopes. When completed outputs were collected, 67 missing approval links among 6,920 pages were recovered from historical review replies, viewing records, and geometry evidence. When the user corrected the storage location, paths were moved and links repaired without regenerating images.

Image-worker operations (Luna v3) actually resumed with up to three workers taking six pages each. One worker's completion report disagreed with actual signature/date overlap and rendering-limit results. Instead of simply accepting the completion count, the affected output was returned to hold. The stop count after finishing active work was 12 masked / 1 hold among 13 pages, with 0 uncollected or active jobs. Agent reports were themselves checked against actual receipts and outputs. [E33](../reference/evidence.md#e33)

## Another contemporary compromise: rewriting entire OCR lines

The OCR read-only experiment (`voku-ocr-readonly`) prohibited fresh OCR and agent image viewing and used only saved coordinates. When no precise existing mask bbox was available, it covered the entire saved OCR line and redrew the string with names replaced by tokens. It retained the surrounding **text strings**, but did not preserve the original handwriting, typefaces, spacing, and OCR errors exactly as they were. The contemporary README and code stated this limitation.

Current receipts from September 5 cover 59 episodes / 644 pages, with 210 output pages and 538 applications of `saved_ocr_line_bbox`. The progress summary stopped earlier at 40 episodes / 485 pages / 153 outputs. The execution scope therefore requires reading receipts together with actual files, not just that summary. No link was found showing transfer of these separate outputs to main processing. [E34](../reference/evidence.md#e34)

## Geometry repairs that actually followed the 52-page test

The isolated main-processing test ended with verified 12 / no_changes 30 / partial 8 / hold 2 across 4 documents / 52 pages. All four documents were held and exports totaled 0. Name reading and decision writing took about 310 seconds, while geometry and rendering services totaled about 17 seconds; nevertheless, coordinates and token placement were also immediate blockers in this sample. [E11](../reference/evidence.md#e11)

The subsequent isolated geometry-test (`tmptest`) materials retain the repair process. Character progression in rotated scripts was normalized before returning to original coordinates, and OCR-box overlap was distinguished from actual ink intersection. Repairs also addressed detached table rules splitting production-credit font-size groups and faint neighboring lines entering name boxes. With already-read decisions fixed as regression materials, coordinate repairs did not require discovering names again from the beginning.

The fourth run of a new 3-episode / 17-page test completed 1 document and held 2. A one-page episode lacked identity context for two people. The **page set to process** was therefore separated from the **reference scope for identity confirmation**. OCR from other episodes was read as hash- and document-linked reference copies limited to the two already discovered names, without adding those reference episodes to the redaction queue. Academic information absent from the working episode was retained only as identity evidence, not represented as a current observation.

In the fifth verification, a new geometry case failed even though two existing samples passed. Further repairs passed the sixth regression check, and the seventh run reused the same readings to complete all 17 pages: verified 11 / no_changes 6, with station-member name erasures and tokens 35/35. Eight code files, 3 fixtures, and 3 documents were then incorporated into the operational package. Test databases, new tokens, and completed states were not merged into operational data. Limited agent tests and code-repair iterations actually occurred here; the same role structure did not persist across every other operating period. [E27](../reference/evidence.md#e27)

## Single-agent reading alternative (read-v2): geometry failures remained with one agent

On September 7, the user wanted to abandon multiple semantic-judgment agents in favor of one agent performing analysis → repair → testing → feedback. The hold analysis at the time contained many mechanical causes such as `NAME_TOUCHES_PROTECTED_FORM`, `NAME_RANGE_NOT_LOCATED`, and `NAME_INK_CROSSES_PROTECTED_FORM`. Reducing the number of agents and resolving those errors were different tasks.

`read-v2` was built with six stages: text decisions, original preparation, coordinates, rendering, human review, and specified feedback. It inherited 5,330 documents / 66,010 pages and 316 identity bindings, and required renewed review of current outputs when feedback arose. After 29 construction-time tests and compatibility checks on 6 existing images, **actual execution** followed. The first page's name link was submitted, but the coordinate stage stopped on `NAME_RANGE_NOT_LOCATED` and `VISION_FAILED: nilError`, producing no new image.

The user then requested “stage 1 only.” A text-only prompt was created that did not call preparation, coordinates, or rendering, and readings for another 5 documents / 84 pages were submitted in two packets. The archived ZIP's database records 85 newly `read` pages, 4,009 inherited readings, 61,916 unread pages, 3 submitted packets and 1 open packet, and 0 new images. [E28](../reference/evidence.md#e28)

## The changed unit in main processing: owning a program unit versus reading it

Main processing's `program-claim` already granted ownership of the entire same-year, same-semester program unit. But `program-packet` returned it in chunks, defaulting to at most two episodes / 45,000 characters and permitting at most ten episodes. Program-unit ownership alone did not show that actual judgment used the whole program context.

The September 8 change was to receive all unsubmitted episodes in one packet and decision statement. Missing episodes or invalid quotation/context checks rejected the entire submission. At a stop, only episodes actually read to the end were recorded with reasons, allowing resumption under the same lease. Long program units were read in file segments, but semantic judgment and submission remained at program-unit scope. An actual submission of 47 documents / 320 pages left 89 verified / 185 no_changes / 46 partial. Whole-program reading did not eliminate geometric failure; it preserved the contextual judgment preceding that failure. [E13](../reference/evidence.md#e13)

The user's explicit optimization target was the combined working time of agent and user. The instructions were to avoid repeating identity judgments on the same evidence, route coordinate failures back to geometry, stop deliberating once evidence was sufficient, and let code generate counts and resume positions. Reducing repeated JSON in reading views shrank one sample from 123,095 to 35,815 characters while retaining current OCR lines, alternatives, and identity links. This addresses the same kind of bottleneck as the earlier 310-second observation, but the record does not say that this single measurement directly triggered the instruction.

## Session-input alternative (read-next): a session interface branched after program-unit reading

`read-next` copied 76,237 files and operational state from the improved main name-reading and redaction path (`read-only-masking`). Whole-program reading, compact display, and existing geometry/rendering were already in the source. Additions were `session-open/read/commit/close` and the first review handoff. Grouping actual occurrences under one semantic judgment and listing exceptions separately allowed the package to assemble the formal decision format. The delivery cursor was also separated from declarations of actual reading.

This package also went beyond construction. On September 9, one program unit with 7 documents / 82 pages / 3,651 OCR units was read and submitted. Comparing the current session and database gives 64 unchanged pages, 11 verified, and 7 partial, with 18 output files from verified and partial combined. Pencil names the user had instructed it to hold and geometric review remained; the program was `running` and the contemporary close result was `review`. The memory record also retains an execution deviation: submission JSON was assembled with Python despite a request not to use a generation script. A new interface did not immediately change working habits. [E29](../reference/evidence.md#e29)

The construction-time README and STOP_POINT still said production had not started. Later submissions and actual outputs support this correction. There is also no record of read-next being transferred back into later main processing. The account therefore does not invent a linear lineage of `read-v2 → read-next → main program-unit processing`.

## main/reverse: two independent execution sessions sharing identities

In main processing, one session was responsible for one program unit's context, identities, and exceptions, while code assigned years and program units. Main worked from earlier years and reverse from later years, but the database, fixed roster, existing IDs, and tokens were shared. Of 181 roster members then, 102 appeared across multiple years, creating a risk of separate identity authorities in independent copies. The two sessions shared 1 Vision process, 2 renderers, and 1 export handler. [Ownership code](../historical/names/session_ownership.py)

A 20-minute observation on September 9 distinguished newly submitted work from carried-over readings. Of reverse's 233 pages, 64 already read pages were subtracted to give 169; 35 read but unsubmitted pages were also excluded. This measured how far results had actually been handed off in operation. Character density and recurring-person context differed by year as well.

The final first-pass database contains formal decisions for 5,330 documents and page states of verified 21,009 / no_changes 40,714 / partial 4,182 / hold 105. Submission code recorded decisions, evidence, state, and the next processing position. It also retained traces of an older helper filling the default `review=read`, so that field alone could not stand in for the actual reading process. Follow-up work reused existing identities, coordinates, and receipts while handling the remaining 4,287 pages by cause. [E12](../reference/evidence.md#e12)
