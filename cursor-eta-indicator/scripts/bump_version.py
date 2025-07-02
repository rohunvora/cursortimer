#!/usr/bin/env python3
"""
Version bump utility for cursor-eta package.

Usage:
    python scripts/bump_version.py patch  # 0.1.0 -> 0.1.1
    python scripts/bump_version.py minor  # 0.1.1 -> 0.2.0
    python scripts/bump_version.py major  # 0.2.0 -> 1.0.0
    python scripts/bump_version.py 0.3.5  # Set specific version
"""

import re
import sys
from pathlib import Path


def get_current_version():
    """Get current version from __init__.py"""
    init_file = Path("cursor_eta/__init__.py")
    content = init_file.read_text()
    match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
    if match:
        return match.group(1)
    raise ValueError("Could not find version in __init__.py")


def bump_version(current, bump_type):
    """Bump version based on type"""
    major, minor, patch = map(int, current.split('.'))
    
    if bump_type == 'major':
        return f"{major + 1}.0.0"
    elif bump_type == 'minor':
        return f"{major}.{minor + 1}.0"
    elif bump_type == 'patch':
        return f"{major}.{minor}.{patch + 1}"
    else:
        # Assume it's a specific version
        if not re.match(r'^\d+\.\d+\.\d+$', bump_type):
            raise ValueError(f"Invalid version format: {bump_type}")
        return bump_type


def update_file(filepath, old_version, new_version):
    """Update version in a file"""
    path = Path(filepath)
    if not path.exists():
        print(f"  ⚠️  {filepath} not found, skipping")
        return False
    
    content = path.read_text()
    
    # Different patterns for different files
    patterns = [
        # Python files: __version__ = "x.x.x"
        (r'(__version__\s*=\s*["\'])' + re.escape(old_version) + r'(["\'])',
         r'\g<1>' + new_version + r'\g<2>'),
        # setup.py/pyproject.toml: version = "x.x.x" or version="x.x.x"
        (r'(version\s*=\s*["\'])' + re.escape(old_version) + r'(["\'])',
         r'\g<1>' + new_version + r'\g<2>'),
    ]
    
    updated = False
    for pattern, replacement in patterns:
        new_content, count = re.subn(pattern, replacement, content)
        if count > 0:
            path.write_text(new_content)
            updated = True
            print(f"  ✓ Updated {filepath} ({count} occurrences)")
            break
    
    if not updated:
        print(f"  ⚠️  No version found in {filepath}")
    
    return updated


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    
    bump_type = sys.argv[1]
    
    # Get current version
    try:
        current_version = get_current_version()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    print(f"Current version: {current_version}")
    
    # Calculate new version
    try:
        new_version = bump_version(current_version, bump_type)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    print(f"New version: {new_version}")
    
    # Files to update
    files_to_update = [
        "cursor_eta/__init__.py",
        "setup.py",
        "pyproject.toml",
    ]
    
    print("\nUpdating files:")
    success_count = 0
    for filepath in files_to_update:
        if update_file(filepath, current_version, new_version):
            success_count += 1
    
    print(f"\n✅ Updated {success_count}/{len(files_to_update)} files")
    
    if success_count == len(files_to_update):
        print(f"\nNext steps:")
        print(f"1. Review changes: git diff")
        print(f"2. Commit: git commit -am 'Bump version to {new_version}'")
        print(f"3. Tag: git tag v{new_version}")
        print(f"4. Push: git push && git push --tags")
    else:
        print("\n⚠️  Some files were not updated. Please check manually.")
        sys.exit(1)


if __name__ == "__main__":
    main()