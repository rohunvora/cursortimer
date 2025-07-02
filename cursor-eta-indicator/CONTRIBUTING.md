# Contributing to Cursor ETA Indicator

Thank you for your interest in contributing to Cursor ETA Indicator! This guide will help you get started with contributing to the project.

## 🚀 Quick Start

1. **Fork the repository**
2. **Clone your fork**:
   ```bash
   git clone https://github.com/yourusername/cursor-eta-indicator.git
   cd cursor-eta-indicator
   ```
3. **Install development dependencies**:
   ```bash
   pip install -e ".[dev]"
   ```
4. **Install pre-commit hooks**:
   ```bash
   pre-commit install
   ```
5. **Create a feature branch**:
   ```bash
   git checkout -b feature/amazing-feature
   ```

## 📁 Project Structure

```
cursor-eta-indicator/
├── cursor_eta/              # Main Python package
│   ├── __init__.py         # Package exports
│   ├── agent_with_eta.py   # Core ETA tracking
│   └── eta_bridge.py       # VS Code communication
├── vscode-extension/        # VS Code extension
│   ├── src/                # TypeScript source
│   ├── package.json        # Extension manifest
│   └── tsconfig.json       # TypeScript config
├── tests/                  # Python tests
├── examples/               # Usage examples
├── docs/                   # Documentation
├── .github/                # CI/CD workflows
└── scripts/                # Utility scripts
```

## 🧪 Development Setup

### Python Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
black cursor_eta tests
isort cursor_eta tests
flake8 cursor_eta tests
mypy cursor_eta
```

### VS Code Extension

```bash
cd vscode-extension

# Install dependencies
npm ci

# Compile TypeScript
npm run compile

# Watch for changes
npm run watch

# Package extension
npm run package
```

### Pre-commit Hooks

We use pre-commit hooks to ensure code quality:

```bash
# Install hooks
pre-commit install

# Run all hooks manually
pre-commit run --all-files

# Run specific hook
pre-commit run black --all-files
```

## 🧪 Testing

### Python Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=cursor_eta --cov-report=html

# Run specific test file
pytest tests/test_agent_eta.py -v

# Run with multiple Python versions
tox
```

### VS Code Extension Tests

```bash
cd vscode-extension

# Compile and run tests
npm test

# Manual testing
npm run compile
code --install-extension .
```

### Integration Tests

```bash
# Test the full pipeline
python examples/basic_usage.py

# Test VS Code integration
python examples/vscode_integration.py
```

## 📝 Code Style

### Python

- **Formatter**: Black with 100 character line limit
- **Import sorting**: isort with Black profile
- **Linting**: flake8 with specific ignore rules
- **Type checking**: mypy with strict settings

```bash
# Format code
black cursor_eta tests

# Sort imports
isort cursor_eta tests

# Check linting
flake8 cursor_eta tests

# Type checking
mypy cursor_eta
```

### TypeScript

- **Formatter**: Prettier
- **Linting**: ESLint with TypeScript rules
- **Style**: 4-space indentation, single quotes

```bash
cd vscode-extension

# Format code
npx prettier --write src/

# Run linting
npm run lint

# Auto-fix linting issues
npm run lint:fix
```

## 🐛 Reporting Issues

### Bug Reports

Use the bug report template and include:

- **Environment**: OS, Python version, VS Code version
- **Steps to reproduce**: Clear, numbered steps
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happens
- **Error messages**: Full stack traces if available
- **Code samples**: Minimal reproducible example

### Feature Requests

Use the feature request template and include:

- **Problem description**: What problem does this solve?
- **Proposed solution**: How should it work?
- **Alternatives considered**: Other approaches you've thought of
- **Use cases**: Real-world scenarios where this would help

## 🔧 Making Changes

### Development Workflow

