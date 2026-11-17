# level.py
import pygame
from settings import *

class Level1:
    def __init__(self):
        self.title = "Fase 1: O Desconto sem Nota"
        self.reset()

    def reset(self):
        self.spawn_pos = (60, 400)
        self.nota_fiscal_emitida = False
        self.trap_triggered = False
        self.death_message = ""
        self.win_message = "Fase Concluída! O tributo virou infraestrutura pública."
        self.edu_card = {
            "title": "Por que pedir Nota Fiscal?",
            "points": [
                "Direito do consumidor: garante troca e assistência do produto",
                "Combate a sonegação: Evita que o imposto pago fique retido",
                "Retorno à Sociedade: Financia saúde, educação e obras públicas"
            ]
        }
        self.won = False

        self.platforms = [
            {"id": "start", "rect": pygame.Rect(0, 460, 280, 140), "solid": True, "falling": False, "color": WALL_COLOR},
            {"id": "bridge", "rect": pygame.Rect(280, 460, 220, 30), "solid": True, "falling": False, "color": WALL_COLOR},
            {"id": "end", "rect": pygame.Rect(500, 460, 300, 140), "solid": True, "falling": False, "color": WALL_COLOR},
        ]

        self.spikes = [pygame.Rect(280, 575, 220, 25)]
        self.nf_item = pygame.Rect(180, 400, 36, 36)
        self.trigger_zone = pygame.Rect(340, 410, 60, 50)
        self.goal = pygame.Rect(710, 390, 40, 70)

    def get_hud_info(self):
        if self.nota_fiscal_emitida:
            return f"{self.title} | Nota Fiscal: EMITIDA (Ponte Segura)", GOAL_COLOR
        return f"{self.title} | Nota Fiscal: NÃO EMITIDA (Cuidado!)", SPIKE_COLOR

    def update(self, player):
        if not player.alive or self.won:
            return

        if not self.nota_fiscal_emitida and player.rect.colliderect(self.nf_item):
            self.nota_fiscal_emitida = True

        if player.rect.colliderect(self.trigger_zone) and not self.nota_fiscal_emitida:
            if not self.trap_triggered:
                self.trap_triggered = True
                for plat in self.platforms:
                    if plat["id"] == "bridge":
                        plat["solid"] = False
                        plat["falling"] = True

        for plat in self.platforms:
            if plat["falling"]:
                plat["rect"].y += 12

        for spike in self.spikes:
            if player.rect.colliderect(spike):
                player.alive = False

        if not player.alive:
            if not self.nota_fiscal_emitida:
                self.death_message = "Sem Nota Fiscal, faltou verba para manter a ponte!"
            else:
                self.death_message = "Cuidado com o abismo!"

        if player.rect.colliderect(self.goal):
            self.won = True

    def draw(self, surface, font):
        for plat in self.platforms:
            pygame.draw.rect(surface, plat["color"], plat["rect"])

        for spike in self.spikes:
            for x in range(spike.left, spike.right, 20):
                points = [(x, spike.bottom), (x + 10, spike.top), (x + 20, spike.bottom)]
                pygame.draw.polygon(surface, SPIKE_COLOR, points)

        pygame.draw.rect(surface, GOAL_COLOR, self.goal, border_radius=4)

        if not self.nota_fiscal_emitida:
            pygame.draw.rect(surface, NF_COLOR, self.nf_item, border_radius=4)
            label = font.render("NF", True, WHITE)
            surface.blit(label, label.get_rect(center=self.nf_item.center))


