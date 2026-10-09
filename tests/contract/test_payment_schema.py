"""Contract tests: validate API response schemas match payment platform contracts."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from framework.assertions import assert_status, assert_schema, assert_json_field

class TestChargeContract:
    def test_charge_response_schema(self, api):
        resp = api.post("/v1/transactions/charge", json={"amount": 5000, "currency": "NGN", "reference": "ref_001"})
        assert_status(resp, 200)
        assert_json_field(resp, "status", "success")
        data = resp.json()["data"]
        assert isinstance(data["id"], str)
        assert isinstance(data["amount"], int)
        assert data["currency"] == "NGN"
        assert data["status"] in ("success", "failed")

    def test_charge_requires_positive_amount(self, api):
        resp = api.post("/v1/transactions/charge", json={"amount": -100})
        assert_status(resp, 200)
        assert resp.json()["data"]["status"] == "failed"

class TestTransferContract:
    def test_transfer_response_schema(self, api):
        resp = api.post("/v1/transfers", json={"amount": 10000, "recipient": "REC_001"})
        assert_status(resp, 202)
        assert_json_field(resp, "status", "success")
        data = resp.json()["data"]
        assert data["status"] == "queued"
        assert "id" in data and "created_at" in data

class TestRefundContract:
    def test_refund_requires_valid_transaction(self, api):
        resp = api.post("/v1/refunds", json={"transaction_id": "TXN_nonexistent"})
        assert_status(resp, 404)
        assert_json_field(resp, "status", "error")

    def test_refund_response_schema(self, api):
        # Create a transaction first
        txn = api.post("/v1/transactions/charge", json={"amount": 3000}).json()["data"]
        resp = api.post("/v1/refunds", json={"transaction_id": txn["id"]})
        assert_status(resp, 201)
        data = resp.json()["data"]
        assert data["status"] == "processed"
        assert data["amount"] == 3000
