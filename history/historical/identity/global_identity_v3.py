"""Eligibility-first global identity planning for semantic revision 3.0.0.

The planner deliberately separates three things that the predecessor mixed:

* aggregate same-name blocking statistics;
* individually supported contested relations; and
* positive identity edges that may be unioned.

No same-name Cartesian product is ever retained.  Incomplete-core buckets produce
one aggregate HOLD row, while positive components use only a deterministic
spanning forest of independently supported edges.
"""
from __future__ import annotations

import collections

from v2_io import cj, compact, sid
from v2_member_rules import identity_core
from v2_assembly_rules import Union, independent_contexts


BLOCKING_HUMAN_CLASSES = frozenset({"PRIVATE_NONSTAFF", "NON_PERSON", "UNRESOLVED"})


def _refs(rows):
    found = {}
    for row in rows:
        for ref in row.get("source_refs") or []:
            found[cj(ref)] = ref
    return [found[key] for key in sorted(found)]


def source_packet(m):
    """Return an auditable strict-core/positive-edge eligibility proof."""
    core = identity_core(m)
    proof = {
        "identity_core_complete": core is not None,
        "local_identity_resolved": m.get("local_identity_status") == "LOCAL_IDENTITY_RESOLVED",
        "academic_exact_source_eligible": m.get("academic_exact_source_eligible") is True,
        "source_refs_present": bool(m.get("source_refs")),
        "broadcast_context_present": bool(m.get("broadcast_segment_id")),
        "independent_content_hash_present": bool(m.get("independent_content_hashes")),
        "human_guard_clear": not bool(set(m.get("human_guard_classes") or []) & BLOCKING_HUMAN_CLASSES)
        and not m.get("human_identity_conflict", False),
        "station_affiliation_confirmed": m.get("station_affiliation_status") == "AFFILIATION_CONFIRMED_MACHINE",
    }
    proof["strict_core_eligible"] = all(
        proof[key]
        for key in (
            "identity_core_complete",
            "local_identity_resolved",
            "academic_exact_source_eligible",
            "source_refs_present",
            "broadcast_context_present",
            "independent_content_hash_present",
            "human_guard_clear",
        )
    )
    proof["positive_edge_endpoint_eligible"] = (
        proof["strict_core_eligible"] and proof["station_affiliation_confirmed"]
    )
    return proof


def _relation(rid, kind, a, b, members, refs, origin, extra=None):
    left, right = sorted((a, b))
    ma, mb = members[left], members[right]
    row = {
        "id": rid,
        "local_member_a": left,
        "local_member_b": right,
        "relation_kind": kind,
        "relation_origin": origin,
        "risk_active": True,
        "risk_type": kind,
        "all_risk_reasons": [kind],
        "current_endpoint_combinations": [[left, right]],
        "independently_supported_contested_relation": True,
        "same_name_only_relation": False,
        "automatic_split": False,
        "automatic_person_promotion": False,
        "role_difference_alone_is_not_split_authority": True,
        "core_a": list(identity_core(ma)) if identity_core(ma) else None,
        "core_b": list(identity_core(mb)) if identity_core(mb) else None,
        "source_refs": refs,
    }
    if extra:
        row.update(extra)
    return row


def _forest(members):
    """Build a deterministic forest without retaining the compatible pair graph."""
    ordered = sorted(members, key=lambda row: row["id"])
    union = Union(row["id"] for row in ordered)
    edges = []
    for index, right in enumerate(ordered):
        connected_roots = set()
        for left in ordered[:index]:
            lroot = union.find(left["id"])
            rroot = union.find(right["id"])
            if lroot == rroot or lroot in connected_roots:
                continue
            if not independent_contexts(left, right):
                continue
            edge = {
                "id": sid("PERSON_IDENTITY_EDGE_V3", left["id"], right["id"]),
                "local_member_a": min(left["id"], right["id"]),
                "local_member_b": max(left["id"], right["id"]),
                "edge_kind": "STRICT_POSITIVE_IDENTITY_FOREST_EDGE",
                "input_entity_type": "BROADCAST_LOCAL_MEMBER",
                "source_bound_name_academic_cohort": True,
                "independent_source_contexts": True,
                "same_name_only": False,
                "human_conflict": False,
                "temporal_stage_progression_inferred": False,
                "positive_union_authority": True,
                "source_refs": _refs((left, right)),
            }
            edges.append(edge)
            connected_roots.add(lroot)
            union.union(left["id"], right["id"])
    return edges, [ids for ids in union.groups() if len(ids) > 1]


