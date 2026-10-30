# -*- coding: utf-8 -*-
from client import OpenClawGenParkRecursiveProtocolSynthesizer

synth = OpenClawGenParkRecursiveProtocolSynthesizer()

# 1. Type Unification (Robinson)
sig1 = {"user_id": "string", "amount": "?T_val", "callback": "?T_func"}
sig2 = {"user_id": "string", "amount": "float64", "callback": "callable"}
mgu = synth.unify_type_signatures(sig1, sig2)
print(f"Type Unification: Unifiable={mgu['is_unifiable']}, MGU={mgu['most_general_unifier']}")

# 2. Schema Edit Distance
schema_v1 = {
    "properties": {"query": {"type": "string"}, "limit": {"type": "integer"}},
    "required": ["query"]
}
schema_v2 = {
    "properties": {"query": {"type": "string"}, "limit": {"type": "number"}, "filter": {"type": "string"}},
    "required": ["query", "limit"]
}
dist = synth.compute_schema_structural_distance(schema_v1, schema_v2)
print(f"\nSchema Distance: Edit Dist={dist['total_edit_distance']}, Similarity={dist['normalized_structural_similarity']} ({dist['compatibility_grade']})")

# 3. Bidirectional Lens
lens = synth.synthesize_bidirectional_lens(schema_v1, schema_v2)
print(f"\nSynthesized Forward Lens: {lens['forward_getter_transform']}")
