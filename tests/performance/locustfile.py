"""Performance test: load test payment charge endpoint with Locust."""
from locust import HttpUser, task, between

class PaymentUser(HttpUser):
    wait_time = between(0.5, 2)
    host = "http://127.0.0.1:9876"

    @task(5)
    def charge_payment(self):
        self.client.post("/v1/transactions/charge", json={
            "amount": 5000,
            "currency": "NGN",
            "reference": f"load_test_{self.environment.runner.user_count}"
        })

    @task(2)
    def check_health(self):
        self.client.get("/v1/health")

    @task(1)
    def list_transactions(self):
        self.client.get("/v1/transactions")
