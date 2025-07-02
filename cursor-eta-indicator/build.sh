#!/bin/bash
# Build script for cursor-eta package

echo "Building cursor-eta package..."

# Clean previous builds
rm -rf build/ dist/ *.egg-info/

# Create source distribution
echo "Creating source distribution..."
python3 setup.py sdist

# Create wheel distribution (if wheel is available)
if python3 -c "import wheel" 2>/dev/null; then
    echo "Creating wheel distribution..."
    python3 setup.py bdist_wheel
else
    echo "Wheel not available, skipping wheel distribution"
fi

echo ""
echo "Build complete! Distribution files:"
ls -la dist/

echo ""
echo "To upload to PyPI:"
echo "  python3 -m twine upload dist/*"
echo ""
echo "To install locally:"
echo "  pip install dist/cursor-eta-*.tar.gz"