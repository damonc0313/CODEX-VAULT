#!/usr/bin/env python3
"""
Setup script for KaelOS Prometheus.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme = Path("kaelos_prometheus/README.md")
long_description = readme.read_text() if readme.exists() else ""

setup(
    name="kaelos-prometheus",
    version="2.0.0",
    description="Autonomous Dialectical Evolution System with Foundry, LiveTrace, and CLA",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="KaelOS Team",
    author_email="kaelos@example.com",
    url="https://github.com/kaelos/prometheus",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        # Minimal dependencies - stdlib only
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "mypy>=0.950",
        ],
        "crypto": [
            "pynacl>=1.5.0",  # For production ed25519 signatures
        ],
    },
    entry_points={
        "console_scripts": [
            "kaelos=kaelos_prometheus.cli.main:cli",
            "kaelos-first-run=kaelos_prometheus.first_run:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="autonomous dialectical ai synthesis prometheus foundry livetrace",
)
