# Publishing Quick Start

## First Time Setup

1. **Create PyPI accounts:**
   - Production: https://pypi.org/account/register/
   - Test: https://test.pypi.org/account/register/

2. **Reserve package name on TestPyPI:**
   ```bash
   # Build locally
   cd cursor-eta-indicator
   python -m build
   
   # Upload to TestPyPI (will prompt for credentials)
   twine upload --repository testpypi dist/*
   ```

3. **Configure GitHub Secrets (for token auth):**
   - Go to Settings → Secrets → Actions
   - Add `TESTPYPI_API_TOKEN` and `PYPI_API_TOKEN`

## Publishing a New Version

### Step 1: Update Version
```bash
# From project root
python scripts/bump_version.py patch  # or minor/major
```

### Step 2: Test Locally
```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info

# Build
python -m build

# Check
twine check dist/*

# Test install
pip install dist/*.whl
cursor-eta check
```

### Step 3: Commit and Tag
```bash
git add -A
git commit -m "Bump version to 0.1.1"
git tag v0.1.1
git push && git push --tags
```

### Step 4: Monitor Release
1. Go to Actions tab on GitHub
2. Watch the "Publish to PyPI" workflow
3. Verify on https://pypi.org/project/cursor-eta/

## Manual Publishing (if automation fails)

### To TestPyPI:
```bash
twine upload --repository testpypi dist/*
```

### To PyPI:
```bash
twine upload dist/*
```

## Troubleshooting

**Build fails locally:**
```bash
pip install --upgrade build setuptools wheel
```

**Version exists error:**
- Bump to next version
- Never reuse version numbers

**GitHub Action fails:**
- Check secrets are set correctly
- Verify tag format matches `v*`
- Check workflow logs for details

## Quick Commands Reference

```bash
# Version management
python scripts/bump_version.py patch|minor|major|X.Y.Z

# Build
python -m build

# Check
twine check dist/*

# Upload test
twine upload -r testpypi dist/*

# Upload prod
twine upload dist/*

# Install from test
pip install -i https://test.pypi.org/simple/ cursor-eta

# Install from prod
pip install cursor-eta
```