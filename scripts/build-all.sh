#!/bin/bash
# Global build script for Classic Games Python Collection

set -e

echo "🎮 Classic Games Python - Global Build Script"
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to build a specific game
build_game() {
    local game_name=$1
    local game_dir=$2

    if [ ! -d "$game_dir" ]; then
        print_warning "Game directory $game_dir not found, skipping $game_name"
        return 0
    fi

    print_status "Building $game_name..."

    cd "$game_dir"

    # Check if Makefile exists
    if [ -f "Makefile" ]; then
        print_status "Using Makefile for $game_name"
        make clean
        make build
    else
        print_status "Using direct build for $game_name"
        # Fallback to direct build
        python -m build
    fi

    cd ..
    print_success "$game_name build completed"
}

# Function to test a specific game
test_game() {
    local game_name=$1
    local game_dir=$2

    if [ ! -d "$game_dir" ]; then
        print_warning "Game directory $game_dir not found, skipping $game_name tests"
        return 0
    fi

    print_status "Testing $game_name..."

    cd "$game_dir"

    # Check if Makefile exists
    if [ -f "Makefile" ]; then
        make test
    else
        # Fallback to direct pytest
        pytest tests/ -v
    fi

    cd ..
    print_success "$game_name tests completed"
}

# Main execution
case "${1:-build}" in
    "test")
        print_status "Running tests for all games..."
        test_game "Snake" "snake"
        # Add future games here:
        # test_game "Pong" "pong"
        # test_game "Tetris" "tetris"
        print_success "All tests completed!"
        ;;

    "build")
        print_status "Building all games..."
        build_game "Snake" "snake"
        # Add future games here:
        # build_game "Pong" "pong"
        # build_game "Tetris" "tetris"
        print_success "All builds completed!"
        ;;

    "clean")
        print_status "Cleaning all game builds..."
        for game_dir in snake pong tetris; do
            if [ -d "$game_dir" ]; then
                cd "$game_dir"
                if [ -f "Makefile" ]; then
                    make clean
                else
                    rm -rf build/ dist/ *.egg-info/
                fi
                cd ..
                print_success "Cleaned $game_dir"
            fi
        done
        ;;

    "check")
        print_status "Running quality checks for all games..."
        for game_dir in snake pong tetris; do
            if [ -d "$game_dir" ]; then
                print_status "Checking $game_dir..."
                cd "$game_dir"
                if [ -f "Makefile" ]; then
                    make check
                else
                    # Fallback quality checks
                    if command -v black &> /dev/null; then
                        black --check . || true
                    fi
                    if command -v flake8 &> /dev/null; then
                        flake8 . || true
                    fi
                fi
                cd ..
            fi
        done
        print_success "Quality checks completed!"
        ;;

    "help"|"-h"|"--help")
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  build    - Build all games (default)"
        echo "  test     - Run tests for all games"
        echo "  clean    - Clean build artifacts for all games"
        echo "  check    - Run quality checks for all games"
        echo "  help     - Show this help message"
        echo ""
        echo "Examples:"
        echo "  $0 build    # Build all games"
        echo "  $0 test     # Test all games"
        echo "  $0 clean    # Clean all builds"
        ;;

    *)
        print_error "Unknown command: $1"
        print_status "Use '$0 help' for usage information"
        exit 1
        ;;
esac

echo ""
print_success "Global build script completed!"
