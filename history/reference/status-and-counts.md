# States and numerical denominators

[한국어](../../korean/history/reference/status-and-counts.md)

The counting reference date is 2026-09-26. Distinguish values current at that investigation from values at specific historical points. **Do not add overlapping cohorts.**

| Count | Denominator, time, and evidence | State and interpretation |
|---|---|---|
| 70,423 pages / 5,719 documents | Numeric years: 66,010 pages / 5,330 documents + Unknown: 4,413 pages / 389 documents, E02/E06 | Scope of early reconstruction, different from the final numeric-year scope |
| 66,010 pages / 5,330 documents | Numeric years 1988–2019, E02/E24 | Physical final-image files and OCR objects were directly recounted during the investigation |
| 4,413 pages / 389 documents | Unknown, E02 | Excluded from final numeric-year composition |
| 4,879 PASS / 420 REVIEW / 31 FAIL | Initial OCR quality for 5,330 documents, E02 | Quality states remaining separately from 100% OCR generation |
| 21,009 / 40,714 / 4,182 / 105 pages | Current first-pass DB: verified/no_changes/partial/hold, E12 | The four states total 66,010 pages |
| 2,768 / 1,087 / 426 / 6 pages | Mechanical-only/semantic-only/both/empty partition of 4,287 held pages, E12 | Page counts, not error-occurrence or person counts |
| 17,042 / 321 / 3,646 pages | Current general review DB: ok/issue/needs states, E14 | Covers 21,009 pages; app-state counts are distinct from final overall approval |
| 2,057 / 2,230 pages | Early/later-year hold targets, E16–18 | The first later-year package's partial run is counted separately from later hold-resolution path (new-boryu) completion |
| 3,949 = 3,800 + 149 pages | Current supplement scope, E19 | Locally complete plus unchanged; targets comprise 3,646+106+197 pages |
| 12,194 / 53,816 pages | Approval-cell review/noapproval states, E20 | Partition by approval-cell processing state |
| 3,594 = 3,563 + 31 pages | Current contact outputs: numeric years + Unknown, E21 | Only 3,563 pages entered numeric-year composition |
| 37,768 pages | Pages with no layers in initial composition, E22 | Originals were copied; this state is separate from clean status or publication approval |
| 1,893 → 1,892 pages | Later integration targets → pages with actual pixel changes, E23 | One page had identical pixels; a different time from the current 1,539 ready pages |
| 1,538 + separate 1 page | Final receiver connection for 1,539 later ready pages, E23 | Overlaps the earlier 1,893 pages; adding them does not give unique corrections |
| 1,990,913 → 1,992,139 → 1,992,146 → 1,992,165 lines | First/second complete OCR → 62 name pages → 52 contact pages, E24 | The last value was directly counted during investigation; changes in line counts are distinct from recognition-accuracy metrics |

## Additional intermediate paths confirmed

| Count | Time and evidence | Distinction for later work |
|---|---|---|
| 17 pages = 11 verified + 6 no_changes | Last isolated geometry-test (tmptest) run, E27 | Code was incorporated, but the test DB was not merged |
| 85 / 4,009 / 61,916 pages | Single-agent reading alternative (read-v2) ZIP DB: read/inherited/pending, E28 | 85 newly text-read pages; 0 new images |
| 82 pages = 11 + 64 + 7 | Actual session-input alternative (read-next) submission, E29 | verified/no_changes/partial partition; 18 physical outputs |
| 1,805 pages = 1,803 + 2 | Manual-review selection correction on 9/14, E31 | Contemporary needs_review/issue states; a different time from the app's current 3,646 pages |
| 51/457 program units; 279 output pages | Later-year name-omission repair (name-repair) STOP report and current files, E31 | Progress comes from the saved report; outputs were directly counted from current files |
| 59 episodes / 644 pages / 210 output pages | OCR line-rewriting receipts, E34 | Includes execution after the intermediate summary of 40 episodes / 153 output pages |
| 1,137 confirmed pages; 20 needing further judgment | Final name-omission audit (tri-force-gumsu), E32 | The two sets overlap by 2 pages; 0 pages were modified in this investigation stage |
| 270 → 229 → 201 pages | Geometry draft → guides → actual application, E19/E32 | Remove 41 overlaps with the existing 106 pages, then exclude another 28 pages |

## What “complete” refers to

| Expression | Actual meaning | State or scope to distinguish |
|---|---|---|
| Packet created/delivered | Input is ready | Actual reading and submission require later records |
| Formal reading submission | Decision scope, quotations, format, and state were saved | Submission state differs from subsequent review state |
| verified | Passed the rendering/geometric checks at that time | Human approval is a separate state |
| local_completed | Target processing finished in an independent workspace | Source-DB hold release and merge status require separate confirmation |
| human_approved=false | No human approval was recorded | It does not mean mechanical failure or that every page was unseen |
| Approval field absent | The field is missing | Do not arbitrarily convert it to false or true |
| integration/merge receipt | Actually incorporated on the receiver side | It does not retroactively change the producer's historical state document |
| Output-set match | Structure and coverage match the specified output set | The check concerns that specified set |

## Conflicts resolved or retained

- The user's “13” versus 14 actual notes: 13 newly analyzed notes plus 1 existing contact note. Administrative records confirmed the difference.
- Copy manifest with 81,835 rows versus README with 81,836: the observed difference is retained. A header explanation was not asserted as fact.
- P0 plan's 70,424 pages versus 70,423 observed: a separate unresolved gate in that early experiment, not overwritten with the final 66,010-page count.
- No complete fresh OCR in game, but complete OCR in final: different times and work locations. The earlier plan was connected to later execution.
- Producer unmerged state versus later receiver integration: a time difference, supplemented by receiver receipts.
- Latest file named final_verification versus contents covering a 1,893-page subset: the initial complete report was traced through an archived before-copy.
- Old partial physical files versus partial 0 in the current manifest: file existence was distinguished from current selection state.
- read-v2/read-next construction reports saying not started versus later submissions: post-construction execution was added from archived databases, sessions, and receipts.
- Early incomplete investigation in tri-force-gumsu memory versus a saved final report: later AUDIT_COMPLETE and summary records strengthened the investigation result.
