"""Game configuration and settings module.

This module contains all game configuration settings, constants, and functions
for loading and saving user preferences. It defines game window dimensions,
colors, custom events, and handles the loading of settings from an INI file.
"""

import configparser
import os
import pygame

from src.utils.tools import resource_path

# Game basic information
GAME_NAME = "Chemination"
VERSION = "0.9.0"

# Game window settings
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 675
FPS = 60

# Color definitions
WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)
RED = pygame.Color(255, 100, 100)
BLUE = pygame.Color(100, 100, 255)
GREEN = pygame.Color(100, 255, 100)
YELLOW = pygame.Color(255, 255, 0)
GOLD = pygame.Color(218, 165, 32)
GRAY = pygame.Color(200, 200, 200)
DARK_GRAY = pygame.Color(100, 100, 100)
DARK_RED = pygame.Color(128, 52, 52)
DARK_BLUE = pygame.Color(52, 95, 130)
DARK_GREEN = pygame.Color(77, 127, 52)
PINK = pygame.Color(229, 71, 130)
CYAN = pygame.Color(65, 166, 220)

# Custom events
ENEMY_ESCAPED = pygame.USEREVENT + 1  # Enemy escaped event
ENEMY_KILLED = pygame.USEREVENT + 2  # Enemy killed event
HERO_ATTACK = pygame.USEREVENT + 3  # Hero attack event

# Default setting options
OPTIONS = {
    "game": {
        "intro": "on",
        "music": "on",
    }
}

# Configuration file path
config_file = resource_path("setting.ini")
config = configparser.ConfigParser()


def load_settings():
    """Load game settings from the INI configuration file.
    
    If the configuration file doesn't exist, creates default settings and saves them.
    Handles any exceptions that occur during the loading process.
    """
    try:
        if os.path.exists(config_file):
            config.read(config_file)
        else:
            # If file doesn't exist, create default settings
            for section, options in OPTIONS.items():
                config[section] = options
            save_settings()
    except Exception as e:
        print(f"Error loading settings: {e}")


def save_settings():
    """Save current game settings to the INI configuration file.
    
    Writes the current configuration to the settings file. Handles any exceptions
    that occur during the saving process.
    """
    try:
        with open(config_file, 'w') as f:
            config.write(f)
    except Exception as e:
        print(f"Error saving settings: {e}")


def get_option(section: str, key: str) -> str | None:
    """Get a setting value from the configuration.
    
    Args:
        section: The section name in the configuration file.
        key:     The key name within the section.
        
    Returns:
        str | None: The value associated with the key, or None if not found.
    """
    try:
        return config.get(section, key)
    except:
        return None


def set_option(section: str, key: str, value):
    """Set a setting value in the configuration.
    
    Args:
        section: The section name in the configuration file.
        key:     The key name within the section.
        value:   The value to set for the key.
    """
    if section not in config:
        config[section] = {}
    config[section][key] = str(value)