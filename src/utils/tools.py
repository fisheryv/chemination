"""Utility functions for the Chemination game.

This module contains various utility functions used throughout the game,
including resource management, image processing, and sprite handling.
"""

import os
import sys

import pygame
from pygame import BLEND_RGBA_MULT
from pathlib import Path

# PyInstaller creates a temp folder and stores path in `_MEIPASS`
# For Nuitka, the temp folder path is unknown.
# We have to get current running script path to find the base path
BASE_PATH = sys._MEIPASS if hasattr(sys, '_MEIPASS') else (
    Path(__file__).resolve().parent.parent.parent if "NUITKA_ONEFILE_PARENT" in os.environ else
    os.getcwd())


def create_alpha_image(image, alpha):
    """Create a copy of an image with specified alpha transparency.
    
    Args:
        image: Original image surface.
        alpha: Alpha transparency value (0-255).
        
    Returns:
        pygame.Surface: New image with specified alpha transparency.
    """
    alpha_image = image.copy()
    alpha_image.fill((255, 255, 255, alpha), None, BLEND_RGBA_MULT)
    return alpha_image


def resource_path(relative_path: str):
    """Get absolute path to resource, works for dev and bundled versions.
    
    This function handles resource paths for both development and bundled
    versions of the game (e.g., PyInstaller or Nuitka builds).
    
    Args:
        relative_path: Relative path to resource from the base directory.
        
    Returns:
        str: Absolute path to the resource.
    """
    return os.path.join(BASE_PATH, relative_path)


def load_sprite_sheet(filename: str, rows: int, cols: int,
                      directions: tuple = ('down', 'left', 'right', 'up'),
                      scale: float = 1.0) -> dict[str, list[pygame.Surface]]:
    """Load and split all frames from a multi-row sprite sheet.
    
    This function loads a sprite sheet image and splits it into individual frames
    organized by direction. It handles errors gracefully by providing substitute graphics.
    
    Args:
        filename:   Path to the sprite sheet file.
        rows:       Number of rows in the sprite sheet.
        cols:       Number of columns in the sprite sheet.
        directions: Direction labels for each row.
        scale:      Scaling factor for the frames.
        
    Returns:
        dict: Dictionary with direction keys and lists of frames as values.
    """
    try:
        filepath = resource_path(filename)
        sprite_sheet = pygame.image.load(filepath).convert_alpha()
    except pygame.error as e:
        print(f"Unable to load sprite sheet {filename}: {e}")
        # Create a simple substitute sprite sheet
        sprite_sheet = pygame.Surface((cols * 50, rows * 50), pygame.SRCALPHA)
        sprite_sheet.fill((200, 100, 100, 200))

    frame_width = sprite_sheet.get_width() // cols
    frame_height = sprite_sheet.get_height() // rows

    frames = {}

    for row in range(rows):
        direction_frames = []
        for col in range(cols):
            try:
                frame = sprite_sheet.subsurface(
                    pygame.Rect(col * frame_width, row * frame_height, frame_width, frame_height)
                )
            except ValueError:
                # If subsurface is out of bounds, create a default frame
                frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
                frame.fill((100, 200, 100, 200))

            # Scale frame
            if scale != 1:
                new_width = int(frame_width * scale)
                new_height = int(frame_height * scale)
                frame = pygame.transform.scale(frame, (new_width, new_height))
            direction_frames.append(frame)

        # Ensure direction label is within bounds
        direction_key = directions[row] if row < len(directions) else f"direction_{row}"
        frames[direction_key] = direction_frames

    return frames


def load_sprite_row(filename: str, cols: int, scale: float = 1.0) -> list[pygame.Surface]:
    """Load and split all frames from a single-row sprite sheet.
    
    This function loads a single-row sprite sheet image and splits it into individual frames.
    It handles errors gracefully by providing substitute graphics.
    
    Args:
        filename: Path to the sprite sheet file.
        cols:     Number of columns in the sprite sheet.
        scale:    Scaling factor for the frames.
        
    Returns:
        list: List of frames.
    """
    try:
        filepath = resource_path(filename)
        sprite_sheet = pygame.image.load(filepath).convert_alpha()
    except pygame.error as e:
        print(f"Unable to load sprite sheet {filename}: {e}")
        # Create a simple substitute sprite sheet
        sprite_sheet = pygame.Surface((cols * 50, 50), pygame.SRCALPHA)
        sprite_sheet.fill((100, 100, 200, 200))

    frame_width = sprite_sheet.get_width() // cols
    frame_height = sprite_sheet.get_height()

    direction_frames = []
    for col in range(cols):
        try:
            frame = sprite_sheet.subsurface(
                pygame.Rect(col * frame_width, 0, frame_width, frame_height)
            )
        except ValueError:
            # If subsurface is out of bounds, create a default frame
            frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            frame.fill((100, 200, 100, 200))

        # Scale frame
        if scale != 1:
            new_width = int(frame_width * scale)
            new_height = int(frame_height * scale)
            frame = pygame.transform.scale(frame, (new_width, new_height))
        direction_frames.append(frame)

    return direction_frames
