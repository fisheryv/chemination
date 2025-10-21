import pygame

from src.config.settings import get_option
from src.utils.tools import resource_path

music_loaded = False
music_playing = False


def load_background_music(bgm: str):
    """加载背景音乐"""
    global music_loaded
    try:
        music_path = resource_path("assets/audios/" + bgm)
        pygame.mixer.music.load(resource_path(music_path))
        pygame.mixer.music.set_volume(0.7)  # 设置音量
        music_loaded = True
        # 根据设置决定是否播放音乐
        if get_option("game", "music") == "off":
            stop_background_music()
        else:
            play_background_music()
    except pygame.error as e:
        music_loaded = False
    except Exception as e:
        music_loaded = False


def play_background_music():
    """播放背景音乐"""
    global music_playing
    if music_loaded:
        pygame.mixer.music.play(-1)  # -1 表示循环播放
        music_playing = True


def stop_background_music():
    """停止背景音乐"""
    global music_playing
    pygame.mixer.music.stop()
    music_playing = False


def pause_background_music():
    """暂停背景音乐"""
    global music_playing
    pygame.mixer.music.pause()
    music_playing = False


def resume_background_music():
    """恢复背景音乐"""
    global music_playing
    pygame.mixer.music.unpause()
    music_playing = True
