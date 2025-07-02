# PyPI Publishing Setup Guide

This guide helps maintainers set up automatic PyPI publishing for cursor-eta.

## Prerequisites

1. PyPI account: https://pypi.org/account/register/
2. TestPyPI account: https://test.pypi.org/account/register/
3. Repository admin access to configure secrets

## Setup Options

### Option 1: Trusted Publishing (Recommended)

This uses OpenID Connect (OIDC) for secure, token-free publishing.

#### PyPI Configuration:

1. Go to https://pypi.org/manage/account/publishing/
2. Add a new trusted publisher:
   - PyPI Project Name: `cursor-eta`
   - Owner: `yourusername` (GitHub username/org)
   - Repository name: `cursor-eta-indicator`
   - Workflow name: `pypi.yml`
   - Environment name: `pypi`

3. Repeat for TestPyPI at https://test.pypi.org/manage/account/publishing/:
   - Use environment name: `test-pypi`

#### GitHub Configuration:

No secrets needed! The workflow uses OIDC authentication automatically.

### Option 2: API Token Authentication

Use this if you can't set up trusted publishing.

#### Generate API Tokens:

1. **TestPyPI Token:**
   - Go to https://test.pypi.org/manage/account/token/
   - Create token with scope: "Entire account" or project-specific
   - Copy the token (starts with `pypi-`)

2. **PyPI Token:**
   - Go to https://pypi.org/manage/account/token/
   - Create token with scope: "Entire account" or project-specific
   - Copy the token (starts with `pypi-`)

#### Add GitHub Secrets:

1. Go to repository Settings → Secrets and variables → Actions
2. Add repository secrets:
   - `TESTPYPI_API_TOKEN`: Your TestPyPI token
   - `PYPI_API_TOKEN`: Your PyPI token

## Publishing Process

### Automatic Publishing (Recommended)

1. Update version in:
   - `cursor_eta/__init__.py`
   - `setup.py`
   - `pyproject.toml`

2. Commit and push changes:
   ```bash
   git add -A
   git commit -m "Bump version to 0.1.0"
   git push
   ```

3. Create and push tag:
   ```bash
   git tag v0.1.0
   git push origin v0.1.0
   ```

4. The `pypi.yml` workflow automatically:
   - Builds the package
   - Publishes to TestPyPI
   - Tests installation
   - Publishes to PyPI
   - Verifies the release

### Manual Publishing

Use the manual workflow for testing or special cases:

1. Go to Actions → "Publish to PyPI (Manual/Token)"
2. Click "Run workflow"
3. Select options:
   - Target: `testpypi` or `pypi`
   - Skip test: Check to skip TestPyPI

## Local Testing

### Build locally:
```bash
python -m build
twine check dist/*
```

### Test with TestPyPI:
```bash
# Upload
twine upload --repository testpypi dist/*

# Install
pip install --index-url https://test.pypi.org/simple/ \
            --extra-index-url https://pypi.org/simple/ \
            cursor-eta
```

## Troubleshooting

### "Invalid or non-existent authentication"
- Check token is correctly set in GitHub secrets
- Ensure token has correct scope
- For trusted publishing, verify GitHub environment names match PyPI config

### "Version already exists"
- PyPI doesn't allow re-uploading the same version
- Bump version number and try again

### Package not found after upload
- Wait 1-2 minutes for PyPI to index
- Check package name matches exactly
- Verify upload succeeded in workflow logs

## Version Management

Use semantic versioning: MAJOR.MINOR.PATCH

- MAJOR: Breaking changes
- MINOR: New features (backwards compatible)
- PATCH: Bug fixes

Example version bumps:
- Bug fix: 0.1.0 → 0.1.1
- New feature: 0.1.1 → 0.2.0
- Breaking change: 0.2.0 → 1.0.0

## Security Notes

- Never commit tokens to the repository
- Use repository secrets for sensitive data
- Prefer trusted publishing over token auth
- Rotate tokens periodically
- Use project-scoped tokens when possible

## Quick Checklist

Before releasing:
- [ ] Tests pass locally
- [ ] Version bumped in all files
- [ ] CHANGELOG updated
- [ ] Documentation updated
- [ ] Example code tested

Release steps:
- [ ] Commit version bump
- [ ] Create git tag
- [ ] Push commits and tag
- [ ] Monitor GitHub Actions
- [ ] Verify PyPI listing
- [ ] Test installation