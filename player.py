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
        pygame.draw.rect(surface, PLAYER_COLOR, self.rect, border_radius=4)