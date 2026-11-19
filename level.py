# level.py
import pygame
import math
from settings import *

class BaseLevel:
    """Classe base que gerencia comportamentos e renderizações comuns."""
    def __init__(self):
        self.won = False
        self.platforms = []
        self.spikes = []
        self.goal = pygame.Rect(0, 0, 40, 70)
        self.spawn_pos = (40, 460)
        self.death_message = ""
        self.edu_card = {}
        self.shake_intensity = 0
        
        # Fontes internas de placas e avisos do cenário
        self.font_sign = pygame.font.SysFont("arial", 12, bold=True)
        self.font_plate = pygame.font.SysFont("arial", 14, bold=True)

    def check_hazards(self, player):
        for spike in self.spikes:
            if player.rect.colliderect(spike):
                player.kill()
                self.shake_intensity = 8

        if player.alive and player.rect.colliderect(self.goal):
            self.won = True

    def draw_common(self, surface):
        # Plataformas
        for plat in self.platforms:
            if plat.get("visible", True):
                pygame.draw.rect(surface, plat["color"], plat["rect"], border_radius=4)

        # Espinhos
        for spike in self.spikes:
            for x in range(spike.left, spike.right, 20):
                pts = [(x, spike.bottom), (x + 10, spike.top), (x + 20, spike.bottom)]
                pygame.draw.polygon(surface, SPIKE_COLOR, pts)

        # Porta Final de Cidadania
        pygame.draw.rect(surface, GOAL_COLOR, self.goal, border_radius=6)
        pygame.draw.circle(surface, WHITE, (self.goal.right - 8, self.goal.centery), 3)


# ==========================================================
# FASE 1: O DILEMA DA NOTA FISCAL
# ==========================================================
class Level1(BaseLevel):
    def __init__(self):
        super().__init__()
        self.title = "Fase 1: O Dilema da Nota Fiscal"
        self.reset()

    def reset(self):
        super().__init__()
        self.spawn_pos = (35, 470)
        self.nota_fiscal_emitida = False
        self.trap_pit_triggered = False

        self.edu_card = {
            "title": "POR QUE EXIGIR NOTA FISCAL?",
            "points": [
                "• Armadilha do Desconto: Sem nota, o imposto fica no bolso do mau comerciante.",
                "• Garantia do Consumidor: Sem documento fiscal, você perde o direito de troca.",
                "• Retorno Coletivo: Cada nota emitida financia escolas, asfalto e postos de saúde."
            ]
        }

        self.platforms = [
            # Chão Inicial
            {"id": "start_floor", "rect": pygame.Rect(0, 520, 180, 80), "solid": True, "color": WALL_COLOR},
            
            # CAMINHO DA TENTAÇÃO (Desconto sem Nota - Ponte Falsa que desaba)
            {"id": "trap_bridge", "rect": pygame.Rect(180, 520, 240, 24), "solid": True, "falling": False, "color": WALL_COLOR},
            {"id": "trap_floor_end", "rect": pygame.Rect(420, 520, 100, 80), "solid": True, "color": WALL_COLOR},

            # CAMINHO LEGAL (Subida pelos balcões comerciais)
            {"id": "shop_step1", "rect": pygame.Rect(70, 420, 100, 18), "solid": True, "color": WALL_COLOR},
            {"id": "shop_step2", "rect": pygame.Rect(180, 340, 110, 18), "solid": True, "color": WALL_COLOR},
            {"id": "shop_counter", "rect": pygame.Rect(50, 250, 150, 22), "solid": True, "color": WALL_COLOR},

            # PASSARELA PÚBLICA (Só surge com a NF emitida)
            {"id": "bridge1", "rect": pygame.Rect(230, 240, 170, 22), "solid": False, "visible": False, "color": REAL_WALL_COLOR},
            {"id": "bridge2", "rect": pygame.Rect(420, 240, 170, 22), "solid": False, "visible": False, "color": REAL_WALL_COLOR},

            # Destino no topo direito
            {"id": "goal_floor", "rect": pygame.Rect(620, 200, 180, 400), "solid": True, "color": WALL_COLOR},
        ]

        self.spikes = [
            pygame.Rect(180, 575, 440, 25)
        ]

        # Item Nota Fiscal no balcão legal
        self.nf_base_y = 195
        self.nf_item = pygame.Rect(95, self.nf_base_y, 44, 38)
        
        # Gatilho da tentação
        self.trigger_trap = pygame.Rect(210, 480, 60, 50)
        self.goal = pygame.Rect(710, 130, 40, 70)

    def get_hud_info(self):
        if self.nota_fiscal_emitida:
            return "Fase 1: Nota Fiscal | NF Emitida! Passarela construída", GOAL_COLOR
        if self.trap_pit_triggered:
            return "Fase 1: Nota Fiscal | Asfalto ruiu! Suba e exija a NF no caixa", SPIKE_COLOR
        return "Fase 1: Nota Fiscal | Atalho sem nota ou Comércio Legal?", COIN_COLOR

    def update(self, player):
        self.nf_item.y = int(self.nf_base_y + math.sin(pygame.time.get_ticks() * 0.005) * 4)

        if not player.alive or self.won:
            return

        # Coleta da NF
        if not self.nota_fiscal_emitida and player.rect.colliderect(self.nf_item):
            self.nota_fiscal_emitida = True
            self.shake_intensity = 5
            for plat in self.platforms:
                if plat["id"] in ("bridge1", "bridge2"):
                    plat["solid"] = True
                    plat["visible"] = True

        # Armadilha de quem pega o atalho sem nota
        if not self.nota_fiscal_emitida and player.rect.colliderect(self.trigger_trap):
            self.trap_pit_triggered = True
            self.shake_intensity = 7
            for plat in self.platforms:
                if plat["id"] == "trap_bridge":
                    plat["falling"] = True
                    plat["solid"] = False

        for plat in self.platforms:
            if plat.get("falling", False) and plat["rect"].y < HEIGHT + 60:
                plat["rect"].y += 14

        self.check_hazards(player)
        if not player.alive:
            if self.trap_pit_triggered:
                self.death_message = "Caiu no conto do 'desconto sem nota'! Sem arrecadação, o asfalto cedeu."
            else:
                self.death_message = "Suba pelos degraus da esquerda até o caixa e exija sua NF!"

    def draw(self, surface, font):
        self.draw_common(surface)

        # Placa 1: A tentação do desconto
        if not self.trap_pit_triggered:
            placa_rect = pygame.Rect(185, 485, 140, 24)
            pygame.draw.rect(surface, (230, 80, 80), placa_rect, border_radius=4)
            msg = self.font_sign.render("SEM NOTA: -20% >", True, WHITE)
            surface.blit(msg, msg.get_rect(center=placa_rect.center))

        # Placa 2: Balcão do comércio legal
        placa_balcao = pygame.Rect(55, 290, 140, 22)
        pygame.draw.rect(surface, WALL_COLOR, placa_balcao, border_radius=4)
        msg_balcao = self.font_sign.render("BALCÃO DO COMÉRCIO", True, WHITE)
        surface.blit(msg_balcao, msg_balcao.get_rect(center=placa_balcao.center))

        # Desenho da NF
        if not self.nota_fiscal_emitida:
            pygame.draw.rect(surface, NF_COLOR, self.nf_item, border_radius=6)
            lbl = font.render("NF", True, WHITE)
            surface.blit(lbl, lbl.get_rect(center=self.nf_item.center))


