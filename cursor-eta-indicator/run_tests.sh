#!/bin/bash
# Test runner script for cursor-eta

echo "Running cursor-eta tests..."
echo "=========================="

# Check if we're in a virtual environment
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "Warning: Not in a virtual environment. Tests may use system packages."
    echo ""
fi

# Run tests with different configurations
echo "1. Running unit tests with coverage..."
python3 -m pytest tests/ -v --cov=cursor_eta --cov-report=term-missing || exit 1

echo ""
echo "2. Running specific test modules..."
echo "   - Testing tracker..."
python3 -m unittest tests.test_tracker -v || exit 1

echo "   - Testing wrapper..."
python3 -m unittest tests.test_wrapper -v || exit 1

echo "   - Testing decorator..."
python3 -m unittest tests.test_decorator -v || exit 1

echo "   - Testing CLI..."
python3 -m unittest tests.test_cli -v || exit 1

echo ""
echo "3. Running doctests..."
python3 -m doctest cursor_eta/*.py -v || exit 1

echo ""
echo "4. Type checking (if mypy is available)..."
if python3 -c "import mypy" 2>/dev/null; then
    python3 -m mypy cursor_eta/ --ignore-missing-imports
else
    echo "   Skipping (mypy not installed)"
fi

echo ""
echo "5. Code style check (if flake8 is available)..."
if python3 -c "import flake8" 2>/dev/null; then
    python3 -m flake8 cursor_eta/ tests/ --max-line-length=100 --ignore=E501,W503
else
    echo "   Skipping (flake8 not installed)"
fi

echo ""
echo "=========================="
echo "All tests completed!"

# Generate coverage report if pytest-cov ran successfully
if [ -d "htmlcov" ]; then
    echo ""
    echo "Coverage report generated in htmlcov/index.html"
fi