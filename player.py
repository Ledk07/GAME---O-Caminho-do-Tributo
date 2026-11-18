# player.py
import pygame
import random
from settings import *

class DeathParticle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, random.randint(5, 9), random.randint(5, 9))
        self.vel_x = random.uniform(-6, 6)
        self.vel_y = random.uniform(-10, -2)
        self.gravity = 0.6
        self.color = PLAYER_COLOR

    def update(self):
        self.vel_y += self.gravity
        self.rect.x += int(self.vel_x)
        self.rect.y += int(self.vel_y)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=2)

class Player:
    def __init__(self, x, y):
        self.start_x = x
        self.start_y = y
        self.rect = pygame.Rect(x, y, 32, 32)
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.alive = True
        
        # Game Feel: buffers de pulo
        self.coyote_timer = 0
        self.jump_buffer = 0
        
        # Game Feel: deformação (squash and stretch)
        self.scale_x = 1.0
        self.scale_y = 1.0
        
        # Partículas de morte
        self.death_particles = []

    def kill(self):
        if self.alive:
            self.alive = False
            # Cria estilhaços cômicos estilo Level Devil
            for _ in range(16):
                px = self.rect.x + random.randint(0, self.rect.width)
                py = self.rect.y + random.randint(0, self.rect.height)
                self.death_particles.append(DeathParticle(px, py))

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.vel_x = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = PLAYER_SPEED

        # Registra intenção de pulo no buffer
        if keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]:
            self.jump_buffer = JUMP_BUFFER_TIME

    def update(self, platforms):
        if not self.alive:
            for p in self.death_particles:
                p.update()
            return

        self.handle_input()

        # Atualiza contadores de tolerância
        if self.on_ground:
            self.coyote_timer = COYOTE_TIME
        else:
            if self.coyote_timer > 0:
                self.coyote_timer -= 1

        if self.jump_buffer > 0:
            self.jump_buffer -= 1

        # Executa pulo com tolerância
        if self.jump_buffer > 0 and self.coyote_timer > 0:
            self.vel_y = JUMP_FORCE
            self.coyote_timer = 0
            self.jump_buffer = 0
            self.on_ground = False
            # Estica verticalmente no pulo
            self.scale_x = 0.75
            self.scale_y = 1.3

        # Movimento Horizontal
        self.rect.x += self.vel_x
        for plat in platforms:
            if plat["solid"] and self.rect.colliderect(plat["rect"]):
                if self.vel_x > 0:
                    self.rect.right = plat["rect"].left
                elif self.vel_x < 0:
                    self.rect.left = plat["rect"].right

        # Movimento Vertical
        self.vel_y += GRAVITY
        self.rect.y += int(self.vel_y)
        was_on_ground = self.on_ground
        self.on_ground = False

        for plat in platforms:
            if plat["solid"] and self.rect.colliderect(plat["rect"]):
                if self.vel_y > 0:
                    self.rect.bottom = plat["rect"].top
                    self.vel_y = 0
                    self.on_ground = True
                    # Achata ao aterrissar com impacto
                    if not was_on_ground:
                        self.scale_x = 1.35
                        self.scale_y = 0.7
                elif self.vel_y < 0:
                    self.rect.top = plat["rect"].bottom
                    self.vel_y = 0

        # Recuperação elástica da deformação
        self.scale_x += (1.0 - self.scale_x) * 0.2
        self.scale_y += (1.0 - self.scale_y) * 0.2

        if self.rect.top > HEIGHT + 40:
            self.kill()

    def draw(self, surface):
        if not self.alive:
            for p in self.death_particles:
                p.draw(surface)
            return

        # Render com Squash & Stretch a partir da base do personagem
        draw_w = int(self.rect.width * self.scale_x)
        draw_h = int(self.rect.height * self.scale_y)
        draw_x = self.rect.centerx - draw_w // 2
        draw_y = self.rect.bottom - draw_h

        draw_rect = pygame.Rect(draw_x, draw_y, draw_w, draw_h)
        pygame.draw.rect(surface, PLAYER_COLOR, draw_rect, border_radius=6)

        # Sombra na base do corpo
        sombra = pygame.Rect(draw_x + 2, draw_rect.bottom - 5, max(1, draw_w - 4), 4)
        pygame.draw.rect(surface, (15, 15, 15), sombra, border_radius=2)

        # Olhos expressivos
        olho_w, olho_h = 6, 8
        desloc_x = 3 if self.vel_x > 0 else (-3 if self.vel_x < 0 else 0)
        desloc_y = -2 if self.vel_y < -2 else (2 if self.vel_y > 2 else 0)

        olho_esq = pygame.Rect(draw_rect.x + 6 + desloc_x, draw_rect.y + 7 + desloc_y, olho_w, olho_h)
        olho_dir = pygame.Rect(draw_rect.x + 18 + desloc_x, draw_rect.y + 7 + desloc_y, olho_w, olho_h)
        pygame.draw.rect(surface, WHITE, olho_esq, border_radius=2)
        pygame.draw.rect(surface, WHITE, olho_dir, border_radius=2)

        pupila_dir_x = 1 if self.vel_x >= 0 else -1
        pup_esq = pygame.Rect(olho_esq.x + 1 + pupila_dir_x, olho_esq.y + 2, 3, 4)
        pup_dir = pygame.Rect(olho_dir.x + 1 + pupila_dir_x, olho_dir.y + 2, 3, 4)
        pygame.draw.rect(surface, PLAYER_COLOR, pup_esq)
        pygame.draw.rect(surface, PLAYER_COLOR, pup_dir)