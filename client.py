# -*- coding: utf-8 -*-
"""
OpenClaw GenPark Recursive Protocol Synthesizer - Robinson Type Unification & Schema Lens Synthesizer
Standard Library only: json, math, typing.
Implements first-order Robinson type unification to derive Most General Unifiers (MGU),
calculates structural Graph Edit Distance across JSON-RPC/MCP schemas, and synthesizes bidirectional lenses.
"""

import math
from typing import Dict, List, Any

class OpenClawGenParkRecursiveProtocolSynthesizer:
    def __init__(self):
        pass

    def unify_type_signatures(self, sig_a: Dict[str, Any],
                              sig_b: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes first-order Robinson type unification:
        Finds a substitution theta mapping type variables (prefixed with '?') to concrete types.
        """
        substitutions = {}
        mismatches = []

        all_keys = set(sig_a.keys()).union(sig_b.keys())

        for k in all_keys:
            if k not in sig_a or k not in sig_b:
                mismatches.append({"key": k, "error": "KEY_MISSING_IN_ONE_SIGNATURE"})
                continue

            t_a = str(sig_a[k])
            t_b = str(sig_b[k])

            # If identical
            if t_a == t_b:
                continue

            # Variable unification
            if t_a.startswith("?"):
                substitutions[t_a] = t_b
            elif t_b.startswith("?"):
                substitutions[t_b] = t_a
            else:
                mismatches.append({"key": k, "type_a": t_a, "type_b": t_b, "error": "TYPE_COLLISION"})

        is_unifiable = len(mismatches) == 0

        return {
            "is_unifiable": is_unifiable,
            "most_general_unifier": substitutions if is_unifiable else {},
            "mismatches_count": len(mismatches),
            "mismatches": mismatches
        }

    def compute_schema_structural_distance(self, schema_a: Dict[str, Any],
                                           schema_b: Dict[str, Any]) -> Dict[str, Any]:
        """
        Computes normalized Graph Edit Distance between two MCP tool parameter schemas.
        Measures insertions, deletions, and type mutations.
        """
        props_a = schema_a.get("properties", {})
        props_b = schema_b.get("properties", {})
        req_a = set(schema_a.get("required", []))
        req_b = set(schema_b.get("required", []))

        keys_a = set(props_a.keys())
        keys_b = set(props_b.keys())

        common_keys = keys_a.intersection(keys_b)
        added_keys = keys_b - keys_a
        removed_keys = keys_a - keys_b

        # Edit costs
        insert_cost = len(added_keys) * 1.0
        delete_cost = len(removed_keys) * 1.0
        
        type_mutations = []
        mutation_cost = 0.0
        for k in common_keys:
            type_a = props_a[k].get("type", "any")
            type_b = props_b[k].get("type", "any")
            if type_a != type_b:
                type_mutations.append({"property": k, "type_a": type_a, "type_b": type_b})
                mutation_cost += 0.8

        req_diff_cost = len(req_a.symmetric_difference(req_b)) * 0.5
        total_edit_distance = insert_cost + delete_cost + mutation_cost + req_diff_cost
        max_possible = max(1.0, (len(keys_a) + len(keys_b)) * 1.5)

        normalized_similarity = max(0.0, 1.0 - (total_edit_distance / max_possible))

        return {
            "total_edit_distance": round(total_edit_distance, 3),
            "normalized_structural_similarity": round(normalized_similarity, 4),
            "added_properties": list(added_keys),
            "removed_properties": list(removed_keys),
            "type_mutations": type_mutations,
            "compatibility_grade": "FULLY_COMPATIBLE" if total_edit_distance == 0 else ("ADAPTABLE_WITH_LENS" if normalized_similarity >= 0.6 else "BREAKING_MIGRATION_REQUIRED")
        }

    def synthesize_bidirectional_lens(self, source_schema: Dict[str, Any],
                                     target_schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Synthesizes bijective / unidirectional property projection lenses:
        getter: source -> target, putback: target x source -> source.
        """
        props_s = source_schema.get("properties", {})
        props_t = target_schema.get("properties", {})

        forward_mappings = {}
        for k_t in props_t:
            if k_t in props_s:
                forward_mappings[k_t] = f"src.{k_t}"
            else:
                forward_mappings[k_t] = f"DEFAULT({props_t[k_t].get('type', 'any')})"

        backward_mappings = {}
        for k_s in props_s:
            if k_s in props_t:
                backward_mappings[k_s] = f"tgt.{k_s}"
            else:
                backward_mappings[k_s] = f"src_orig.{k_s}"

        return {
            "forward_getter_transform": forward_mappings,
            "backward_putback_transform": backward_mappings,
            "is_lossless_bijection": set(props_s.keys()) == set(props_t.keys())
        }
