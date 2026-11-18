# settings.py
WIDTH, HEIGHT = 800, 600
FPS = 60

# Física de Plataforma
GRAVITY = 0.8
PLAYER_SPEED = 5
JUMP_FORCE = -15
COYOTE_TIME = 6        # Frames de tolerância ao cair de uma plataforma
JUMP_BUFFER_TIME = 6   # Frames para memorizar o pulo antes de tocar o chão

# Paleta de Cores (Estilo Level Devil)
BG_COLOR = (238, 226, 200)          # Bege claro
WALL_COLOR = (55, 40, 30)           # Marrom café profundo
PLAYER_COLOR = (25, 25, 25)         # Grafite escuro
SPIKE_COLOR = (210, 45, 45)         # Vermelho alerta
GOAL_COLOR = (40, 160, 75)          # Verde sucesso
NF_COLOR = (35, 105, 220)           # Azul tributo
TRANSPARENCY_COLOR = (130, 40, 215) # Roxo Portal GOV
FAKE_WALL_COLOR = (220, 80, 80)     # Vermelho desvio
REAL_WALL_COLOR = (40, 160, 75)     # Verde investimento
COIN_COLOR = (240, 180, 25)         # Dourado
URN_COLOR = (30, 90, 155)           # Azul escuro urna
WHITE = (255, 255, 255)
TEXT_BG = (20, 20, 20)