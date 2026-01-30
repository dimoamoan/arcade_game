import arcade

# Размеры экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Space Adventure: Pro Version"

# Настройки скоростей
PLAYER_SPEED = 5
BULLET_SPEED = 8
ALIEN_SPEED = 3
RESOURCE_SPEED = 2

# Условия победы
WIN_SCORE = 100
WIN_RESOURCES = 100

# Пути к изображениям (положи файлы в папку с кодом)
BACKGROUND_PATH = "background.png"

# Пути к звукам (поддерживаются .wav, .mp3, .ogg)
SOUND_SHOOT = "shoot.wav"
SOUND_COLLECT = "collect.wav"
SOUND_HIT = "hit.wav"

# Состояния игры
STATE_PLAYING = 0
STATE_WON = 1
STATE_LOST = 2