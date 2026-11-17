# player.py
import pygame
from settings import *

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 32, 32)
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.alive = True

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.vel_x = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = PLAYER_SPEED
        if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and self.on_ground:
            self.vel_y = JUMP_FORCE
            self.on_ground = False

    def update(self, platforms):
        if not self.alive:
            return

        self.handle_input()

        # 1. Movimento Horizontal + Colisão
        self.rect.x += self.vel_x
        for plat in platforms:
            if plat["solid"] and self.rect.colliderect(plat["rect"]):
                if self.vel_x > 0:
                    self.rect.right = plat["rect"].left
                elif self.vel_x < 0:
                    self.rect.left = plat["rect"].right

        # 2. Movimento Vertical (Gravidade) + Colisão
        self.vel_y += GRAVITY
        self.rect.y += int(self.vel_y)
        self.on_ground = False

        for plat in platforms:
            if plat["solid"] and self.rect.colliderect(plat["rect"]):
                if self.vel_y > 0:
                    self.rect.bottom = plat["rect"].top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = plat["rect"].bottom
                    self.vel_y = 0

        # Morte se cair fora da tela
        if self.rect.top > HEIGHT:
            self.alive = False

    def draw(self, surface):
        if not self.alive:
            return

        # 1. Corpo principal: Retângulo escuro e arredondado (Corpo)
        pygame.draw.rect(surface, PLAYER_COLOR, self.rect, border_radius=6)

        # 2. Detalhe de Sombra: Uma borda ou base levemente mais escura para dar profundidade
        sombra_rect = pygame.Rect(self.rect.x + 2, self.rect.bottom - 6, self.rect.width - 4, 4)
        pygame.draw.rect(surface, (15, 15, 15), sombra_rect, border_radius=2)

        # 3. Lógica dos Olhos dinâmicos (expressão estilo Level Devil)
        # O tamanho dos olhos e a pupila
        olho_largura, olho_altura = 6, 8
        pupila_largura, pupila_altura = 3, 4

        # Determina para onde os olhos olham com base na direção do movimento (vel_x)
        deslocamento_olhar = 0
        if self.vel_x > 0:
            deslocamento_olhar = 3   # Olha para a direita
        elif self.vel_x < 0:
            deslocamento_olhar = -3  # Olha para a esquerda

        # Altura dos olhos (se estiver caindo ou pulando, os olhos sobem ou descem um pouco)
        deslocamento_altura = 0
        if self.vel_y < -2:
            deslocamento_altura = -2  # Olhando para cima ao pular
        elif self.vel_y > 2:
            deslocamento_altura = 2   # Olhando para baixo ao cair

        # Posições de referência para os olhos dentro da cabeça
        olho_esq_x = self.rect.x + 6 + deslocamento_olhar
        olho_dir_x = self.rect.x + 18 + deslocamento_olhar
        olho_y = self.rect.y + 8 + deslocamento_altura

        # Desenhar o "Branco" dos Olhos
        olho_esq = pygame.Rect(olho_esq_x, olho_y, olho_largura, olho_altura)
        olho_dir = pygame.Rect(olho_dir_x, olho_y, olho_largura, olho_altura)
        pygame.draw.rect(surface, WHITE, olho_esq, border_radius=2)
        pygame.draw.rect(surface, WHITE, olho_dir, border_radius=2)

        # Desenhar as "Pupilas" (olhando para a mesma direção de movimento)
        direcao_pupila_x = 1 if self.vel_x >= 0 else -1
        pupila_esq = pygame.Rect(olho_esq_x + 1 + direcao_pupila_x, olho_y + 2, pupila_largura, pupila_altura)
        pupila_dir = pygame.Rect(olho_dir_x + 1 + direcao_pupila_x, olho_y + 2, pupila_largura, pupila_altura)
        pygame.draw.rect(surface, PLAYER_COLOR, pupila_esq, border_radius=1)
        pygame.draw.rect(surface, PLAYER_COLOR, pupila_dir, border_radius=1)