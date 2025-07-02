"""Setup configuration for cursor-eta package."""

from setuptools import setup, find_packages
import os

# Read the README for long description
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='cursor-eta',
    version='0.1.0',
    author='Cursor ETA Contributors',
    author_email='',
    description='Lightweight ETA/progress indicator for Cursor AI agent calls with zero token overhead',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/cursor-eta/cursor-eta',
    project_urls={
        'Bug Reports': 'https://github.com/cursor-eta/cursor-eta/issues',
        'Source': 'https://github.com/cursor-eta/cursor-eta',
        'Documentation': 'https://cursor-eta.github.io',
    },
    packages=find_packages(exclude=['tests*', 'examples*', 'docs*']),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: User Interfaces',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
        'Environment :: Console',
        'Framework :: AsyncIO',
    ],
    keywords='cursor ai eta progress tracking llm agent development-tools',
    python_requires='>=3.8',
    install_requires=[
        # No dependencies! Keeping it lightweight
    ],
    extras_require={
        'dev': [
            'pytest>=7.0',
            'pytest-cov>=4.0',
            'pytest-asyncio>=0.20',
            'black>=23.0',
            'flake8>=6.0',
            'mypy>=1.0',
            'pre-commit>=3.0',
        ],
        'docs': [
            'mkdocs>=1.5',
            'mkdocs-material>=9.0',
            'mkdocstrings[python]>=0.20',
        ],
    },
    entry_points={
        'console_scripts': [
            'cursor-eta=cursor_eta.__main__:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)