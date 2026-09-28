# 3. Review outputs became inputs for the next reading and tool

[한국어](../../korean/history/cases/03-review-and-repair.md)

[History](../HISTORY.md) · [Later composition](05-composition.md)

The 4,287 partial/hold pages left by first-pass name processing were not one kind of failure: 2,768 had only mechanical problems, 1,087 only semantic problems, 426 both, and 6 empty OCR. In 918 episodes, only one page remained held. Repeating an existing identity judgment and repairing the region where applying that judgment to actual pixels failed were different tasks. [E12](../reference/evidence.md#e12)

## Why rework branched into independent paths

On September 10, the user clarified that the existing package was “for a fast first pass,” not designed for rework. Rather than a design reusing its CLI, queues, and program leases, the user requested a separate execution structure using existing results as source materials. The request at this point was for planning only; production did not begin during design. Actual implementation took place in the later individual tasks. [E30](../reference/evidence.md#e30)

Operational constraints were specific. Reopening old holds through two sessions whose semantic-reading queues were exhausted hit the year-ownership check `REVIEW_OUTSIDE_SESSION_YEAR`. Pages marked issue by humans viewing completed outputs also did not overlap the contemporary hold/partial pages. The former needed replacements while preserving previous outputs; the latter needed unresolved problems solved where normal outputs did not yet exist. They were different inputs unsuited to one retry command.

The later branches therefore were not merely a tidy folder arrangement. **Errors in completed outputs, original holds, newly found omissions, and geometry repairs for specific names** had different input states and preservation requirements. Early and later years also differed in scale, identity context, and user review scope. The denominators below differ, and some follow-up targets overlap.

| Follow-up path | Starting inputs | New work required | Result retained |
|---|---|---|---|
| Shortened-name pilot | One episode's OCR and two resolved people | Discover short forms and repair geometric boundaries | 10 occurrences / 9 pages |
| Early-year completed-output repair | 230 review-designated pages and existing outputs | Restore originals and reapply specified regions | 227 corrected + 2 already satisfied, 1 excluded → 229 outputs |
| Early-year holds | 2,057 held originals and existing identities/failures | Resolve semantic/geometric issues and produce separate outputs | 2,057 pages locally complete |
| First later-year hold package | 2,230 held pages, episode context, and existing outputs | Repair deltas, restoration, caches, and tokens | Artifacts on 18 pages; partial run |
| Later-year name-omission repair | 2000–2019 OCR, existing targets, and human-review history | Compare new links, omissions, and existing masks together | STOP report: 51 program units; current outputs: 279 pages |
| Separate later-year hold processing | The same 2,230 later-year held pages | User-specified OCR-centered first pass | 195 pages from 2000 + remaining 2,035 completed |
| Later-year name-repair path (supplement) | needs_review, issue, and new bbox guides on completed outputs | Reread pages without stated problems and apply specified corrections | Currently 3,949 target pages |

## How human review was saved and reread also changed

The general app shows 21,009 actual output pages and currently records ok 17,042 / issue 321 / needs_review 3,646. The separate hold app shows held **originals**. After unlinking 2,057 early-year pages and 9 later designated pages, all 2,221 active pages are unreviewed. Even for the same page location, output-based and original-based bboxes needed to be distinguished. [E14](../reference/evidence.md#e14)

Bbox entry was added to initially note-centered review, followed by fixes for unintended submission on Enter with Korean IME and better draft preservation. Sometimes the bbox name field contained a description of a mask error. It was consumed as a problem guide for the next agent, not directly as a name ledger. When an image fingerprint changed, old feedback remained in history and the current version returned to review. [Coordinate code](../historical/review/geometry.js)

On September 14, a separate later-year name-repair package misread these human records. Collecting only entries with notes, boxes, or `issue` counted unresolved problems as 3 pages. But the actual app's Space save could leave an empty `needs_review` entry and a NULL fingerprint; that was still a user mark. Replaying saved history chronologically and recognizing only a later valid `saved ok` as resolution increased the target count to 1,805 pages. Automatic `source_changed` was not an event resolving a manual mark either. This included 4 pages with no candidates, and pages already on the machine-candidate list regained a separate review obligation. [E31](../reference/evidence.md#e31)

## Shortened names of known people: retaining identity and resolving only boundaries

Saved OCR for 28 pages in one episode contained 10 two-syllable name forms for two people. Eight pages had previously been `no_changes`. The first application reached 9 occurrences / 8 pages, with one blocked at the boundary of a following form of address. A detached vowel stroke had been split off as the start of that following text; measured ink width and blank-column boundaries were improved, completing 10 occurrences / 9 pages. [E15](../reference/evidence.md#e15), [original correction function](../historical/names/short_alias.py)

What passed onward was not a new identity, but **resolved identity links and geometry that still failed**. The same candidates were reused without regenerating all OCR, verifying only coordinates and outputs. Other later shortened-name repairs likewise followed new instructions at that time rather than treating the earlier preservation policy as an omission automatically.

## Hold restoration exposed cache and composition problems

The first later-year hold package handled existing processing and unresolved portions of the same episode together. Restoring one region from the original could undo another new mask on the same page. Verification changed from stopping at individual operations to checking old and new targets and protected pixels together in the final composed page. [Render contract](../historical/repair/render_contract.py)

Caching required more than storing success or failure. Reusing prior success after a name's scope changed required validity checks linked to both input and scope. Conversely, discarding valid coordinates when only an identity link changed required separating the physical occurrence from the output identity. A completion path was also added for deferred submissions that had failed midway, using the state left behind. [E17](../reference/evidence.md#e17)

The current database has 58 artifact-history rows but only 18 unique pages, with 15 new physical outputs. This path fixed several errors but did not complete all 2,230 later-year pages. Later composition could receive only its existing results as upper-priority correction layers; a separate path supplied the full later-year hold set.

## Later-year name-omission repair: historical mask records were also an input format

The planning package with corrected review selection moved to the later-year name-omission repair path (`voku-name-repair`). The user wanted less repeated searching and image-first reading, following saved-OCR judgment → code repair → image exceptions. The path was organized to preserve existing identities, episode links, and masks while assessing only missing forms and new context. Its targets were not limited to the 2,230 later-year held pages.

Actual rendering stopped when `.get('box')` was called on a historical receipt with `token_layout=null`. It recorded a name already erased but lacking a placed token. Reading null as “no existing mask” would lose a previously protected region. The repair read explicit `token_rendered=false`, erasure regions, and geometry linked to the same occurrence together, leaving a specific hold only when evidence was insufficient. The frozen input then contained 1,652 null-layout items across 975 pages.

During testing, an absolute path in a copied display mapping pointed to one original output, and test cleanup code deleted the actual display file. It was restored from an immutable backup with the same hash; display paths were then separated from test copies and preservation checks added. This incident led to an actual correction: running in an isolated folder alone did not isolate every reference.

Production subsequently resumed, processed 51/457 program units, and stopped at the user's request. The contemporary report records OCR comparison for 52 program units / 4,401 pages, processing scope of 51 program units / 4,275 pages, 279 output pages, and preservation of 1,805 existing manual-review pages. The 279 current output files exist, but execution files in the corresponding production-state directory no longer remain. Progress counts are therefore grounded in the contemporary STOP record and memory, while output counts are grounded in current physical files. Incorporation into final composition remains unconfirmed. [E31](../reference/evidence.md#e31)

## A resolution path revisiting the same later-year holds (new-boryu)

The separate `new-boryu` initially required actual image inspection on every page in its 2000 engine. The user clarified a preference for a fast OCR-centered first pass followed by their own final visual review. From 2001 onward, it changed to a continuous processor reading saved OCR for held pages. Scope was also set to read the held_pages needed for this task rather than repeatedly reading the entire episode context. [E18](../reference/evidence.md#e18)

The 195 pages from 2000 and 2,035 pages from 2001–2019 were independently completed. The count of 2,835 resolved questions includes 2,364 mechanical geometry resolutions; it does not mean that a human answered 2,835 times. Agent image-check markers, technical verification, `human_approved=false`, and source hold states remained separate. Local outputs later became composition name layers; the procedure did not force the source database into completion.

## Returning review outputs as new correction scope

Supplement's initial 3,646 needs_review pages had no bboxes or notes. Agents had to find the problems in saved OCR. Later, 106 issue pages and 197 new bbox targets brought the current count to 3,949: 3,800 locally complete and 149 unchanged. Exports of 76/200/78 items from a separate later-year review app connect to input snapshots in the next repair package. [E19](../reference/evidence.md#e19)

After final composition, the name-omission audit (`tri-force-gumsu`) used 12,194 approval-processed pages as the name-audit sample scope. The 554 pages without a name layer were not counted immediately as omissions; OCR candidates, current pixels, existing targets, and context were compared. The saved final investigation confirmed omissions on 1,137 pages. The confirmed names were also absent from existing valid target lists, so the report provided grounds to revisit upstream name selection rather than treating the issue as loss during composition handoff. [E32](../reference/evidence.md#e32)

A draft of 436 geometry candidates on 270 pages stopped before rendering or registration. Excluding the 106 already completed pages removed 41 overlaps, leaving 229 guide pages. After excluding 25 user-designated pages and 3 additional pages, 394 separately resolved operations were applied to 201 pages. Bboxes underwent another interpretation from problem-location guides to final erasure regions. Contemporary user decisions about fictional roles, cancelled names, one-character speakers, contact with table rules, and mask margins also formed part of these later inputs.