def plan_global_identity(members, baseline_relations=(), max_relation_rows=25_000):
    """Return bounded semantic products from source-bound local members.

    ``baseline_relations`` contains one predecessor homonym record and its two
    separately mapped endpoint sets.  Ambiguous endpoint maps are retained as
    aggregate audit rows and are never expanded into their Cartesian product.
    """
    member_map = {row["id"]: row for row in members}
    by_name = collections.defaultdict(list)
    by_core = collections.defaultdict(list)
    packets = {}
    for member in member_map.values():
        packets[member["id"]] = source_packet(member)
        if member.get("name"):
            by_name[compact(member["name"])].append(member)
        core = identity_core(member)
        if core:
            by_core[core].append(member)

    theoretical_pairs = 0
    incomplete_theoretical_pairs = 0
    aggregate_holds = []
    for name, bucket in sorted(by_name.items()):
        total = len(bucket)
        complete = sum(identity_core(row) is not None for row in bucket)
        all_pairs = total * (total - 1) // 2
        complete_pairs = complete * (complete - 1) // 2
        incomplete_pairs = all_pairs - complete_pairs
        theoretical_pairs += all_pairs
        incomplete_theoretical_pairs += incomplete_pairs
        if incomplete_pairs:
            aggregate_holds.append(
                {
                    "id": sid("IDENTITY_AGGREGATE_HOLD_V3", "INCOMPLETE_CORE", name),
                    "hold_kind": "INCOMPLETE_CORE_SAME_NAME_AGGREGATE_HOLD",
                    "normalized_name": name,
                    "local_member_ids": sorted(row["id"] for row in bucket),
                    "bucket_member_count": total,
                    "complete_core_member_count": complete,
                    "incomplete_core_member_count": total - complete,
                    "theoretical_pair_count_not_materialized": incomplete_pairs,
                    "materialized_pair_count": 0,
                    "individual_review_question_created": False,
                    "source_refs": _refs(bucket),
                }
            )

    relations = []
    baseline_audit_rows = []
    blocked_same_core = set()
    for old in sorted(baseline_relations, key=lambda row: row["id"]):
        left_ids = sorted(set(old.get("mapped_a_ids") or []))
        right_ids = sorted(set(old.get("mapped_b_ids") or []))
        extra = {
            "v1_homonym_pair_id": old["id"],
            "legacy_risk_type_audit_only": old.get("risk_type"),
            "mapped_a_count": len(left_ids),
            "mapped_b_count": len(right_ids),
        }
        if len(left_ids) == len(right_ids) == 1 and left_ids[0] != right_ids[0]:
            a, b = left_ids[0], right_ids[0]
            ca, cb = identity_core(member_map[a]), identity_core(member_map[b])
            if ca and cb and ca != cb:
                kind = "EXACT_SOURCE_BOUND_CORE_CONFLICT_SAME_NAME"
            elif ca and ca == cb and member_map[a].get("broadcast_segment_id") == member_map[b].get("broadcast_segment_id"):
                kind = "EXACT_PHYSICAL_SLOT_SAME_CORE_CONTRADICTION"
                blocked_same_core.update((a, b))
            elif not ca or not cb:
                kind = "EXACT_LEGACY_CONTESTED_RELATION_INCOMPLETE_CORE"
                blocked_same_core.update((a, b))
            else:
                kind = "EXACT_LEGACY_CONTESTED_IDENTITY_RELATION"
                blocked_same_core.update((a, b))
            row = _relation(
                sid("HOMONYM_PAIR_V3", "V1", old["id"]), kind, a, b,
                member_map, old.get("source_refs") or _refs((member_map[a], member_map[b])),
                "DECLARED_PREDECESSOR_EXACT_RELATION", extra,
            )
            relations.append(row)
            baseline_audit_rows.append(row)
        else:
            hold = {
                "id": sid("IDENTITY_AGGREGATE_HOLD_V3", "LEGACY_ENDPOINT", old["id"]),
                "hold_kind": "LEGACY_CONTESTED_RELATION_ENDPOINT_MAP_AGGREGATE_HOLD",
                "v1_homonym_pair_id": old["id"],
                "mapped_a_ids": left_ids,
                "mapped_b_ids": right_ids,
                "mapped_a_count": len(left_ids),
                "mapped_b_count": len(right_ids),
                "theoretical_pair_count_not_materialized": len(left_ids) * len(right_ids),
                "materialized_pair_count": 0,
                "individual_review_question_created": False,
                "source_refs": old.get("source_refs") or [],
            }
            aggregate_holds.append(hold)
            baseline_audit_rows.append(
                {
                    "id": sid("HOMONYM_PAIR_V3", "V1", old["id"]),
                    "v1_homonym_pair_id": old["id"],
                    "local_member_a": None,
                    "local_member_b": None,
                    "current_endpoint_combinations": [],
                    "risk_active": True,
                    "risk_type": "LEGACY_ENDPOINT_MAP_AGGREGATE_HOLD",
                    "all_risk_reasons": ["LEGACY_ENDPOINT_MAP_AGGREGATE_HOLD"],
                    "independently_supported_contested_relation": True,
                    "aggregate_only": True,
                    "aggregate_hold_id": hold["id"],
                    "automatic_split": False,
                    "automatic_person_promotion": False,
                    "role_difference_alone_is_not_split_authority": True,
                    "source_refs": old.get("source_refs") or [],
                    **extra,
                }
            )

    # A same core in two physical slots of one broadcast is a real contested
    # relation.  Retain a star, not all slot combinations.
    for core, core_members in sorted(by_core.items()):
        by_broadcast = collections.defaultdict(list)
        for member in core_members:
            by_broadcast[member.get("broadcast_segment_id")].append(member)
        for broadcast, bucket in sorted(by_broadcast.items(), key=lambda item: str(item[0])):
            bucket = sorted(bucket, key=lambda row: row["id"])
            if len(bucket) < 2:
                continue
            anchor = bucket[0]
            blocked_same_core.update(row["id"] for row in bucket)
            for other in bucket[1:]:
                relations.append(
                    _relation(
                        sid("HOMONYM_PAIR_V3", "PHYSICAL_SLOT", anchor["id"], other["id"]),
                        "EXACT_PHYSICAL_SLOT_SAME_CORE_CONTRADICTION",
                        anchor["id"], other["id"], member_map, _refs((anchor, other)),
                        "CURRENT_SOURCE_PHYSICAL_SLOT_CONTRADICTION",
                        {"broadcast_segment_id": broadcast, "v1_homonym_pair_id": None},
                    )
                )

    # Distinct complete cores under one name are semantically contested.  One
    # representative row per source-supported core pair is sufficient.
    for name, bucket in sorted(by_name.items()):
        cores = collections.defaultdict(list)
        for member in bucket:
            core = identity_core(member)
            if core:
                cores[core].append(member)
        core_keys = sorted(cores)
        for i, left_core in enumerate(core_keys):
            for right_core in core_keys[i + 1:]:
                left = sorted(cores[left_core], key=lambda row: row["id"])[0]
                right = sorted(cores[right_core], key=lambda row: row["id"])[0]
                relations.append(
                    _relation(
                        sid("HOMONYM_PAIR_V3", "CORE_CONFLICT", left_core, right_core),
                        "EXACT_SOURCE_BOUND_CORE_CONFLICT_SAME_NAME",
                        left["id"], right["id"], member_map, _refs((left, right)),
                        "CURRENT_COMPLETE_CORE_CONFLICT",
                        {"v1_homonym_pair_id": None, "normalized_name": name},
                    )
                )

    # De-duplicate current relations by semantic endpoint/kind while preserving
    # every declared predecessor audit row separately.
    seen_current = set()
    deduplicated_relations = []
    for row in relations:
        if row.get("v1_homonym_pair_id"):
            deduplicated_relations.append(row)
            continue
        key = (row["relation_kind"], row["local_member_a"], row["local_member_b"])
        if key not in seen_current:
            seen_current.add(key)
            deduplicated_relations.append(row)
    relations = deduplicated_relations

    positive_edges = []
    confirmed_components = []
    probable_candidates = []
    member_candidate = {}
    confirmed_member_person = {}
    for core, core_members in sorted(by_core.items()):
        eligible = [
            row for row in core_members
            if packets[row["id"]]["positive_edge_endpoint_eligible"]
            and row["id"] not in blocked_same_core
        ]
        edges, components = _forest(eligible)
        edge_by_member = collections.defaultdict(list)
        for edge in edges:
            edge_by_member[edge["local_member_a"]].append(edge["id"])
            edge_by_member[edge["local_member_b"]].append(edge["id"])
        confirmed_ids = set()
        for ids in components:
            rows = [member_map[mid] for mid in ids]
            person_id = sid("PERSON_V3_CONFIRMED", core, ids)
            candidate_id = sid("PERSON_CANDIDATE_V3", "CONFIRMED", person_id)
            component = {
                "id": candidate_id,
                "person_candidate_id": candidate_id,
                "status": "CONFIRMED",
                "person_id": person_id,
                "local_member_ids": ids,
                "input_entity_type": "BROADCAST_LOCAL_MEMBER",
                "identity_core": list(core),
                "broadcast_segment_ids": sorted({row["broadcast_segment_id"] for row in rows}),
                "independent_content_hashes": sorted({value for row in rows for value in row["independent_content_hashes"]}),
                "source_supported_identity_edge_ids": sorted({eid for mid in ids for eid in edge_by_member[mid]}),
                "same_name_only_merge": False,
                "academic_cohort_exact_match": True,
                "independent_context_requirement_met": True,
                "station_affiliation_confirmed_for_all_members": True,
                "final_canonical_person": True,
                "provisional": False,
                "token": None,
                "source_refs": _refs(rows),
            }
            confirmed_components.append(component)
            confirmed_ids.update(ids)
            for mid in ids:
                member_candidate[mid] = candidate_id
                confirmed_member_person[mid] = person_id
        for edge in edges:
            owner = next((c for c in confirmed_components if edge["local_member_a"] in c["local_member_ids"]), None)
            if owner:
                edge["person_candidate_id"] = owner["id"]
                edge["person_id"] = owner["person_id"]
                edge["active_confirmed_edge"] = True
                positive_edges.append(edge)
        remaining = sorted(row["id"] for row in core_members if row["id"] not in confirmed_ids)
        if remaining:
            rows = [member_map[mid] for mid in remaining]
            candidate_id = sid("PERSON_CANDIDATE_V3", "PROBABLE", core, remaining)
            probable = {
                "id": candidate_id,
                "person_candidate_id": candidate_id,
                "status": "PROBABLE",
                "person_id": None,
                "local_member_ids": remaining,
                "input_entity_type": "BROADCAST_LOCAL_MEMBER",
                "identity_core": list(core),
                "broadcast_segment_ids": sorted({row["broadcast_segment_id"] for row in rows}),
                "independent_content_hashes": sorted({value for row in rows for value in row["independent_content_hashes"]}),
                "source_supported_identity_edge_ids": [],
                "reason": "STRICT_POSITIVE_COMPONENT_REQUIREMENTS_NOT_ALL_MET",
                "endpoint_eligibility_counts": dict(collections.Counter(
                    "ELIGIBLE" if packets[mid]["positive_edge_endpoint_eligible"] else "INELIGIBLE"
                    for mid in remaining
                )),
                "same_name_only_merge": False,
                "final_canonical_person": False,
                "provisional": True,
                "token": None,
                "source_refs": _refs(rows),
            }
            probable_candidates.append(probable)
            for mid in remaining:
                member_candidate.setdefault(mid, candidate_id)

    conflict_union = Union()
    conflict_relation_ids = collections.defaultdict(list)
    for row in relations:
        a, b = row.get("local_member_a"), row.get("local_member_b")
        if not a or not b:
            continue
        conflict_union.union(a, b)
        conflict_relation_ids[a].append(row["id"])
        conflict_relation_ids[b].append(row["id"])
    conflict_components = []
    member_conflict = {}
    for ids in conflict_union.groups():
        cid = sid("IDENTITY_CONFLICT_COMPONENT_V3", ids)
        rows = [member_map[mid] for mid in ids]
        relation_ids = sorted({rid for mid in ids for rid in conflict_relation_ids[mid]})
        component = {
            "id": cid,
            "status": "CONFLICT",
            "local_member_ids": ids,
            "contested_relation_ids": relation_ids,
            "positive_union_applied": False,
            "transitive_identity_truth": False,
            "person_id": None,
            "token": None,
            "source_refs": _refs(rows),
        }
        conflict_components.append(component)
        for mid in ids:
            member_conflict[mid] = cid

    if len(relations) > max_relation_rows:
        raise RuntimeError("GLOBAL_IDENTITY_RELATION_BUDGET_EXCEEDED")
    if len(positive_edges) > max_relation_rows:
        raise RuntimeError("GLOBAL_IDENTITY_POSITIVE_EDGE_BUDGET_EXCEEDED")

    dispositions = []
    for mid, member in sorted(member_map.items()):
        person_id = confirmed_member_person.get(mid)
        candidate_id = member_candidate.get(mid)
        conflict_id = member_conflict.get(mid)
        if person_id:
            disposition = "LINKED_TO_CONFIRMED_CANONICAL_PERSON"
        elif conflict_id:
            disposition = "MEMBER_OF_IDENTITY_CONFLICT"
        elif candidate_id:
            disposition = "PROBABLE_GLOBAL_IDENTITY"
        elif identity_core(member) is None:
            disposition = "UNRESOLVED_INCOMPLETE_CORE"
        else:
            disposition = "UNRESOLVED_GLOBAL_IDENTITY"
        dispositions.append(
            {
                "id": sid("MEMBER_PERSON_DISPOSITION_V3", mid),
                "local_member_id": mid,
                "person_candidate_id": candidate_id,
                "person_id": person_id,
                "identity_conflict_component_id": conflict_id,
                "disposition": disposition,
                "terminal_disposition_count": 1,
                "source_refs": member.get("source_refs") or [],
            }
        )

    materialized_endpoint_relations = sum(
        bool(row.get("local_member_a") and row.get("local_member_b")) for row in relations
    )
    stats = {
        "local_member_count": len(member_map),
        "normalized_name_bucket_count": len(by_name),
        "theoretical_same_name_pair_count": theoretical_pairs,
        "incomplete_core_theoretical_pair_count_not_materialized": incomplete_theoretical_pairs,
        "aggregate_hold_count": len(aggregate_holds),
        "baseline_audit_relation_count": len(baseline_audit_rows),
        "materialized_contested_relation_count": materialized_endpoint_relations,
        "positive_forest_edge_count": len(positive_edges),
        "confirmed_person_count": len(confirmed_components),
        "probable_candidate_count": len(probable_candidates),
        "conflict_component_count": len(conflict_components),
        "incomplete_core_pair_rows_materialized": 0,
        "relation_budget": max_relation_rows,
        "relation_budget_pass": materialized_endpoint_relations <= max_relation_rows,
        "materialized_relations_are_not_name_cartesian_product": True,
    }
    return {
        "stats": stats,
        "source_packets": packets,
        "aggregate_holds": aggregate_holds,
        "baseline_audit_rows": baseline_audit_rows,
        "contested_relations": relations,
        "positive_edges": positive_edges,
        "confirmed_components": confirmed_components,
        "probable_candidates": probable_candidates,
        "conflict_components": conflict_components,
        "member_dispositions": dispositions,
    }
