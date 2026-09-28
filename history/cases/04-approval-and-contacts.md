# 4. Changing what to redact also changed the geometry problem

[한국어](../../korean/history/cases/04-approval-and-contacts.md)

[History](../HISTORY.md)

## Approval cells: from tracing outside ink to fixed interiors

Early processing addressed stamps/signatures in cells 3 and 5 of a seven-cell approval area, including outside ink. Follow-up work on 3,004 items added and verified blur on 2,632 images, but those changes were restored at the user's rollback request. A report records logs, masks, and output existence/hashes for 66,010 pages returning to the earlier baseline. [E20](../reference/evidence.md#e20)

The criterion then changed to the **interiors** of specified cells. Determining the owner of ink outside a mask became less central; finding the actual seven-cell boundaries became the main problem. Noisy form detection produced 47,481 held/partial pages, followed by improvements using actual horizontal and vertical rules and repeated label widths, with searches narrowed to the top table of each logical panel. Even among the final 339 pages, 96 UI-saved items are distinguished from shared location instructions for the rest.

The user later added cell 7, processing 12,177 cells on 12,175 pages. The current function's default remains `(3,5)`, while call configuration supplies `(3,5,7)`. A single function line therefore cannot establish the latest production scope. [Actual mask code](../historical/approval/masking.py)

After width, height, and station-director-label corrections, current outputs are review 12,194 pages / no_approval 53,816 pages. Rough ROIs were generally **search regions**; only the few exceptions where the user specified the entire rectangle directly matched the final mask.

## Contacts: the discovery ledger did not match actual erased regions

Early Fill processing covered broad OCR lines or combined lines, erasing context while still missing contacts. The record also notes interpreting nilError/0-line results from a fresh OCR environment as clean outputs. After the contemporary report of 3,718 restored pages, white fill with black outlines was adopted. Some early restoration files no longer exist, so that number is cited only from the saved report. [E03](../reference/evidence.md#e03)

On September 22, the user requested tighter masks on the existing 3,518 pages, inclusion of separators, and removal of interior borders between overlapping boxes. But 108 discovery-ledger rows did not match actual masks. Instead of guessing coordinates for restoration, connected components of changed pixels between original and output recovered the physical regions. [Connected-component code](../historical/contacts/recover_components.py), [union-border code](../historical/contacts/paint_union.py), [E21](../reference/evidence.md#e21)

The 48.72% area reduction shows how much tighter the existing masks became. A later gap audit was separate: from a population excluding already processed pages, 82 evidence items on 76 pages were approved and applied as 90 actual regions. Duplicate evidence, fragments of one contact, and physical-region counts are different units.

Of the final 3,594 contact pages, 3,563 belong to numeric years and 31 to Unknown. Only the former entered final numeric-year composition. Separate rules for phonetic Hangul, fragmented contacts, and pencil notes are not retroactively applied to the entire name-only package.

## What the repeated changes meant

These two paths did more than keep refining the same algorithm. Whether to follow outside ink, redact only fixed-cell interiors, treat a bbox as a search guide or resolved region, and include number separators all changed. User judgments about scope changed the problem the next code had to solve.
