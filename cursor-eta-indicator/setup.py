#!/usr/bin/env python3
"""Setup script for cursor-eta package."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

setup(
    name="cursor-eta",
    version="0.1.0",
    author="Your Name",  # TODO: Update with actual author
    author_email="your.email@example.com",  # TODO: Update with actual email
    description="ETA indicators for cursor AI coding tasks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/cursor-eta-indicator",  # TODO: Update with actual URL
    packages=find_packages(exclude=["tests*", "examples*", "demo*", "vscode-extension*"]),
    python_requires=">=3.8",
    install_requires=[
        "psutil>=5.9.0",
        "typing-extensions>=4.0.0;python_version<'3.9'",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "mypy>=1.0.0",
            "flake8>=6.0.0",
            "pre-commit>=3.0.0",
        ],
        "demo": [
            "rich>=13.0.0",
            "click>=8.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "cursor-eta=cursor_eta.__main__:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: User Interfaces",
    ],
    keywords="cursor, eta, progress, ai, coding, assistant",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/cursor-eta-indicator/issues",
        "Source": "https://github.com/yourusername/cursor-eta-indicator",
        "Documentation": "https://cursor-eta.github.io",
    },
)