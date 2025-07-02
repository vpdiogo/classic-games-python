#!/bin/bash
# Complete release script for Snake Game

set -e  # Exit on any error

echo "🚀 Starting Snake Game release process..."

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: pyproject.toml not found. Run this script from the snake/ directory."
    exit 1
fi

# Check if git is available and we're in a git repo
if ! command -v git &> /dev/null; then
    echo "⚠️  Git not found. Skipping git checks..."
    SKIP_GIT=true
else
    SKIP_GIT=false
fi

if [ "$SKIP_GIT" = false ]; then
    # Check if we're on main branch (optional warning)
    BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
    if [ "$BRANCH" != "main" ] && [ "$BRANCH" != "master" ]; then
        echo "⚠️  Warning: Not on main/master branch (current: $BRANCH)"
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "❌ Release cancelled"
            exit 1
        fi
    fi

    # Check if working directory is clean (optional warning)
    if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
        echo "⚠️  Warning: Working directory has uncommitted changes"
        git status --short
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "❌ Release cancelled"
            exit 1
        fi
    fi
fi

# Get current version from pyproject.toml directly
VERSION=$(python -c "
import re
with open('pyproject.toml', 'r') as f:
    content = f.read()
    version_match = re.search(r'version\s*=\s*[\"\'](.*?)[\"\']', content)
    if version_match:
        print(version_match.group(1))
    else:
        print('unknown')
" 2>/dev/null)

echo "📋 Current version: $VERSION"

# Run all quality checks
echo ""
echo "🔍 Running pre-release checks..."
./scripts/check.sh

# Build everything
echo ""
echo "🏗️ Building release packages..."
./scripts/build.sh

# Update changelog with release info
echo ""
echo "📝 Updating CHANGELOG.md..."
DATE=$(date +%Y-%m-%d)

# Create temporary changelog entry
cat > temp_changelog_entry.md << EOF
## [$VERSION] - $DATE

### Changes in this release:
- Bug fixes and improvements
- Updated documentation
- Package optimizations

EOF

# Backup original changelog
cp CHANGELOG.md CHANGELOG.md.backup

# Merge changelogs
cat temp_changelog_entry.md CHANGELOG.md.backup > CHANGELOG.md
rm temp_changelog_entry.md CHANGELOG.md.backup

echo "   ✅ CHANGELOG.md updated"

# Create release directory structure
echo ""
echo "📦 Creating release package..."
RELEASE_DIR="release/snake-game-$VERSION"
mkdir -p "$RELEASE_DIR"

# Copy release files
cp dist/*.whl "$RELEASE_DIR/"
cp dist/*.tar.gz "$RELEASE_DIR/"
if [ -f dist/SnakeGame ]; then
    cp dist/SnakeGame "$RELEASE_DIR/"
fi
cp README.md "$RELEASE_DIR/"
cp LICENSE "$RELEASE_DIR/"
cp docs/INSTALL.md "$RELEASE_DIR/"
cp CHANGELOG.md "$RELEASE_DIR/"

# Create release archive
cd release
ARCHIVE_NAME="snake-game-$VERSION-$(uname -s | tr '[:upper:]' '[:lower:]').zip"
zip -r "$ARCHIVE_NAME" "snake-game-$VERSION/"
cd ..

echo "   ✅ Release archive created: release/$ARCHIVE_NAME"

# Generate release notes
echo ""
echo "📄 Generating release notes..."
cat > "release/RELEASE_NOTES_$VERSION.md" << EOF
# Snake Game $VERSION Release Notes

## Installation

### From Package (Recommended)
\`\`\`bash
pip install snake_game_classic-$VERSION-py3-none-any.whl
snake-game
\`\`\`

### From Executable
\`\`\`bash
# Download and run the executable
./SnakeGame
\`\`\`

### From Source
\`\`\`bash
pip install snake_game_classic-$VERSION.tar.gz
snake-game
\`\`\`

## Features

- 🐍 Classic Snake gameplay with modern features
- 🎮 Complete menu system
- ⚙️ Configurable settings (wall collision, speed)
- 🏆 High score tracking
- 🎯 Two game modes: Classic and Wrap-around
- ⌨️ Multiple input methods (Arrow keys, WASD)

## Requirements

- Python 3.8+
- Pygame 2.1.0+

## Platform Support

- ✅ Linux
- ✅ Windows
- ✅ macOS

## Known Issues

- Some edge cases in wrap-around mode may need polish
- First run may take longer to load

## Changelog

See CHANGELOG.md for detailed changes.

## Support

For issues or questions, please check the documentation or create an issue on GitHub.
EOF

echo "   ✅ Release notes created: release/RELEASE_NOTES_$VERSION.md"

# Final verification
echo ""
echo "🧪 Final release verification..."

# Check package integrity
echo "   Checking package integrity..."
python -m zipfile -l dist/*.whl >/dev/null 2>&1 && echo "   ✅ Wheel package is valid"

# Test installation one more time
echo "   Testing final installation..."
python -m venv final_test_env
source final_test_env/bin/activate
pip install -q dist/*.whl
python -c "from snake_game import __version__; print(f'✅ Package version: {__version__}')"
deactivate
rm -rf final_test_env

echo ""
echo "🎉 Release $VERSION completed successfully!"
echo ""
echo "📦 Release artifacts:"
echo "  - Python package: dist/snake_game_classic-$VERSION-py3-none-any.whl"
echo "  - Source archive: dist/snake_game_classic-$VERSION.tar.gz"
if [ -f dist/SnakeGame ]; then
    echo "  - Executable: dist/SnakeGame"
fi
echo "  - Release archive: release/$ARCHIVE_NAME"
echo "  - Release notes: release/RELEASE_NOTES_$VERSION.md"
echo ""
echo "🚀 Next steps:"
if [ "$SKIP_GIT" = false ]; then
    echo "  1. Review CHANGELOG.md and commit changes:"
    echo "     git add ."
    echo "     git commit -m 'Release v$VERSION'"
    echo "  2. Create and push git tag:"
    echo "     git tag v$VERSION"
    echo "     git push origin main --tags"
fi
echo "  3. Upload to PyPI (when ready):"
echo "     twine upload dist/*.whl dist/*.tar.gz"
echo "  4. Create GitHub release with release/$ARCHIVE_NAME"
echo "  5. Share the release with users!"
echo ""
echo "Happy releasing! 🎮🚀"