# ==========================================================
# FASE 2: A OBRA FANTASMA E O CANTEIRO DE OBRAS
# ==========================================================
class Level2(BaseLevel):
    def __init__(self):
        super().__init__()
        self.title = "Fase 2: Obra Fantasma e Canteiro"
        self.reset()

    def reset(self):
        super().__init__()
        self.spawn_pos = (35, 480)
        self.transparencia_ativada = False

        self.edu_card = {
            "title": "O QUE É FISCALIZAÇÃO SOCIAL?",
            "points": [
                "• Obra Fantasma: Obra que recebe verba pública, mas nunca sai do papel.",
                "• Portal da Transparência: Ferramenta pública para checar gastos da prefeitura e governo.",
                "• Controle Social: O cidadão tem o direito e o dever de denunciar obras paralisadas."
            ]
        }

        # Plataforma móvel que patrulha após a fiscalização
        self.platform_mover = pygame.Rect(320, 270, 90, 18)
        self.mover_dir = 1
        self.mover_speed = 2.5

        self.platforms = [
            {"id": "start", "rect": pygame.Rect(0, 530, 200, 70), "solid": True, "color": WALL_COLOR},

            # Andaimes de subida até a auditoria
            {"id": "scaffold_1", "rect": pygame.Rect(60, 430, 100, 18), "solid": True, "color": WALL_COLOR},
            {"id": "scaffold_2", "rect": pygame.Rect(180, 350, 100, 18), "solid": True, "color": WALL_COLOR},
            {"id": "scaffold_top", "rect": pygame.Rect(30, 240, 160, 22), "solid": True, "color": WALL_COLOR},

            # Obras Fantasmas no ar (parecem seguras, mas não têm colisão sólida)
            {"id": "fake_1", "rect": pygame.Rect(260, 210, 100, 18), "solid": False, "color": WALL_COLOR},
            {"id": "fake_2", "rect": pygame.Rect(440, 180, 100, 18), "solid": False, "color": WALL_COLOR},

            # Plataforma móvel mecânica (inativa até fiscalizar)
            {"id": "mover", "rect": self.platform_mover, "solid": False, "visible": False, "color": REAL_WALL_COLOR},

            # Apoio do lado direito
            {"id": "step_right", "rect": pygame.Rect(530, 260, 90, 20), "solid": False, "visible": False, "color": REAL_WALL_COLOR},

            # Destino final
            {"id": "end", "rect": pygame.Rect(650, 200, 150, 400), "solid": True, "color": WALL_COLOR},
        ]

        self.spikes = [pygame.Rect(200, 575, 450, 25)]
        self.totem_base_y = 185
        self.audit_item = pygame.Rect(60, self.totem_base_y, 50, 38)
        self.goal = pygame.Rect(720, 130, 40, 70)

    def get_hud_info(self):
        if self.transparencia_ativada:
            return "Fase 2: Obra Fantasma | AUDITADA! Obra retomada e móvel liberado", TRANSPARENCY_COLOR
        return "Fase 2: Obra Fantasma | Obra Parada! Ative o totem GOV para auditar", SPIKE_COLOR

    def update(self, player):
        self.audit_item.y = int(self.totem_base_y + math.sin(pygame.time.get_ticks() * 0.005) * 4)

        # Movimento da plataforma mecânica regularizada
        if self.transparencia_ativada:
            self.platform_mover.x += int(self.mover_speed * self.mover_dir)
            if self.platform_mover.x > 420:
                self.mover_dir = -1
            elif self.platform_mover.x < 240:
                self.mover_dir = 1

        if not player.alive or self.won:
            return

        if not self.transparencia_ativada and player.rect.colliderect(self.audit_item):
            self.transparencia_ativada = True
            self.shake_intensity = 6
            for plat in self.platforms:
                if plat["id"] in ("fake_1", "fake_2"):
                    plat["color"] = FAKE_WALL_COLOR  # Fica vermelho: desvio identificado
                elif plat["id"] == "mover":
                    plat["solid"] = True
                    plat["visible"] = True
                elif plat["id"] == "step_right":
                    plat["solid"] = True
                    plat["visible"] = True

        self.check_hazards(player)
        if not player.alive:
            self.death_message = "Obra fantasma! Ative o Portal GOV para auditar e retomar os trabalhos."

    def draw(self, surface, font):
        self.draw_common(surface)

        # Placa de obra pública no centro da tela
        placa_box = pygame.Rect(260, 460, 280, 55)
        bg_col = (40, 110, 60) if self.transparencia_ativada else (180, 60, 50)
        pygame.draw.rect(surface, bg_col, placa_box, border_radius=6)
        pygame.draw.rect(surface, WHITE, placa_box, width=2, border_radius=6)

        t1 = "REFORMA PÚBLICA: R$ 8.000.000"
        t2 = "STATUS: AUDITADA E ENTREGUE" if self.transparencia_ativada else "STATUS: PARADA (DESVIO SUSPEITO)"
        s1 = self.font_plate.render(t1, True, WHITE)
        s2 = self.font_sign.render(t2, True, WHITE)
        surface.blit(s1, s1.get_rect(center=(placa_box.centerx, placa_box.y + 18)))
        surface.blit(s2, s2.get_rect(center=(placa_box.centerx, placa_box.y + 38)))

        # Totem de Fiscalização
        if not self.transparencia_ativada:
            pygame.draw.rect(surface, TRANSPARENCY_COLOR, self.audit_item, border_radius=6)
            lbl = font.render("GOV", True, WHITE)
            surface.blit(lbl, lbl.get_rect(center=self.audit_item.center))


