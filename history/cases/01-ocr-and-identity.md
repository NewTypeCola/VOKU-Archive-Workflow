# 1. OCR recovery and identity reconstruction were different kinds of success

[한국어](../../korean/history/cases/01-ocr-and-identity.md)

[History](../HISTORY.md) · [Changes in reading operations](02-reading-and-state.md)

## Initial assumptions and problems exposed by human review

The initial personal-information processing plan (P0-4.5) prioritized names but also sought to handle student IDs, departments, and approval cells. It envisioned building a private roster, collecting candidates broadly, obtaining human decisions, and applying them to images. Its scope differs from the later **name-only first-pass package**. [E01](../reference/evidence.md#e01)

The analysis of 513 human reviews on 2026-08-24 records 151 name entries and 131 name corrections. Of those 131 corrections, 61 already existed in one of the two OCR sources, while 70 were missed by both. Human judgment changed 108 machine-held cases into redaction targets. Whether a candidate was visible, whether the characters were correct, who the person was, and how much to erase were separate failures. [E04](../reference/evidence.md#e04)

The original review ledger also included notes meaning ordinary non-station-member individuals stored alongside `PUBLIC_PERSON_EXCLUDE`. A formally valid state did not express the intended protection scope correctly. Rather than simply overwriting it with a human answer, this became a problem of separating classification axes again.

## Better OCR did not immediately mean more candidates

| Limited experiment | Actual result | What it left for the next judgment |
|---|---|---|
| OCR retry on 13 known printed failures | Exact 7 / partial 4 / unrecovered 2 / confidently wrong 0 | Evidence for adding recovered forms to existing observations |
| OCR retry on 56 handwritten/mixed cases | Exact 22 / partial 11 / unrecovered 14 / confidently wrong 9 | Limited override materials retaining wrong and unrecovered cases separately |
| Add recovery OCR to the existing 513-case evaluation | Existing 440/440 targets preserved; 0 newly exposed targets; 0 existing IDs rewritten | Evaluate form improvement separately from candidate exposure; retain the remaining HOLD-exposure problem |

New forms were attached to existing observations as **additional evidence**. Existing Rough/Fresh OCR was not erased. Better form quality and evidence in an evaluation already recovering candidates were not counted as an increase in candidate numbers; review exposure of the remaining 17 HOLD cases was a separate issue. At this experimental stage, complete candidate generation and image redaction had not started. [E05](../reference/evidence.md#e05)

## A tool-use incident separate from the technical experiment

During the handwriting experiment, it was discovered that a local image-reading path had uploaded a montage of crops from four cases to external storage. That path was stopped, and work returned to fixed local evidence. [E05](../reference/evidence.md#e05)

## The large identity model ran, but image processing was still not complete

Large-scale identity reconstruction (P0-4.5v2 attempt 008) ran over 70,423 pages / 5,719 documents: 66,010 pages / 5,330 documents from numeric years plus Unknown's 4,413 pages / 389 documents. Instead of making every combination of the same name, it connected only evidence meeting eligibility conditions. It retained 598,223 incomplete combinations as an aggregate without expanding them into individual relationships. It also reclassified 1,311 probable occurrences with unresolved local affiliation. [Actual code](../historical/identity/global_identity_v3.py), [E06](../reference/evidence.md#e06)

Candidate semantic repair (attempt 009) separated structured name slots, affiliation, academic information, and identity hypotheses. It fixed an intermediate QA failure displaying 16 `UNRESOLVED_BINDING` cases as `NOT_STATED`; final independent verification was 99/99. Nevertheless, `candidate_only=true`, while public-token use and redaction execution remained false. What passed verification was **candidate reconstruction**. [E07](../reference/evidence.md#e07)

## Direct images and more verification were not automatic answers either

On August 30, the blind pilot prepared reading bundles for 100 broadcasts / 270 full pages, but there were no 100 model responses. In a separate direct-image reading, the agent repeatedly fixated on a misread name until the user pointed out the last syllable; an enlarged rereading then corrected it. Seeing repeated forms and obtaining independent evidence were different. [E08](../reference/evidence.md#e08)

In the September 1 roster integration, the verifier was the more important failure point. The 2017 input had 2 `input_incomplete` cases and 1 `blocked` case, but both the generator and fixed evaluator missed them and reported `complete` with 0 input problems. This was discovered after 57 tests and Cycle 00 had passed. Cycle 01 was stopped; Cycle 02 and publication of final outputs did not proceed. [E09](../reference/evidence.md#e09)

Role-based roster work in early September also left separately reintegrated yearly outputs. A separate integration for 2006–2019 recorded 281 year-specific people, 969 assignments, and 204 review items. It too needed to retain confirmed, candidate, and conflicting cases separately. However, inheritance of every row into the later operational roster is not linked by the evidence. [E35](../reference/evidence.md#e35)

The confirmed transition here was to treat OCR forms, candidate exposure, identity hypotheses, and actual image application as different outputs. Recovery OCR remained beside existing observations, identity reconstruction retained candidate status, and flawed merge verification became a stop report. Later saved-OCR processing again faced the need to inherit resolved identities separately from failed geometry. Specific handoffs and branches continue in [Case 2](02-reading-and-state.md).
