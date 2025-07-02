# Unified CI Pipeline Documentation

This document describes the comprehensive CI/CD pipeline for the Cursor ETA Indicator project.

## Overview

The CI pipeline is defined in `.github/workflows/ci.yml` and runs on:
- Every push to `main` and `develop` branches
- Every pull request targeting `main` or `develop`
- Manual workflow dispatch

## Pipeline Jobs

### 1. Pre-commit Checks
- **Purpose**: Enforce code quality standards before changes are merged
- **Tools**: pre-commit hooks defined in `.pre-commit-config.yaml`
- **Checks**:
  - Trailing whitespace removal
  - End-of-file fixing
  - YAML/JSON/TOML validation
  - Python formatting (Black)
  - Import sorting (isort)
  - Linting (flake8)
  - Type checking (mypy)
  - Security scanning (bandit)
  - Spell checking (codespell)
  - Version consistency

### 2. Python Tests
- **Purpose**: Ensure Python package functionality across multiple versions
- **Strategy**: Matrix testing on Python 3.8-3.12
- **Coverage**: Minimum 80% code coverage required
- **Platforms**: Ubuntu (all versions), Windows (3.8), macOS (3.12)
- **Test Runner**: pytest with coverage reporting
- **Reports**: XML coverage uploaded to Codecov

### 3. Python Linting
- **Purpose**: Enforce Python code style and quality
- **Tools**:
  - **Black**: Code formatting
  - **isort**: Import organization
  - **flake8**: Style guide enforcement
  - **mypy**: Static type checking

### 4. TypeScript Checks
- **Purpose**: Ensure VS Code extension code quality
- **Node Version**: 18.x
- **Checks**:
  - TypeScript compilation
  - Type error detection
  - ESLint (when configured)

### 5. Integration Tests
- **Purpose**: Verify the complete system works together
- **Dependencies**: Runs after Python and TypeScript checks
- **Tests**:
  - Python package installation
  - CLI command execution
  - Import verification
  - VS Code extension build

### 6. Build Artifacts
- **Purpose**: Create distribution packages
- **Outputs**:
  - Python wheel and source distribution
  - VS Code extension VSIX package
- **Artifacts**: Uploaded for download

### 7. Coverage Report
- **Purpose**: Generate detailed coverage analysis
- **Requirements**: 80% minimum coverage
- **Reports**:
  - Terminal output
  - HTML report (uploaded as artifact)
  - PR comment (on pull requests)

## Local Development

### Running Tests Locally

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run all tests with coverage
pytest --cov=cursor_eta --cov-report=html

# Run specific test file
pytest tests/test_agent_eta.py -v

# Run with tox for multiple Python versions
tox

# Run only linting
tox -e lint

# Run only type checking
tox -e typecheck
```

### Pre-commit Setup

```bash
# Install pre-commit hooks
pre-commit install

# Run all hooks manually
pre-commit run --all-files

# Run specific hook
pre-commit run black --all-files
```

### VS Code Extension Testing

```bash
cd vscode-extension

# Install dependencies
npm ci

# Compile TypeScript
npm run compile

# Run ESLint
npx eslint src --ext .ts

# Package extension
npx vsce package
```

## Configuration Files

### tox.ini
Defines environments for:
- Multi-version Python testing (py38-py312)
- Linting environment
- Type checking environment
- Coverage reporting
- Documentation building
- Package building

### .pre-commit-config.yaml
Configures automatic checks:
- Code formatting
- Import sorting
- Linting
- Type checking
- Security scanning
- Version consistency
- TypeScript compilation

### pyproject.toml
Defines:
- Build system configuration
- Project metadata
- Tool configurations (Black, isort, mypy, pytest, coverage)

## CI Secrets Required

For full functionality, configure these GitHub secrets:
- `CODECOV_TOKEN`: For coverage reporting (optional but recommended)

## Troubleshooting

### Common Issues

1. **Coverage Below 80%**
   - Run `pytest --cov=cursor_eta --cov-report=html`
   - Open `htmlcov/index.html` to see uncovered lines
   - Add tests for uncovered code

2. **Pre-commit Failures**
   - Most issues auto-fixable: `pre-commit run --all-files`
   - For persistent issues, check specific tool output

3. **Type Checking Errors**
   - Ensure all functions have type hints
   - Add `# type: ignore` sparingly for third-party issues
   - Use `types-*` packages for typed stubs

4. **VS Code Extension Build Failures**
   - Ensure Node.js 18.x is installed
   - Run `npm ci` to get exact dependency versions
   - Check TypeScript compilation: `npx tsc --noEmit`

## Adding New Tests

1. Create test file in `tests/` directory
2. Name it `test_*.py`
3. Use `unittest` or `pytest` style
4. Include docstrings for test methods
5. Mock external dependencies
6. Aim for fast execution (use `time.sleep` patches)

## Maintaining Code Quality

1. **Before Committing**:
   - Run `pre-commit run --all-files`
   - Run `tox -e coverage` to check coverage
   - Run `tox -e lint` for style issues

2. **Before Creating PR**:
   - Ensure all CI checks will pass
   - Update documentation if needed
   - Add tests for new features
   - Check version consistency

3. **Regular Maintenance**:
   - Update dependencies monthly
   - Review and update pre-commit hooks
   - Monitor CI execution time
   - Archive old artifacts