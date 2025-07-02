#!/usr/bin/env python3
"""Check version consistency across project files."""

import json
import re
import sys
from pathlib import Path


def get_version_from_init():
    """Extract version from __init__.py."""
    init_file = Path("cursor_eta/__init__.py")
    if not init_file.exists():
        return None
    
    content = init_file.read_text()
    match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
    return match.group(1) if match else None


def get_version_from_setup():
    """Extract version from setup.py."""
    setup_file = Path("setup.py")
    if not setup_file.exists():
        return None
    
    content = setup_file.read_text()
    match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
    return match.group(1) if match else None


def get_version_from_pyproject():
    """Extract version from pyproject.toml."""
    pyproject_file = Path("pyproject.toml")
    if not pyproject_file.exists():
        return None
    
    content = pyproject_file.read_text()
    match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
    return match.group(1) if match else None


def get_version_from_package_json():
    """Extract version from package.json."""
    package_file = Path("vscode-extension/package.json")
    if not package_file.exists():
        return None
    
    try:
        data = json.loads(package_file.read_text())
        return data.get("version")
    except (json.JSONDecodeError, KeyError):
        return None


def main():
    """Check version consistency across all files."""
    versions = {
        "__init__.py": get_version_from_init(),
        "setup.py": get_version_from_setup(),
        "pyproject.toml": get_version_from_pyproject(),
        "package.json": get_version_from_package_json(),
    }
    
    # Filter out None values
    versions = {k: v for k, v in versions.items() if v is not None}
    
    if not versions:
        print("❌ No version information found in any file!")
        return 1
    
    # Check if all versions are the same
    unique_versions = set(versions.values())
    
    if len(unique_versions) == 1:
        version = unique_versions.pop()
        print(f"✅ All versions are consistent: {version}")
        return 0
    else:
        print("❌ Version mismatch detected!")
        for file, version in versions.items():
            print(f"  {file}: {version}")
        return 1


if __name__ == "__main__":
    sys.exit(main())