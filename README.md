# PayGuard — Payment Platform Quality Engineering

A comprehensive test automation framework for payment platforms, covering API, Dashboard, mobile, and POS channels.

## Structure
- `framework/` — Core test infrastructure (HTTP client, assertions, fixtures)
- `tests/contract/` — Schema & contract validation
- `tests/integration/` — Service-to-service integration tests
- `tests/e2e/` — End-to-end user flows
- `tests/performance/` — Load & performance tests
- `mock_server/` — Mock payment gateway for isolated testing
- `reports/` — Generated test reports

## Walkthrough Video

<p align="center">
  <video src="https://github.com/iambel0ved-dev/PayGuard/raw/main/payguard_walkthrough.mp4" controls width="720"></video>
</p>

▶ [Watch: payguard_walkthrough.mp4](payguard_walkthrough.mp4)

A real-execution walkthrough of the full suite: project layout → mock payment gateway health check → contract, integration & E2E test suites (10 tests) → 20-user Locust load test against the charge API → HTML test-report generation. Every command in the video actually runs.

## Quick Start
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest tests/ -v --html=reports/report.html
```
