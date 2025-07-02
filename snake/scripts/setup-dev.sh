#!/bin/bash
# Development environment setup

set -e  # Exit on any error

echo "🚀 Setting up Snake Game development environment..."

# Check if we're in a virtual environment
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Warning: Not in a virtual environment"
    echo "   Consider running: python -m venv .venv && source .venv/bin/activate"
fi

# Install development dependencies
echo "📦 Installing development dependencies..."
pip install -e .[dev]

# Install additional development tools
echo "🔧 Installing development tools..."
pip install black flake8 mypy pytest-cov pre-commit build twine pyinstaller bumpversion

# Setup pre-commit hooks if .pre-commit-config.yaml exists
if [ -f .pre-commit-config.yaml ]; then
    echo "🪝 Setting up pre-commit hooks..."
    pre-commit install
else
    echo "ℹ️  No pre-commit config found, skipping hooks setup"
fi

# Create initial config files if missing
echo "⚙️  Setting up configuration files..."
if [ ! -f config.json ]; then
    echo "   Creating default config.json..."
    python -c "
try:
    from snake_game.config import CONFIG
    CONFIG.save_to_file('config.json')
    print('   ✅ config.json created')
except Exception as e:
    print(f'   ⚠️  Could not create config.json: {e}')
"
fi

# Create logs directory if missing
if [ ! -d logs ]; then
    echo "   Creating logs directory..."
    mkdir -p logs
    echo "   ✅ logs/ directory created"
fi

# Run initial tests to make sure everything works
echo "🧪 Running initial tests..."
if python -m pytest tests/ -q; then
    echo "   ✅ All tests passing"
else
    echo "   ⚠️  Some tests failed - check your setup"
fi

# Test if the game can be imported
echo "🎮 Testing game import..."
if python -c "from snake_game import SnakeGame; print('✅ Game import successful')"; then
    echo "   ✅ Snake game ready to run"
else
    echo "   ❌ Game import failed - check dependencies"
    exit 1
fi

echo ""
echo "🎉 Development environment setup complete!"
echo ""
echo "Quick start commands:"
echo "  python run_snake.py    # Test the game"
echo "  pytest tests/          # Run tests"
echo "  make test              # Run full test suite"
echo "  make build             # Build package"
echo ""
echo "See DEVELOPMENT.md for detailed workflow information."
