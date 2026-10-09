"""Mock Payment Gateway — simulates Paystack-like APIs for test execution."""
import json
import uuid
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

DB = {"transactions": {}, "transfers": {}, "refunds": {}, "customers": {}, "merchants": {}}

class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(body).encode())

    def _read(self):
        length = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(length)) if length else {}

    def do_POST(self):
        body = self._read()
        path = self.path.rstrip("/")

        if path == "/v1/customers":
            cid = f"CUS_{uuid.uuid4().hex[:12]}"
            DB["customers"][cid] = {"id": cid, "email": body.get("email"), "created_at": int(time.time())}
            self._send(201, {"status": "success", "data": DB["customers"][cid]})

        elif path == "/v1/transactions/charge":
            tid = f"TXN_{uuid.uuid4().hex[:12]}"
            amount = body.get("amount", 0)
            status = "success" if amount > 0 else "failed"
            DB["transactions"][tid] = {
                "id": tid, "amount": amount, "currency": body.get("currency", "NGN"),
                "status": status, "reference": body.get("reference", str(uuid.uuid4())),
                "created_at": int(time.time())
            }
            self._send(200, {"status": "success", "data": DB["transactions"][tid]})

        elif path == "/v1/transfers":
            tid = f"TRF_{uuid.uuid4().hex[:12]}"
            DB["transfers"][tid] = {
                "id": tid, "amount": body.get("amount"), "recipient": body.get("recipient"),
                "status": "queued", "created_at": int(time.time())
            }
            self._send(202, {"status": "success", "data": DB["transfers"][tid]})

        elif path == "/v1/refunds":
            txn_id = body.get("transaction_id")
            if txn_id not in DB["transactions"]:
                self._send(404, {"status": "error", "message": "Transaction not found"})
                return
            rid = f"REF_{uuid.uuid4().hex[:12]}"
            DB["refunds"][rid] = {
                "id": rid, "transaction_id": txn_id,
                "amount": body.get("amount", DB["transactions"][txn_id]["amount"]),
                "status": "processed", "created_at": int(time.time())
            }
            self._send(201, {"status": "success", "data": DB["refunds"][rid]})

        else:
            self._send(404, {"status": "error", "message": "Not found"})

    def do_GET(self):
        path = self.path.rstrip("/")
        parts = path.split("/")

        if path == "/v1/health":
            self._send(200, {"status": "healthy", "uptime": time.time()})

        elif len(parts) == 4 and parts[1] == "v1":
            collection, resource_id = parts[2], parts[3]
            store = DB.get(collection, {})
            if resource_id in store:
                self._send(200, {"status": "success", "data": store[resource_id]})
            else:
                self._send(404, {"status": "error", "message": "Not found"})

        elif len(parts) == 3 and parts[1] == "v1":
            collection = parts[2]
            store = DB.get(collection, {})
            self._send(200, {"status": "success", "data": list(store.values())})

        else:
            self._send(404, {"status": "error", "message": "Not found"})

    def log_message(self, format, *args):
        pass  # silence request logs

def run(port=9876):
    server = HTTPServer(("127.0.0.1", port), Handler)
    print(f"Mock gateway running on :{port}")
    server.serve_forever()

if __name__ == "__main__":
    run()
