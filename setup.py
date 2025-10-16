"""
Setup configuration for Codex Framework.

Production-grade packaging for distribution and installation.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read long description from README
readme_path = Path(__file__).parent / "README.md"
if readme_path.exists():
    long_description = readme_path.read_text(encoding="utf-8")
else:
    long_description = "Codex Autonomous Framework v4.0"

setup(
    name="codex-framework",
    version="4.0.0",
    description="Autonomous cognitive framework with continuous evolution",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Codex-Kael Prime",
    author_email="codex@autonomous.ai",
    url="https://github.com/codex-kael/autonomous-framework",
    packages=find_packages(include=["codex_framework", "codex_framework.*"]),
    python_requires=">=3.9",
    install_requires=[
        "pypdf>=3.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "mypy>=1.0.0",
            "ruff>=0.1.0",
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    entry_points={
        "console_scripts": [
            "codex=codex_framework.codex_autonomous:main",
        ],
    },
)
