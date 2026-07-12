# -*- coding: utf-8 -*-
import os
import json
from http.server import SimpleHTTPRequestHandler, HTTPServer
from socketserver import TCPServer

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(DIRECTORY, 'db_store.json')

def load_db():
    """Loads state from persistent JSON file database."""
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            pass
            
    # Initial default dashboard records state
    default_state = {
        "esg_score": 89.5,
        "e_score": 92.0,
        "s_score": 80.0,
        "g_score": 83.0,
        "health": "Excellent",
        "trend": "Improving",
        "carbon_transactions": [
            {"date": "2026-07-05", "name": "Ops Warehouse Grid Logging Q2", "type": "Scope 2 (Indirect)", "qty": "12,000 kWh", "co2": 9.84, "status": "Approved"},
            {"date": "2026-07-10", "name": "Generator Diesel Fill-up", "type": "Scope 1 (Direct)", "qty": "1,500 Liters", "co2": 4.02, "status": "Draft"}
        ],
        "csr_activities": [
            {"volunteer": "Siddharth", "event": "Annual Tree Planting Initiative 2026", "hours": "8.0 Hours", "points": "80 Points", "date": "2026-07-05"}
        ],
        "rewards": [
            {"name": "Eco Bamboo Water Bottle", "cost": "60 Points", "stock": 15},
            {"name": "Recycled Cork Notebook", "cost": "30 Points", "stock": 25},
            {"name": "Solar Window Charger", "cost": "180 Points", "stock": 5}
        ]
    }
    save_db(default_state)
    return default_state

def save_db(data):
    """Saves state to persistent JSON file database."""
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)

class DynamicESGRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, X-User-Role')
        self.end_headers()

    def do_GET(self):
        if self.path == '/api/data':
            try:
                data = load_db()
                response_content = json.dumps(data).encode('utf-8')
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(response_content)))
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(response_content)
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode('utf-8'))
        else:
            super().do_GET()

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        try:
            params = json.loads(post_data)
        except Exception:
            params = {}

        # Extract active user role from X-User-Role header
        user_role = self.headers.get('X-User-Role', 'Employee')
        
        # Enforce Backend RBAC Authorization checks
        if self.path in ['/api/carbon/add', '/api/carbon/approve']:
            if user_role != 'Sustainability Manager':
                self.send_response(403)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Permission Denied: Only Sustainability Managers can add or approve carbon entries."}).encode('utf-8'))
                return
        
        elif self.path == '/api/audit/schedule':
            if user_role != 'Compliance Officer':
                self.send_response(403)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Permission Denied: Only Compliance Officers can schedule audits."}).encode('utf-8'))
                return

        # Persist transactions to local JSON database in real-time
        db = load_db()
        if self.path == '/api/carbon/add':
            db["carbon_transactions"].insert(0, {
                "date": params.get("date", "2026-07-12"),
                "name": params.get("name", "Logged Carbon"),
                "type": params.get("type", "Scope 2 (Indirect)"),
                "qty": params.get("qty", "0 units"),
                "co2": float(params.get("co2", 0.0)),
                "status": "Approved"
            })
            # Recalculate dynamic ESG score based on cumulative carbon footprints
            total_co2 = sum(tx["co2"] for tx in db["carbon_transactions"])
            db["esg_score"] = max(89.5 - (total_co2 * 0.05), 40.0)
            save_db(db)

        elif self.path == '/api/csr/log':
            db["csr_activities"].insert(0, {
                "volunteer": params.get("volunteer", "Employee"),
                "event": params.get("event", "Event"),
                "hours": params.get("hours", "0 Hours"),
                "points": params.get("points", "0 Points"),
                "date": params.get("date", "2026-07-12")
            })
            save_db(db)

        # Request verified and persisted successfully
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({"success": True, "message": "ERP operation posted successfully"}).encode('utf-8'))

if __name__ == '__main__':
    TCPServer.allow_reuse_address = True
    with HTTPServer(('0.0.0.0', PORT), DynamicESGRequestHandler) as httpd:
        print(f"Serving EcoSphere dynamic preview on http://localhost:{PORT}")
        httpd.serve_forever()
