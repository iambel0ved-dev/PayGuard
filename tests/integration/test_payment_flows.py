"""Integration tests: verify multi-step payment flows across services."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from framework.assertions import assert_status, assert_response_time

class TestChargeThenRefund:
    def test_full_refund_flow(self, api):
        # 1. Charge
        charge = api.post("/v1/transactions/charge", json={"amount": 7500, "currency": "NGN"})
        assert_status(charge, 200)
        txn = charge.json()["data"]

        # 2. Verify transaction exists
        lookup = api.get(f"/v1/transactions/{txn['id']}")
        assert_status(lookup, 200)
        assert lookup.json()["data"]["amount"] == 7500

        # 3. Refund
        refund = api.post("/v1/refunds", json={"transaction_id": txn["id"]})
        assert_status(refund, 201)
        assert refund.json()["data"]["amount"] == 7500

        # 4. Verify refund recorded
        refund_lookup = api.get(f"/v1/refunds/{refund.json()['data']['id']}")
        assert_status(refund_lookup, 200)

class TestCustomerLifecycle:
    def test_create_and_retrieve_customer(self, api):
        create = api.post("/v1/customers", json={"email": "merchant@example.com"})
        assert_status(create, 201)
        cid = create.json()["data"]["id"]

        get = api.get(f"/v1/customers/{cid}")
        assert_status(get, 200)
        assert get.json()["data"]["email"] == "merchant@example.com"

class TestTransferQueue:
    def test_transfer_enters_queue(self, api):
        resp = api.post("/v1/transfers", json={"amount": 50000, "recipient": "REC_BANK_01"})
        assert_status(resp, 202)
        tid = resp.json()["data"]["id"]

        lookup = api.get(f"/v1/transfers/{tid}")
        assert_status(lookup, 200)
        assert lookup.json()["data"]["status"] == "queued"
