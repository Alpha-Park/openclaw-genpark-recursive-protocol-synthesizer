# -*- coding: utf-8 -*-
import sys, json
from client import OpenClawGenParkRecursiveProtocolSynthesizer

client = OpenClawGenParkRecursiveProtocolSynthesizer()

TOOLS = [
    {
        "name": "unify_type_signatures",
        "description": "Executes first-order Robinson type unification to derive Most General Unifiers (MGU).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "sig_a": {"type": "object"},
                "sig_b": {"type": "object"}
            },
            "required": ["sig_a", "sig_b"]
        }
    },
    {
        "name": "compute_schema_structural_distance",
        "description": "Calculates normalized Graph Edit Distance between two MCP tool parameter schemas.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "schema_a": {"type": "object"},
                "schema_b": {"type": "object"}
            },
            "required": ["schema_a", "schema_b"]
        }
    },
    {
        "name": "synthesize_bidirectional_lens",
        "description": "Synthesizes getter/putback projection lenses between protocol schema versions.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "source_schema": {"type": "object"},
                "target_schema": {"type": "object"}
            },
            "required": ["source_schema", "target_schema"]
        }
    }
]

def handle_request(req):
    method = req.get("method")
    rid = req.get("id")
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": rid, "result": {"tools": TOOLS}}
    elif method == "tools/call":
        params = req.get("params", {})
        tname = params.get("name")
        args = params.get("arguments", {})
        if tname == "unify_type_signatures":
            res = client.unify_type_signatures(args["sig_a"], args["sig_b"])
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        elif tname == "compute_schema_structural_distance":
            res = client.compute_schema_structural_distance(args["schema_a"], args["schema_b"])
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        elif tname == "synthesize_bidirectional_lens":
            res = client.synthesize_bidirectional_lens(args["source_schema"], args["target_schema"])
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32601, "message": "Method not found"}}
    return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32600, "message": "Invalid Request"}}

def main():
    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
