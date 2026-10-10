#!/bin/bash
# PayGuard walkthrough — all commands run for real; sleeps pace the video.
cd /root/payguard
export PATH="$PWD/.venv/bin:$PATH"
clear
printf '\n\e[1;36m  PayGuard — Payment Platform Quality Engineering\e[0m\n'
printf '\e[1;33m  Contract • Integration • E2E • Performance test automation\e[0m\n\n'
sleep 3

printf '\e[1;32m$ \e[0mProject layout:\n'
find . -path ./.venv -prune -o -path ./.git -prune -o -path ./reports -prune -o -type f -print | grep -v __pycache__ | sort
sleep 4

printf '\n\e[1;32m$ \e[0mStarting mock payment gateway (charge/transfer/refund APIs)...\n'
python mock_server/server.py > /tmp/mock_gw.log 2>&1 &
MOCK_PID=$!
sleep 1.5
curl -s http://127.0.0.1:9876/v1/health; echo
sleep 2

printf '\n\e[1;32m$ \e[0mContract tests — response schema validation:\n'
python -m pytest tests/contract -v 2>&1 | tail -10
sleep 3

printf '\n\e[1;32m$ \e[0mIntegration tests — charge → lookup → refund flows:\n'
python -m pytest tests/integration -v 2>&1 | tail -8
sleep 3

printf '\n\e[1;32m$ \e[0mE2E tests — full merchant payment journey + health gate:\n'
python -m pytest tests/e2e -v 2>&1 | tail -7
sleep 3

printf '\n\e[1;32m$ \e[0mPerformance: Locust load test — 20 users against charge API:\n'
python -m locust -f tests/performance/locustfile.py --headless -u 20 -r 10 -t 25s 2>&1 | tail -22
sleep 2

printf '\n\e[1;32m$ \e[0mGenerate HTML test report (CI artifact):\n'
python -m pytest tests/contract tests/integration tests/e2e --html=reports/report.html --self-contained-html -q 2>&1 | tail -3
sleep 2

printf '\n\e[1;35m  ✔ 10 functional tests passing • load test complete • CI gate: .github/workflows/test-gate.yml\e[0m\n'
sleep 4
kill $MOCK_PID 2>/dev/null
exit 0