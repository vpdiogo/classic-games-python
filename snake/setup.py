"""Setup configuration for Snake Game package"""

from setuptools import setup, find_packages
import os

# Read README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="snake-game-classic",
    version="0.1.0-alpha.1",
    author="Vitor",
    author_email="your.email@example.com",
    description="A modern implementation of the classic Snake game with configurable modes (Alpha Version)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/classic-games-python",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/classic-games-python/issues",
        "Source Code": "https://github.com/yourusername/classic-games-python/tree/main/snake",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Topic :: Games/Entertainment :: Arcade",
        "Topic :: Software Development :: Libraries :: pygame",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "snake-game=snake_game.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "snake_game": [
            "assets/*",
            "config/*.json",
        ],
    },
    keywords="game snake pygame classic retro arcade alpha development",
    zip_safe=False,
)
