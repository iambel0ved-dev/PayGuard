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

## Quick Start
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest tests/ -v --html=reports/report.html
```
