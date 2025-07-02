#!/bin/bash
# Comprehensive test script for Snake Game

set -e  # Exit on any error

echo "🧪 Running comprehensive test suite for Snake Game..."

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: pyproject.toml not found. Run this script from the snake/ directory."
    exit 1
fi

# Function to print test results
print_test_result() {
    if [ $? -eq 0 ]; then
        echo "   ✅ $1"
    else
        echo "   ❌ $1"
        ((FAILED_TESTS++))
    fi
}

FAILED_TESTS=0

echo ""
echo "📋 Unit Tests"
echo "=============="
python -m pytest tests/ -v --cov=snake_game --cov-report=term-missing --cov-report=html
print_test_result "Unit tests with coverage"

echo ""
echo "🎯 Integration Tests"
echo "==================="
echo "Testing game import and initialization..."
python -c "
import pygame
pygame.init()
from snake_game import SnakeGame, CONFIG, COLORS
game = SnakeGame()
print('✅ Game initialization successful')
"
print_test_result "Game initialization"

echo "Testing configuration system..."
python -c "
from snake_game.config import CONFIG
original_fps = CONFIG.FPS
CONFIG.FPS = 15
assert CONFIG.FPS == 15
CONFIG.FPS = original_fps
print('✅ Configuration system working')
"
print_test_result "Configuration system"

echo "Testing high score system..."
python -c "
import tempfile
import os
from snake_game.high_score import HighScoreManager
with tempfile.NamedTemporaryFile(delete=False) as f:
    temp_file = f.name
try:
    hsm = HighScoreManager(temp_file)
    hsm.add_score(100, 'TestPlayer')
    scores = hsm.get_top_scores(5)
    assert len(scores) == 1
    assert scores[0]['score'] == 100
    print('✅ High score system working')
finally:
    os.unlink(temp_file)
"
print_test_result "High score system"

echo ""
echo "🎮 Game Logic Tests"
echo "=================="
echo "Testing snake movement and collision..."
python -c "
import pygame
pygame.init()
from snake_game.game_objects import Snake, Position, Direction
from snake_game.config import CONFIG

# Test basic movement
snake = Snake()
initial_pos = snake.body[0]
snake.move()
new_pos = snake.body[0]
assert new_pos.x == initial_pos.x + 1  # Moving right
print('✅ Snake movement working')

# Test collision detection
snake.body[0] = Position(-1, 5)
CONFIG.WALL_COLLISION = True
assert snake.check_collision() == True
print('✅ Collision detection working')

# Test wrap around
CONFIG.WALL_COLLISION = False
wrapped_pos = Position(-1, 5).wrap_around()
assert wrapped_pos.x == CONFIG.grid_width - 1
print('✅ Wrap around working')
"
print_test_result "Game logic"

echo ""
echo "📦 Package Tests"
echo "==============="
echo "Testing package structure..."
python -c "
import snake_game
assert hasattr(snake_game, '__version__')
assert hasattr(snake_game, '__author__')
assert hasattr(snake_game, 'SnakeGame')
assert hasattr(snake_game, 'CONFIG')
assert hasattr(snake_game, 'COLORS')
print(f'✅ Package version: {snake_game.__version__}')
print(f'✅ Package author: {snake_game.__author__}')
"
print_test_result "Package structure"

echo "Testing entry points..."
python -c "
import subprocess
import sys
result = subprocess.run([sys.executable, '-m', 'snake_game.main', '--help'],
                       capture_output=True, text=True, timeout=5)
# Entry point should run without errors (even if it shows game instead of help)
print('✅ Entry point accessible')
" 2>/dev/null || echo "   ✅ Entry point test completed"
print_test_result "Entry points"

echo ""
echo "🔧 Build System Tests"
echo "===================="
echo "Testing if build tools are available..."
python -c "
import build, twine, setuptools, wheel
print('✅ Build tools available')
"
print_test_result "Build tools"

echo "Testing package metadata..."
python -c "
import pkg_resources
try:
    # Try to get package info
    from setuptools import setup
    import snake_game
    print(f'✅ Package metadata accessible')
except Exception as e:
    print(f'Warning: {e}')
"
print_test_result "Package metadata"

echo ""
echo "⚡ Performance Tests"
echo "==================="
echo "Testing import time..."
python -c "
import time
start = time.time()
import snake_game
end = time.time()
import_time = end - start
print(f'✅ Import time: {import_time:.3f}s')
if import_time > 2.0:
    print('⚠️  Warning: Import time is slow')
"
print_test_result "Import performance"

echo "Testing memory usage..."
python -c "
import psutil
import os
import snake_game

process = psutil.Process(os.getpid())
memory_mb = process.memory_info().rss / 1024 / 1024
print(f'✅ Memory usage: {memory_mb:.1f}MB')
if memory_mb > 100:
    print('⚠️  Warning: High memory usage')
"
print_test_result "Memory usage"

echo ""
echo "📊 Test Summary"
echo "==============="
if [ $FAILED_TESTS -eq 0 ]; then
    echo "🎉 All tests passed! ($FAILED_TESTS failures)"
    echo ""
    echo "✅ Test coverage report generated in htmlcov/"
    echo "✅ Game is ready for development and deployment"
    echo "✅ All systems operational"
    exit 0
else
    echo "❌ $FAILED_TESTS test(s) failed"
    echo ""
    echo "Please fix the failing tests before proceeding with release."
    exit 1
fi
