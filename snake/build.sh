#!/bin/bash

# Build script for Snake Game (Alpha)

echo "🐍 Building Snake Game Package (Alpha v0.1.0-alpha.1)..."

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build/ dist/ *.egg-info/

# Install build dependencies
echo "Installing build dependencies..."
pip install build twine bumpversion

# Build the package
echo "Building package..."
python -m build

# Build executable with PyInstaller
echo "Building executable..."
pip install pyinstaller

# Create executable for current platform
pyinstaller --onefile \
    --windowed \
    --name "SnakeGame" \
    --add-data "snake_game/assets:snake_game/assets" \
    --add-data "config.json:." \
    snake_game/main.py

echo "✅ Build complete!"
echo "📦 Package: dist/*.whl"
echo "🚀 Executable: dist/SnakeGame"