# ==========================================================
# FASE 3: A BALANÇA DO ORÇAMENTO PÚBLICO
# ==========================================================
class Level3(BaseLevel):
    def __init__(self):
        super().__init__()
        self.title = "Fase 3: A Balança do Orçamento"
        self.reset()

    def reset(self):
        super().__init__()
        self.spawn_pos = (40, 480)
        self.coins_collected = 0
        self.total_coins = 5
        self.orcamento_aprovado = False
        self.trap_triggered = False

        self.edu_card = {
            "title": "COMO FUNCIONA O ORÇAMENTO PÚBLICO?",
            "points": [
                "• Arrecadação Consciente: O poder público só consegue investir se houver receita.",
                "• Prioridades Sociais: Saúde, mobilidade e segurança demandam planejamento e verba.",
                "• Impacto da Sonegação: Sem a contribuição de todos, pontes e serviços essenciais fecham."
            ]
        }

        self.platforms = [
            {"id": "start", "rect": pygame.Rect(0, 530, 360, 70), "solid": True, "color": WALL_COLOR},

            # Circuito vertical para coletar tributos
            {"id": "step_a", "rect": pygame.Rect(70, 440, 120, 18), "solid": True, "color": WALL_COLOR},
            {"id": "step_b", "rect": pygame.Rect(230, 350, 110, 18), "solid": True, "color": WALL_COLOR},
            {"id": "step_c", "rect": pygame.Rect(60, 260, 120, 18), "solid": True, "color": WALL_COLOR},
            {"id": "step_d", "rect": pygame.Rect(220, 180, 130, 18), "solid": True, "color": WALL_COLOR},

            # Pontes de Serviços Públicos (fogem se tentar cruzar sem orçamento)
            {"id": "pub_service1", "rect": pygame.Rect(410, 460, 100, 22), "solid": True, "color": WALL_COLOR},
            {"id": "pub_service2", "rect": pygame.Rect(550, 390, 100, 22), "solid": True, "color": WALL_COLOR},

            {"id": "end", "rect": pygame.Rect(690, 320, 110, 280), "solid": True, "color": WALL_COLOR},
        ]

        self.spikes = [pygame.Rect(360, 575, 330, 25)]

        # Circuito de Moedas
        self.coin_spots = [
            (125, 405), (280, 315), (115, 225), (285, 145), (190, 485)
        ]
        self.coins = [pygame.Rect(x, y, 22, 22) for x, y in self.coin_spots]

        # Urna do Tesouro Público
        self.urn_base_y = 475
        self.urn = pygame.Rect(290, self.urn_base_y, 50, 55)
        self.trigger_void = pygame.Rect(365, 360, 60, 160)
        self.goal = pygame.Rect(730, 250, 40, 70)

    def get_hud_info(self):
        if self.orcamento_aprovado:
            return "Fase 3: Orçamento | 100% ARRECADADO (Infraestrutura Pronta)", REAL_WALL_COLOR
        return f"Fase 3: Orçamento | Tributos: {self.coins_collected}/{self.total_coins} (Deposite na Urna)", COIN_COLOR

    def update(self, player):
        ticks = pygame.time.get_ticks()
        for i, coin in enumerate(self.coins):
            coin.y = int(self.coin_spots[i][1] + math.sin(ticks * 0.006 + i) * 4)

        if not player.alive or self.won:
            return

        for coin in self.coins[:]:
            if player.rect.colliderect(coin):
                self.coins.remove(coin)
                self.coins_collected += 1

        # Depósito dos tributos na Urna
        if not self.orcamento_aprovado and player.rect.colliderect(self.urn):
            if self.coins_collected == self.total_coins:
                self.orcamento_aprovado = True
                self.shake_intensity = 6
                for plat in self.platforms:
                    if plat["id"] in ("pub_service1", "pub_service2"):
                        plat["color"] = REAL_WALL_COLOR

        # Tentativa de cruzar sem orçamento
        if player.rect.colliderect(self.trigger_void) and not self.orcamento_aprovado:
            self.trap_triggered = True

        if self.trap_triggered and not self.orcamento_aprovado:
            for plat in self.platforms:
                if plat["id"] in ("pub_service1", "pub_service2") and plat["rect"].x < 700:
                    plat["rect"].x += 16

        self.check_hazards(player)
        if not player.alive:
            if self.coins_collected < self.total_coins:
                self.death_message = "Cofre público vazio! Colete os 5 tributos para financiar as pontes."
            else:
                self.death_message = "Deposite as moedas na Urna 'R$' antes de tentar cruzar!"

    def draw(self, surface, font):
        self.draw_common(surface)

        for coin in self.coins:
            pygame.draw.ellipse(surface, COIN_COLOR, coin)
            lbl = font.render("$", True, TEXT_BG)
            surface.blit(lbl, lbl.get_rect(center=coin.center))

        # Urna com letreiro
        urn_col = REAL_WALL_COLOR if self.orcamento_aprovado else URN_COLOR
        pygame.draw.rect(surface, urn_col, self.urn, border_radius=6)
        lbl = font.render("R$", True, WHITE)
        surface.blit(lbl, lbl.get_rect(center=self.urn.center))

        placa_urna = pygame.Rect(self.urn.x - 20, self.urn.y - 24, 90, 20)
        pygame.draw.rect(surface, WALL_COLOR, placa_urna, border_radius=3)
        txt = "ORÇAMENTO" if not self.orcamento_aprovado else "APROVADO"
        surface.blit(self.font_sign.render(txt, True, WHITE), self.font_sign.render(txt, True, WHITE).get_rect(center=placa_urna.center))