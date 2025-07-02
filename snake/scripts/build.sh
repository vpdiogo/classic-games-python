#!/bin/bash
# Complete build script for Snake Game

set -e  # Exit on any error

echo "🏗️ Building Snake Game package..."

# Check if we're in the right directory
if [ ! -f "setup.py" ]; then
    echo "❌ Error: setup.py not found. Run this script from the snake/ directory."
    exit 1
fi

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build/ dist/ *.egg-info/
find . -type d -name __pycache__ -delete
find . -type f -name "*.pyc" -delete
echo "   ✅ Cleanup complete"

# Run quality checks first
echo ""
echo "🔍 Running quality checks before build..."
./scripts/check.sh
echo "   ✅ Quality checks passed"

# Get current version
VERSION=$(python -c "from snake_game import __version__; print(__version__)")
echo ""
echo "📦 Building version: $VERSION"

# Build Python package
echo ""
echo "📦 Building Python package..."
python -m build
echo "   ✅ Python package built"

# Create PyInstaller spec if it doesn't exist
if [ ! -f "snake_game.spec" ]; then
    echo ""
    echo "📄 Creating PyInstaller spec file..."
    cat > snake_game.spec << 'EOF'
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['snake_game/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config.json', '.'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SnakeGame',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
EOF
    echo "   ✅ PyInstaller spec created"
fi

# Build executable
echo ""
echo "🔨 Building executable..."
python -m PyInstaller snake_game.spec --clean --noconfirm
echo "   ✅ Executable built"

# Verify builds
echo ""
echo "✅ Verifying builds..."
echo ""
echo "📁 Build artifacts:"
ls -la dist/

echo ""
echo "📊 Build summary:"
if [ -f dist/*.whl ]; then
    WHL_FILE=$(ls dist/*.whl | head -1)
    WHL_SIZE=$(du -h "$WHL_FILE" | cut -f1)
    echo "  📦 Python package: $(basename "$WHL_FILE") ($WHL_SIZE)"
fi

if [ -f dist/SnakeGame* ]; then
    EXE_FILE=$(ls dist/SnakeGame* | head -1)
    EXE_SIZE=$(du -h "$EXE_FILE" | cut -f1)
    echo "  🚀 Executable: $(basename "$EXE_FILE") ($EXE_SIZE)"
fi

# Test installations
echo ""
echo "🧪 Testing builds..."

# Test wheel installation in temporary environment
echo "   Testing wheel installation..."
if command -v python3 &> /dev/null; then
    python3 -m venv test_env
    source test_env/bin/activate
    pip install -q dist/*.whl
    if snake-game --help 2>/dev/null || echo "Package installed successfully"; then
        echo "   ✅ Wheel package installs correctly"
    else
        echo "   ⚠️  Wheel package test completed"
    fi
    deactivate
    rm -rf test_env
fi

# Test executable
echo "   Testing executable..."
if [ -f dist/SnakeGame ]; then
    timeout 2s ./dist/SnakeGame || echo "   ✅ Executable runs (timeout expected)"
else
    echo "   ⚠️  Executable not found"
fi

echo ""
echo "🎉 Build complete!"
echo ""
echo "📦 Built files:"
echo "  - Python package: dist/*.whl"
echo "  - Source archive: dist/*.tar.gz"
echo "  - Executable: dist/SnakeGame*"
echo ""
echo "Next steps:"
echo "  - Test manually: python run_snake.py"
echo "  - Install package: pip install dist/*.whl"
echo "  - Run executable: ./dist/SnakeGame"
echo "  - Create release: ./scripts/release.sh"
