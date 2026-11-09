"""Tiny client for the UEFN MCP server (http://127.0.0.1:8001/mcp).

usage: python uefn_mcp.py list                      -> tool names and descriptions
       python uefn_mcp.py schema <tool>             -> input schema of a tool
       python uefn_mcp.py call <tool> '<json args>' -> result text
"""
import json, sys, urllib.request

URL = "http://127.0.0.1:8001/mcp"


def post(body, session=None):
    req = urllib.request.Request(URL, data=json.dumps(body).encode(), method="POST",
                                 headers={"Content-Type": "application/json", "Accept": "application/json, text/event-stream",
                                          **({"Mcp-Session-Id": session} if session else {})})
    with urllib.request.urlopen(req, timeout=600) as r:
        sid = r.headers.get("Mcp-Session-Id")
        text = r.read().decode("utf-8", "replace")
    if text.startswith("event:") or "\ndata:" in text or text.startswith("data:"):
        datas = [l[5:].strip() for l in text.splitlines() if l.startswith("data:")]
        text = datas[-1] if datas else ""
    return sid, (json.loads(text) if text.strip() else None)


def session():
    sid, _ = post({"jsonrpc": "2.0", "id": 1, "method": "initialize",
                   "params": {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "claude", "version": "1"}}})
    post({"jsonrpc": "2.0", "method": "notifications/initialized"}, sid)
    return sid


def main():
    sid = session()
    cmd = sys.argv[1]
    if cmd == "list":
        _, r = post({"jsonrpc": "2.0", "id": 2, "method": "tools/list"}, sid)
        for t in r["result"]["tools"]:
            print(t["name"], "-", (t.get("description") or "")[:200].replace("\n", " "))
    elif cmd == "schema":
        _, r = post({"jsonrpc": "2.0", "id": 2, "method": "tools/list"}, sid)
        for t in r["result"]["tools"]:
            if t["name"] == sys.argv[2]:
                print(json.dumps(t, indent=1))
    elif cmd == "call":
        args = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}
        _, r = post({"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": sys.argv[2], "arguments": args}}, sid)
        if r is None:
            print("(no response)")
            return
        if "error" in r:
            print("ERROR", json.dumps(r["error"]))
            return
        for c in r["result"].get("content", []):
            print(c.get("text", c))


if __name__ == "__main__":
    main()
