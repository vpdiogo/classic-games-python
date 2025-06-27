#!/usr/bin/env python3
"""
Launcher script for Snake Game
"""

import sys
import os

# Adiciona o diretório do jogo ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from snake_game import main

if __name__ == "__main__":
    main()
