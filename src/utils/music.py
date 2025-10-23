"""Music and audio management for the Chemination game.

This module contains functions for loading, playing, pausing, and stopping
background music and sound effects.
"""

import pygame

from src.config.settings import get_option
from src.utils.tools import resource_path

music_loaded = False


def load_background_music(bgm: str, volume: float = 0.7):
    """Load a background music file for playback.
    
    Args:
        bgm:    Background music filename.
        volume: Volume level for the music (default: 0.7).
    """
    global music_loaded
    try:
        music_path = resource_path("assets/audios/" + bgm)
        pygame.mixer.music.load(resource_path(music_path))
        pygame.mixer.music.set_volume(volume)  # Set music volume
        music_loaded = True
        # Play music based on settings
        if get_option("game", "music") == "off":
            stop_background_music()
        else:
            play_background_music()
    except pygame.error as e:
        music_loaded = False
    except Exception as e:
        music_loaded = False


def play_background_music(loops: int = -1):
    """Play the loaded background music in loop.
    
    Args:
        loops: Loop counts (default: -1 means infinite loop).
    """
    if music_loaded:
        pygame.mixer.music.play(loops)  # -1 means loop playback


def stop_background_music():
    """Stop the background music."""
    pygame.mixer.music.stop()


def pause_background_music():
    """Pause the background music."""
    pygame.mixer.music.pause()


def resume_background_music():
    """Resume the paused background music."""
    pygame.mixer.music.unpause()
