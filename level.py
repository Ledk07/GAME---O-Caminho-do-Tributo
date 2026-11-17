# level.py
import pygame
from settings import *

class Level1:
    def __init__(self):
        self.reset()

    def reset(self):
        self.spawn_pos = (60, 400)
        self.nota_fiscal_emitida = False
        self.trap_triggered = False
        self.death_message = ""
        self.won = False

        # Plataformas: dicionários permitem alterar propriedades em tempo real (armadilhas)
        self.platforms = [
            # Chão inicial
            {"id": "start", "rect": pygame.Rect(0, 460, 280, 140), "solid": True, "falling": False},
            # A PONTE (alvo da armadilha se sonegar!)
            {"id": "bridge", "rect": pygame.Rect(280, 460, 220, 30), "solid": True, "falling": False},
            # Chão final
            {"id": "end", "rect": pygame.Rect(500, 460, 300, 140), "solid": True, "falling": False},
        ]

        # Espinhos no fundo do abismo
        self.spikes = [
            pygame.Rect(280, 575, 220, 25)
        ]

        # Item de escolha fiscal: Pegar a Nota Fiscal
        self.nf_item = pygame.Rect(180, 400, 28, 36)

        # Gatilho invisível no meio da ponte (Estilo Level Devil)
        self.trigger_zone = pygame.Rect(340, 410, 60, 50)

        # Porta de saída da fase
        self.goal = pygame.Rect(710, 390, 40, 70)

    def update(self, player):
        if not player.alive or self.won:
            return

        # 1. Coleta da Nota Fiscal (Ação de Cidadania Fiscal)
        if not self.nota_fiscal_emitida and player.rect.colliderect(self.nf_item):
            self.nota_fiscal_emitida = True

        # 2. Gatilho da Armadilha (Consequência da Sonegação)
        if player.rect.colliderect(self.trigger_zone) and not self.nota_fiscal_emitida:
            if not self.trap_triggered:
                self.trap_triggered = True
                for plat in self.platforms:
                    if plat["id"] == "bridge":
                        plat["solid"] = False
                        plat["falling"] = True

        # Animação da ponte desabando
        for plat in self.platforms:
            if plat["falling"]:
                plat["rect"].y += 12

        # 3. Verificação de Morte (Espinhos ou Queda)
        for spike in self.spikes:
            if player.rect.colliderect(spike):
                player.alive = False

        if not player.alive:
            if not self.nota_fiscal_emitida:
                self.death_message = "Sem Nota Fiscal, faltou verba para manter a ponte! (Pressione R)"
            else:
                self.death_message = "Cuidado com o abismo! (Pressione R)"

        # 4. Condição de Vitória
        if player.rect.colliderect(self.goal):
            self.won = True

    def draw(self, surface, font):
        # Plataformas
        for plat in self.platforms:
            pygame.draw.rect(surface, WALL_COLOR, plat["rect"])

        # Espinhos (triângulos simples)
        for spike in self.spikes:
            for x in range(spike.left, spike.right, 20):
                points = [(x, spike.bottom), (x + 10, spike.top), (x + 20, spike.bottom)]
                pygame.draw.polygon(surface, SPIKE_COLOR, points)

        # Porta final
        pygame.draw.rect(surface, GOAL_COLOR, self.goal, border_radius=4)

        # Item Nota Fiscal (se ainda não foi pego)
        if not self.nota_fiscal_emitida:
            pygame.draw.rect(surface, NF_COLOR, self.nf_item, border_radius=3)
            label = font.render("NF", True, WHITE)
            surface.blit(label, (self.nf_item.x + 4, self.nf_item.y + 8))