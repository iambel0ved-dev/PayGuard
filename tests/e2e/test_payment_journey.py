"""E2E tests: simulate full merchant payment journeys."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from framework.assertions import assert_status, assert_response_time

class TestMerchantPaymentJourney:
    """Simulates: customer created → charged → refunded → verified."""

    def test_complete_payment_lifecycle(self, api):
        # Step 1: Register customer
        cust = api.post("/v1/customers", json={"email": "buyer@shop.ng"})
        assert_status(cust, 201)

        # Step 2: Process payment
        charge = api.post("/v1/transactions/charge", json={
            "amount": 25000, "currency": "NGN", "reference": "ORDER_789"
        })
        assert_status(charge, 200)
        assert_response_time(charge, 500)  # SLA: <500ms
        txn = charge.json()["data"]
        assert txn["status"] == "success"

        # Step 3: Merchant issues refund
        refund = api.post("/v1/refunds", json={"transaction_id": txn["id"], "amount": 25000})
        assert_status(refund, 201)
        assert refund.json()["data"]["status"] == "processed"

        # Step 4: Audit trail
        all_refunds = api.get("/v1/refunds")
        assert_status(all_refunds, 200)
        assert any(r["transaction_id"] == txn["id"] for r in all_refunds.json()["data"])

class TestHealthGate:
    def test_platform_healthy(self, api):
        resp = api.get("/v1/health")
        assert_status(resp, 200)
        assert_response_time(resp, 100)
        assert resp.json()["status"] == "healthy"
