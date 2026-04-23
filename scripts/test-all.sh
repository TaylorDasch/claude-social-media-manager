#!/usr/bin/env bash
# Health check for all content system scripts.
# Run from project root: bash scripts/test-all.sh

cd "$(dirname "$0")/.."

PASS=0
FAIL=0

run_check() {
    local name="$1"
    shift
    if "$@" > /dev/null 2>&1; then
        echo "  PASS: $name"
        PASS=$((PASS + 1))
    else
        echo "  FAIL: $name"
        FAIL=$((FAIL + 1))
    fi
}

echo "========================================"
echo "SCRIPT HEALTH CHECK"
echo "========================================"

# Check Python 3 is available
run_check "Python 3 available" python3 --version

# Check each script can at least parse (syntax check)
run_check "freshness-scanner.py syntax" python3 -c "import py_compile; py_compile.compile('scripts/freshness-scanner.py', doraise=True)"
run_check "output-integrity-check.py syntax" python3 -c "import py_compile; py_compile.compile('scripts/output-integrity-check.py', doraise=True)"
run_check "dedupe-checker.py syntax" python3 -c "import py_compile; py_compile.compile('scripts/dedupe-checker.py', doraise=True)"
run_check "next-best-action.py syntax" python3 -c "import py_compile; py_compile.compile('scripts/next-best-action.py', doraise=True)"

# Check each script can run --help (no import errors)
run_check "freshness-scanner --help" python3 scripts/freshness-scanner.py --help
run_check "output-integrity-check --help" python3 scripts/output-integrity-check.py --help
run_check "dedupe-checker --help" python3 scripts/dedupe-checker.py --help
run_check "next-best-action --help" python3 scripts/next-best-action.py --help

# Check required data files exist
run_check "content-registry.csv exists" test -f data/content-registry.csv
run_check "performance-ledger.csv exists" test -f data/performance-ledger.csv
run_check "hook-bank.json exists" test -f data/hook-bank.json
run_check "QUALITY-GATES.md exists" test -f governance/QUALITY-GATES.md
run_check "VIDEO-TO-PAGE-MAP.md exists" test -f VIDEO-TO-PAGE-MAP.md

# Check sibling project path
if [ -d "../real-estate-redefined" ]; then
    echo "  PASS: real-estate-redefined/ sibling exists"
    PASS=$((PASS + 1))
else
    echo "  WARN: real-estate-redefined/ not found — freshness scanner will skip page scans"
fi

echo ""
echo "========================================"
echo "Results: $PASS passed, $FAIL failed"
echo "========================================"
exit $FAIL
