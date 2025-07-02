#!/usr/bin/env python3
"""Release script for Snake Game"""

import os
import sys
import subprocess
import platform
from pathlib import Path


def run_command(cmd, check=True):
    """Run shell command and return result"""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(1)
    return result


def build_package():
    """Build Python package"""
    print("🏗️  Building Python package...")
    
    # Clean previous builds
    run_command("rm -rf build/ dist/ *.egg-info/")
    
    # Build package
    run_command("python -m build")
    print("✅ Python package built successfully!")


def build_executable():
    """Build executable for current platform"""
    print(f"🔨 Building executable for {platform.system()}...")
    
    # Install PyInstaller if not available
    run_command("pip install pyinstaller", check=False)
    
    # Platform-specific settings
    if platform.system() == "Windows":
        exe_name = "SnakeGame.exe"
    else:
        exe_name = "SnakeGame"
    
    # Build executable
    cmd = f"""pyinstaller --onefile \
        --name "{exe_name}" \
        --add-data "config.json:." \
        snake_game/main.py"""
    
    run_command(cmd)
    print("✅ Executable built successfully!")


def create_release_archive():
    """Create release archive with all files"""
    print("📦 Creating release archive...")
    
    version = get_version()
    platform_name = platform.system().lower()
    
    # Create release directory
    release_dir = f"release/snake-game-{version}-{platform_name}"
    os.makedirs(release_dir, exist_ok=True)
    
    # Copy files
    files_to_copy = [
        "dist/SnakeGame*",
        "README.md",
        "config.json"
    ]
    
    for file_pattern in files_to_copy:
        run_command(f"cp -r {file_pattern} {release_dir}/", check=False)
    
    # Create archive
    archive_name = f"snake-game-{version}-{platform_name}.zip"
    run_command(f"cd release && zip -r {archive_name} snake-game-{version}-{platform_name}/")
    
    print(f"✅ Release archive created: release/{archive_name}")


def get_version():
    """Get current version from setup.py"""
    with open("setup.py", "r") as f:
        for line in f:
            if "version=" in line:
                return line.split('"')[1]
    return "unknown"


def main():
    """Main release process"""
    print("🚀 Starting Snake Game release process (Alpha)...")
    
    # Check if we're in the right directory
    if not os.path.exists("setup.py"):
        print("❌ Error: setup.py not found. Run this script from the snake/ directory.")
        sys.exit(1)
    
    # Install build dependencies
    print("📋 Installing dependencies...")
    run_command("pip install build twine pyinstaller")
    
    # Build everything
    build_package()
    build_executable()
    create_release_archive()
    
    print("🎉 Release process complete!")
    print(f"📦 Files created:")
    print(f"   - Python package: dist/*.whl")
    print(f"   - Executable: dist/SnakeGame*")
    print(f"   - Release archive: release/*.zip")


if __name__ == "__main__":
    main()