class Level2:
    def __init__(self):
        self.title = "Fase 2: Obra Fantasma"
        self.reset()

    def reset(self):
        self.spawn_pos = (50, 420)
        self.transparencia_ativada = False
        self.death_message = ""
        self.win_message = "Boa! O controle social revelou a obra fantasma."
        self.edu_card = {
            "title": "O QUE É CONTROLE SOCIAL?",
            "points": [
                "Portal da Transparência: permite consultar gastos públicos.",
                "Fiscalização Cidadã: ajuda a identificar obras fantasmas.",
                "Cidadania Ativa: o tributo só vira benefício quando fiscalizado."
            ]
        }
        self.won = False

        self.platforms = [
            # Chão inicial e final
            {"id": "start", "rect": pygame.Rect(0, 480, 220, 120), "solid": True, "falling": False, "color": WALL_COLOR},
            {"id": "end", "rect": pygame.Rect(620, 300, 180, 300), "solid": True, "falling": False, "color": WALL_COLOR},

            # Degrau 1 (Sólido normal)
            {"id": "step1", "rect": pygame.Rect(260, 420, 90, 22), "solid": True, "falling": False, "color": WALL_COLOR},

            # Degrau 2 e 3 (ARMADILHA LEVEL DEVIL: parecem normais, mas não têm colisão!)
            {"id": "fake1", "rect": pygame.Rect(390, 360, 90, 22), "solid": False, "falling": False, "color": WALL_COLOR},
            {"id": "fake2", "rect": pygame.Rect(510, 300, 80, 22), "solid": False, "falling": False, "color": WALL_COLOR},

            # Caminho verdadeiro (invisível até ativar o Portal da Transparência)
            {"id": "real_bridge", "rect": pygame.Rect(380, 385, 210, 22), "solid": False, "falling": False, "color": BG_COLOR},
        ]

        # Espinhos cobrindo todo o abismo
        self.spikes = [pygame.Rect(220, 575, 400, 25)]

        # Totem de Fiscalização / Portal da Transparência (fica na plataforma inicial à esquerda)
        self.audit_item = pygame.Rect(45, 340, 42, 36)

        # Porta de saída no alto à direita
        self.goal = pygame.Rect(720, 230, 40, 70)

    def get_hud_info(self):
        if self.transparencia_ativada:
            return f"{self.title} | Transparência: ATIVA (Obras falsas reveladas!)", TRANSPARENCY_COLOR
        return f"{self.title} | Transparência: INATIVA (Cuidado com desvios!)", SPIKE_COLOR

    def update(self, player):
        if not player.alive or self.won:
            return

        # 1. Jogador encosta no totem de Transparência / Controle Social
        if not self.transparencia_ativada and player.rect.colliderect(self.audit_item):
            self.transparencia_ativada = True
            for plat in self.platforms:
                if plat["id"] in ("fake1", "fake2"):
                    plat["color"] = FAKE_WALL_COLOR  # Revela que são falsas
                elif plat["id"] == "real_bridge":
                    plat["solid"] = True             # Ativa a ponte verdadeira
                    plat["color"] = REAL_WALL_COLOR

        # 2. Verificação de Morte
        for spike in self.spikes:
            if player.rect.colliderect(spike):
                player.alive = False

        if not player.alive:
            if not self.transparencia_ativada:
                self.death_message = "Obra fantasma! Você caiu num desvio de verba."
            else:
                self.death_message = "Use a ponte verde fiscalizada para atravessar!"

        # 3. Condição de Vitória
        if player.rect.colliderect(self.goal):
            self.won = True

    def draw(self, surface, font):
        for plat in self.platforms:
            # Não desenha a ponte verdadeira enquanto estiver oculta
            if plat["id"] == "real_bridge" and not self.transparencia_ativada:
                continue
            pygame.draw.rect(surface, plat["color"], plat["rect"], border_radius=3)

        # Espinhos
        for spike in self.spikes:
            for x in range(spike.left, spike.right, 20):
                points = [(x, spike.bottom), (x + 10, spike.top), (x + 20, spike.bottom)]
                pygame.draw.polygon(surface, SPIKE_COLOR, points)

        # Porta final
        pygame.draw.rect(surface, GOAL_COLOR, self.goal, border_radius=4)

        # Item Portal da Transparência ("PT" ou "GOV")
        if not self.transparencia_ativada:
            pygame.draw.rect(surface, TRANSPARENCY_COLOR, self.audit_item, border_radius=4)
            label = font.render("GOV", True, WHITE)
            surface.blit(label, label.get_rect(center=self.audit_item.center))