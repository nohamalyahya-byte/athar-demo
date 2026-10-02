"""ATHAR demo API — serves the interactive demo and exposes the SQLite database as JSON.
Standard library only. Run:  python3 api/server.py   then open http://localhost:8080
All data is synthetic / illustrative. No real patient data, no real system integration.
"""
import json, os, sqlite3
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(ROOT, "database", "athar_demo.sqlite")
WEB = os.path.join(ROOT, "code")

def query(sql, args=()):
    con = sqlite3.connect(DB); con.row_factory = sqlite3.Row
    try: return [dict(r) for r in con.execute(sql, args).fetchall()]
    finally: con.close()

def level(score, th):
    return "high" if score >= th["cumulative_high"] else "med" if score >= th["cumulative_medium"] else "low"

ROUTES = {
    "/api/cases":        lambda: query("SELECT c.*, s.score FROM cases c JOIN v_case_scores s ON s.case_id=c.id ORDER BY c.id"),
    "/api/signal-types": lambda: query("SELECT * FROM signal_types"),
    "/api/thresholds":   lambda: query("SELECT * FROM thresholds"),
    "/api/departments":  lambda: query("SELECT * FROM departments"),
    "/api/places":       lambda: query("SELECT * FROM places"),
}

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=WEB, **k)
    def do_GET(self):
        path = urlparse(self.path).path
        if path in ROUTES: return self.send_json(ROUTES[path]())
        if path.startswith("/api/cases/"):
            cid = path.split("/")[3]
            case = query("SELECT c.*, s.score FROM cases c JOIN v_case_scores s ON s.case_id=c.id WHERE c.id=?", (cid,))
            if not case: return self.send_json({"error": "case not found"}, 404)
            th = {r["key"]: r["value"] for r in query("SELECT key,value FROM thresholds")}
            c = case[0]; c["level"] = level(c["score"], th)
            c["signals"]  = query("SELECT s.*, t.name_ar, t.name_en, t.source_ar, t.source_en FROM case_signals s JOIN signal_types t ON t.key=s.signal_key WHERE case_id=?", (cid,))
            c["events"]   = query("SELECT * FROM journey_events WHERE case_id=? ORDER BY id", (cid,))
            c["update"]   = (query("SELECT * FROM case_updates WHERE case_id=?", (cid,)) or [None])[0]
            c["log"]      = query("SELECT * FROM follow_up_log WHERE case_id=? ORDER BY id", (cid,))
            c["location"] = query("SELECT seq, place_code FROM location_pings WHERE case_id=? ORDER BY seq", (cid,))
            return self.send_json(c)
        if path == "/": self.path = "/index.html"
        return super().do_GET()
    def send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status); self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)

if __name__ == "__main__":
    print("ATHAR demo API on http://localhost:8080  (Ctrl+C to stop)")
    ThreadingHTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