1. **Create an issue** first (for non-trivial changes)
2. **Fork and clone** the repository
3. **Create a feature branch**: `git checkout -b feature/description`
4. **Make your changes** following the style guide
5. **Add tests** for new functionality
6. **Update documentation** if needed
7. **Run the test suite** to ensure everything works
8. **Commit your changes** with descriptive messages
9. **Push to your fork** and create a pull request

### Commit Messages

Follow conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat(eta): add token usage tracking
fix(bridge): handle JSON serialization errors
docs(readme): update installation instructions
test(agent): add tests for error handling
```

### Pull Request Guidelines

1. **Fill out the PR template** completely
2. **Link to related issues** using keywords like "Fixes #123"
3. **Keep changes focused** - one feature/fix per PR
4. **Update documentation** for user-facing changes
5. **Add tests** for new functionality
6. **Ensure CI passes** before requesting review
7. **Respond to feedback** promptly and professionally

### Code Review Process

- **All PRs require review** before merging
- **Maintainers will review** within a few days
- **Address feedback** by pushing new commits
- **Squash commits** may be requested before merge
- **CI must pass** for all supported Python versions

## 📚 Documentation

### Adding Documentation

- **API changes**: Update `docs/API_REFERENCE.md`
- **New features**: Add examples to `examples/`
- **VS Code extension**: Update `docs/VSCODE_EXTENSION.md`
- **Configuration**: Update README.md

### Documentation Style

- **Clear and concise**: Use simple language
- **Code examples**: Include working examples
- **Cross-references**: Link to related sections
- **Up-to-date**: Keep examples current with API

## 🎯 Areas for Contribution

### High Priority

- **Performance optimizations**: Reduce overhead
- **Better error handling**: More informative error messages
- **Cross-platform testing**: Windows/macOS specific issues
- **Documentation improvements**: Clearer examples and guides

### Medium Priority

- **New ETA algorithms**: More accurate time estimation
- **Additional VS Code features**: Progress notifications, etc.
- **Integration examples**: With popular frameworks
- **Performance benchmarks**: Automated performance testing

### Good First Issues

Look for issues labeled `good first issue`:
- **Documentation fixes**: Typos, unclear instructions
- **Test improvements**: Edge cases, error conditions
- **Small feature additions**: Configuration options
- **Example scripts**: Real-world usage scenarios

## 🚀 Release Process

### Version Numbers

We follow [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Steps

1. **Update version** in relevant files
2. **Update CHANGELOG.md** with release notes
3. **Run full test suite** on all platforms
4. **Create release PR** for review
5. **Tag release** after merge
6. **CI automatically publishes** to PyPI and Open VSX

### Version Update Script

```bash
# Bump version automatically
python scripts/bump_version.py patch  # or minor, major
```

## 🤝 Community Guidelines

### Code of Conduct

- **Be respectful** and inclusive
- **Welcome newcomers** and help them learn
- **Focus on constructive feedback**
- **Assume good intentions**

### Communication

- **GitHub Issues**: Bug reports, feature requests
- **GitHub Discussions**: Questions, ideas, general chat
- **Pull Request Reviews**: Code-focused feedback

### Recognition

Contributors are recognized in:
- **CHANGELOG.md**: Major contributions
- **README.md**: Significant contributors
- **Release notes**: Notable features/fixes

## ❓ Getting Help

### Documentation

- **README.md**: Project overview and quick start
- **docs/**: Detailed documentation
- **examples/**: Working code examples

### Support Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Questions and community chat
- **Code Comments**: Implementation details

### Common Issues

- **Import errors**: Check Python path and installation
- **VS Code extension not working**: Check output panel for errors
- **Tests failing**: Ensure all dependencies are installed
- **Type checking errors**: Install type stubs with `pip install types-*`

## 📋 Checklist for Contributors

Before submitting a PR:

- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] Documentation updated if needed
- [ ] Pre-commit hooks pass
- [ ] Commit messages follow convention
- [ ] PR template filled out completely
- [ ] Related issues linked

Thank you for contributing to Cursor ETA Indicator! 🎉