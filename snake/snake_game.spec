# -*- mode: python ; coding: utf-8 -*-
import os
import sys

block_cipher = None

# Analysis of the main script
a = Analysis(
    ['run_snake.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('snake_game/assets', 'snake_game/assets') if os.path.exists('snake_game/assets') else ('snake_game', 'snake_game'),
    ],
    hiddenimports=[
        'pygame',
        'pygame.mixer',
        'pygame.font',
        'pygame.image',
        'pygame.key',
        'pygame.mouse',
        'pygame.display',
        'pygame.event',
        'pygame.time',
        'pygame.transform',
        'pygame.surface',
        'pygame.rect',
        'pygame.color',
        'snake_game.config',
        'snake_game.game',
        'snake_game.game_objects',
        'snake_game.input_handler',
        'snake_game.high_score',
        'snake_game.logger',
        'snake_game.menu',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'IPython',
        'jupyter',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Filter out None values from datas
a.datas = [x for x in a.datas if x is not None]

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
    console=False,  # Set to True for debug console
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon path here if available
)

# macOS specific bundle (optional)
if sys.platform == 'darwin':
    app = BUNDLE(
        exe,
        name='SnakeGame.app',
        icon=None,  # Add icon path here if available
        bundle_identifier='com.classicgames.snake',
        info_plist={
            'NSPrincipalClass': 'NSApplication',
            'NSAppleScriptEnabled': False,
            'CFBundleDocumentTypes': [
                {
                    'CFBundleTypeName': 'Snake Game',
                    'CFBundleTypeRole': 'Viewer',
                    'LSHandlerRank': 'Owner',
                }
            ]
        },
    )
