# Chemination

An educational chemistry game built with Python and Pygame where players catch falling chemical formula blocks.

## Description

Chemination is an educational game that helps players learn chemistry concepts through gameplay. Players choose to play as an acid, base, or salt character and must catch falling chemical formula blocks that match their character type.

## Features

- Over 150 chemical formulas across acids, bases, and salts
- Progressive difficulty levels
- HP system with automatic decay over time
- Score tracking based on successful catches
- Visual effects for correct/incorrect catches
- Background music
- Three playable character types: Acid (red), Base (blue), Salt (green)

## Installation

1. Clone or download this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## How to Play

1. Run the game:
   ```
   python main.py
   ```
2. Select your character (acid, base, or salt) from the main menu
3. Use the left and right arrow keys (or A/D keys) to move your character
4. Catch falling chemical formula blocks that match your character type:
   - Acid character catches acid formulas
   - Base character catches base formulas
   - Salt character catches salt formulas
5. Game rules:
   - Correct catches: +5 HP, +10 points
   - Wrong catches: -30 HP
   - Missed blocks of your type: -20 HP
   - Automatic HP decay: -3 HP per second
   - Game ends when HP reaches zero
6. Music controls:
   - Press 'M' key to toggle background music on/off

## Project Structure

The project has been modularized for better maintainability:

```
chemgame/
├── main.py          # Main entry point
├── src/             # Source code directory
│   ├── config/      # Configuration and settings
│   ├── data/        # Game data (chemical databases)
│   ├── entities/    # Game entities (player, blocks)
│   ├── utils/       # Utility modules (effects, HUD)
│   └── game/        # Main game logic
├── audio/           # Audio files
│   └── bgm.mp3      # Background music file
├── images/          # Image assets
├── requirements.txt # Python dependencies
└── README.md        # This file
```

## Requirements

- Python 3.x
- Pygame 2.6.1

## Packaging

```bash
pyinstaller main.spec
```

## Credits

This game was developed with Lucas Gao.

## License

This project is open source and available under the MIT License.