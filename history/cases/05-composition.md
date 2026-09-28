# 5. Independent corrections could not be selected as whole images

[한국어](../../korean/history/cases/05-composition.md)

[History](../HISTORY.md) · [Revision history and OCR](06-history-and-final-ocr.md)

## The same original, different revision histories

Initial name outputs, shortened-name repairs, review corrections, hold follow-ups, approval cells, and contacts were all produced separately. No latest file could be assumed to include all earlier edits. The user chose to preserve lower-layer name masks while giving priority to **upper-layer correction regions**. Later instructions added the later-year name-repair path (supplement) as the highest-priority later-year name layer. [E22](../reference/evidence.md#e22)

| Application order: low → high | Name layers |
|---|---|
| 1988–1999 | First-pass names → shortened names → early-year completed-output repair → early-year hold repair |
| 2000–2019 | First-pass names → separate later-year holds → later-year context holds → supplement |
| After names | Approval cells → contacts |

This table is an **explicit priority order for final composition**. It does not mean that the folders were developed in that order from the outset.

## Why a simple image difference was insufficient

As a small hypothetical example, a lower output might redact A and B, while an upper output restores A and redacts C. Selecting the entire upper image loses B; combining only pixels different from the original fails to pass on A's restoration because A now matches the original. In addition to erasure and token regions, **explicitly restored regions** are therefore required. This is an explanatory example, not a substituted real-name case.

In the [original composition code](../historical/composition/compose.py), `name_mask` receives rectangles, previous target regions, mask images, lines, and original-image differences specified by contract. `build_one` compares Pillow composition with NumPy assignment and checks pixels outside authorized regions, decoded saved outputs, and input hashes. Comparing two independent calculation paths checked whether already resolved correction regions passed accurately through composition. Judgments about whether something was a name, whether to restore it, and which layer should take priority came from preceding decisions and user instructions.

## Passing restoration regions into the next layer

Independent corrections used different prior images as their bases. A hold-repair renderer recreating names from an original could produce a file lacking other names already masked in a lower layer. Before using an upper file as a replacement, the receiver therefore needed the regions for which the upper task was actually responsible. Restoration records such as `restore` and `restored_boxes`, together with previous target regions, conveyed correction intent even for pixels returned to the original.

This contract handles what an original-image diff misses. Restored regions have the same color as the original and disappear from the diff, yet the decision to remove a lower mask remains. Conversely, lower name masks must survive where the upper layer did not intervene. This is why authorized name-layer regions were combined first, with approval cells and contacts applied above them. [E22](../reference/evidence.md#e22)

Later incorporation of 201 supplement pages repeated this handoff within a narrow scope. Replayed names, approval cells, and contacts were compared with specified corrections while preserving bytes, hashes, and timestamps of the other 65,809 pages. A report of once generating all 66,010 pages and a receiver receipt confirming later changes to 201 pages record different events. [E23](../reference/evidence.md#e23), [E32](../reference/evidence.md#e32)

## Applied scope

Initial composition covered 66,010 pages in numeric years 1988–2019, explicitly excluding Unknown's 4,413 pages. The contemporary sets of 25,304 pages with name layers, 12,194 approval-cell outputs, and 3,563 contact outputs overlap. The 37,768 pages with no layer were copied from originals. Saved verification reports preservation of 219,031 input files and checks of the full output set, dimensions, hashes, and pixel round trips. [E22](../reference/evidence.md#e22)

A later 3,646-page supplement integration changed 3,494 pages and left 152 identical. Separate integrations followed: issue 106, bbox guide 201, 16 pixel changes among 17 selected pages, and 1,892 pixel changes among 1,893 ready pages. These cohorts can overlap and must not be added into a total of unique corrected pages. [E23](../reference/evidence.md#e23)

## Reading producer and receiver records together

An exported package's `source_merged=false` can coexist with a later receiver integration report. Reading the earlier producer state alone misses later actual application; applying the later receiver state retroactively distorts the completion boundary at that time. The current 1,539 ready pages connect to 1,538 applied pages in the final backup and one separate page correction. The 15-page staff correction unconfirmed in the original folder notes also connects through receiver receipts. [E23, E25](../reference/evidence.md#e25)

The current contents of `reports/final_verification.json` concern the later 1,893-page integration, not the initial complete composition. The initial report was compared against a preserved before-copy. Neither filenames nor a “final” title determined time and scope.

Supplement, bbox guides, local name repairs, and typography changes continued after initial complete composition. The receiver therefore needed to preserve not just one plan, but later correction scopes, order, previous images, and receipts. This leads into the next case's historical-token replay problem.
