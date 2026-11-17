# level.py
import pygame
from settings import *


class Level1:
    def __init__(self):
        self.title = "Fase 1: O Desconto sem Nota"
        self.reset()

    def reset(self):
        self.spawn_pos = (40, 460)
        self.nota_fiscal_emitida = False
        self.trap1_triggered = False
        self.trap2_triggered = False
        self.death_message = ""
        self.win_message = "Fase Concluída! O tributo virou infraestrutura pública."
        self.won = False

        self.edu_card = {
            "title": "POR QUE PEDIR A NOTA FISCAL?",
            "points": [
                "• Direito do Consumidor: garante troca e assistência do produto.",
                "• Combate à Sonegação: evita que o imposto pago fique retido.",
                "• Retorno à Sociedade: financia saúde, educação e obras públicas."
            ]
        }

        self.platforms = [
            # --- ANDAR INFERIOR ---
            {"id": "floor_left", "rect": pygame.Rect(0, 520, 260, 80), "solid": True, "falling": False, "color": WALL_COLOR},
            {"id": "step_mid", "rect": pygame.Rect(330, 490, 120, 20), "solid": True, "falling": False, "color": WALL_COLOR},
            {"id": "floor_right", "rect": pygame.Rect(520, 460, 280, 140), "solid": True, "falling": False, "color": WALL_COLOR},

            # Degraus de subida para o 2º andar (lado direito)
            {"id": "climb1", "rect": pygame.Rect(680, 380, 100, 18), "solid": True, "falling": False, "color": WALL_COLOR},
            {"id": "climb2", "rect": pygame.Rect(550, 300, 100, 18), "solid": True, "falling": False, "color": WALL_COLOR},

            # --- ANDAR SUPERIOR ---
            # Plataforma esquerda onde fica o item NF
            {"id": "upper_left", "rect": pygame.Rect(0, 230, 230, 24), "solid": True, "falling": False, "color": WALL_COLOR},
            # Ponte Dupla (Armadilhas se não tiver NF!)
            {"id": "bridge1", "rect": pygame.Rect(230, 230, 160, 24), "solid": True, "falling": False, "color": WALL_COLOR},
            {"id": "bridge2", "rect": pygame.Rect(390, 230, 160, 24), "solid": True, "falling": False, "color": WALL_COLOR},
            # Plataforma da porta final no topo direito
            {"id": "upper_goal", "rect": pygame.Rect(630, 190, 170, 24), "solid": True, "falling": False, "color": WALL_COLOR},
        ]

        # Espinhos no abismo inferior
        self.spikes = [
            pygame.Rect(260, 575, 260, 25)
        ]

        # Nota Fiscal fica no canto superior esquerdo (obriga o jogador a subir e buscar)
        self.nf_item = pygame.Rect(45, 170, 36, 36)

        # Dois gatilhos sequenciais na ponte superior
        self.trigger1 = pygame.Rect(260, 180, 50, 50)
        self.trigger2 = pygame.Rect(420, 180, 50, 50)

        # Porta final no topo direito
        self.goal = pygame.Rect(720, 120, 40, 70)

    def get_hud_info(self):
        if self.nota_fiscal_emitida:
            return f"{self.title} | Nota Fiscal: EMITIDA (Ponte Segura)", GOAL_COLOR
        return f"{self.title} | Nota Fiscal: NÃO EMITIDA (Busque a NF no alto!)", SPIKE_COLOR

    def update(self, player):
        if not player.alive or self.won:
            return

        if not self.nota_fiscal_emitida and player.rect.colliderect(self.nf_item):
            self.nota_fiscal_emitida = True

        # Gatilho 1 e Gatilho 2 derrubam as duas metades da ponte se não houver NF
        if not self.nota_fiscal_emitida:
            if player.rect.colliderect(self.trigger1) and not self.trap1_triggered:
                self.trap1_triggered = True
                for plat in self.platforms:
                    if plat["id"] == "bridge1":
                        plat["solid"] = False
                        plat["falling"] = True

            if player.rect.colliderect(self.trigger2) and not self.trap2_triggered:
                self.trap2_triggered = True
                for plat in self.platforms:
                    if plat["id"] == "bridge2":
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
                self.death_message = "Sem Nota Fiscal, a ponte superior desabou por falta de verba!"
            else:
                self.death_message = "Cuidado com os saltos entre os andares!"

        if player.rect.colliderect(self.goal):
            self.won = True

    def draw(self, surface, font):
        for plat in self.platforms:
            pygame.draw.rect(surface, plat["color"], plat["rect"], border_radius=3)

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
        self.spawn_pos = (40, 480)
        self.transparencia_ativada = False
        self.death_message = ""
        self.win_message = "Boa! O controle social revelou todas as obras fantasmas."
        self.won = False

        self.edu_card = {
            "title": "O QUE É CONTROLE SOCIAL?",
            "points": [
                "• Portal da Transparência: permite consultar gastos públicos.",
                "• Fiscalização Cidadã: ajuda a identificar obras fantasmas.",
                "• Cidadania Ativa: o tributo só vira benefício quando fiscalizado."
            ]
        }

        self.platforms = [
            # Base inferior esquerda
            {"id": "start", "rect": pygame.Rect(0, 530, 240, 70), "solid": True, "falling": False, "color": WALL_COLOR},

            # Isca inferior (parece uma ponte direta à direita, mas a segunda metade é FALSA!)
            {"id": "bait_real", "rect": pygame.Rect(300, 510, 120, 20), "solid": True, "falling": False, "color": WALL_COLOR},
            {"id": "fake_low", "rect": pygame.Rect(470, 490, 140, 20), "solid": False, "falling": False, "color": WALL_COLOR},

            # Caminho de subida pela esquerda até o Portal da Transparência
            {"id": "left_step1", "rect": pygame.Rect(40, 430, 110, 18), "solid": True, "falling": False, "color": WALL_COLOR},
            {"id": "left_step2", "rect": pygame.Rect(180, 340, 110, 18), "solid": True, "falling": False, "color": WALL_COLOR},
            {"id": "top_left", "rect": pygame.Rect(20, 240, 150, 22), "solid": True, "falling": False, "color": WALL_COLOR},

            # Degraus superiores falsos (obras desviadas)
            {"id": "fake_high1", "rect": pygame.Rect(260, 210, 110, 20), "solid": False, "falling": False, "color": WALL_COLOR},
            {"id": "fake_high2", "rect": pygame.Rect(450, 180, 110, 20), "solid": False, "falling": False, "color": WALL_COLOR},

            # Caminho verdadeiro no topo (aparece em verde ao ativar o GOV)
            {"id": "real_high1", "rect": pygame.Rect(240, 270, 130, 20), "solid": False, "falling": False, "color": BG_COLOR},
            {"id": "real_high2", "rect": pygame.Rect(430, 240, 140, 20), "solid": False, "falling": False, "color": BG_COLOR},

            # Plataforma final no topo direito
            {"id": "end", "rect": pygame.Rect(630, 200, 170, 400), "solid": True, "falling": False, "color": WALL_COLOR},
        ]

        # Espinhos cobrindo todo o fosso inferior
        self.spikes = [
            pygame.Rect(240, 575, 390, 25)
        ]

        # Totem de Fiscalização no topo esquerdo
        self.audit_item = pygame.Rect(55, 185, 44, 36)

        # Porta final
        self.goal = pygame.Rect(720, 130, 40, 70)

    def get_hud_info(self):
        if self.transparencia_ativada:
            return f"{self.title} | Transparência: ATIVA (Obras falsas reveladas!)", TRANSPARENCY_COLOR
        return f"{self.title} | Transparência: INATIVA (Suba e ative o GOV!)", SPIKE_COLOR

    def update(self, player):
        if not player.alive or self.won:
            return

        if not self.transparencia_ativada and player.rect.colliderect(self.audit_item):
            self.transparencia_ativada = True
            for plat in self.platforms:
                if plat["id"] in ("fake_low", "fake_high1", "fake_high2"):
                    plat["color"] = FAKE_WALL_COLOR
                elif plat["id"] in ("real_high1", "real_high2"):
                    plat["solid"] = True
                    plat["color"] = REAL_WALL_COLOR

        for spike in self.spikes:
            if player.rect.colliderect(spike):
                player.alive = False

        if not player.alive:
            if not self.transparencia_ativada:
                self.death_message = "Obra fantasma! Escale pela esquerda e ative o portal GOV."
            else:
                self.death_message = "Siga pelas plataformas verdes fiscalizadas até o topo!"

        if player.rect.colliderect(self.goal):
            self.won = True

    def draw(self, surface, font):
        for plat in self.platforms:
            if plat["id"] in ("real_high1", "real_high2") and not self.transparencia_ativada:
                continue
            pygame.draw.rect(surface, plat["color"], plat["rect"], border_radius=3)

        for spike in self.spikes:
            for x in range(spike.left, spike.right, 20):
                points = [(x, spike.bottom), (x + 10, spike.top), (x + 20, spike.bottom)]
                pygame.draw.polygon(surface, SPIKE_COLOR, points)

        pygame.draw.rect(surface, GOAL_COLOR, self.goal, border_radius=4)

        if not self.transparencia_ativada:
            pygame.draw.rect(surface, TRANSPARENCY_COLOR, self.audit_item, border_radius=4)
            label = font.render("GOV", True, WHITE)
            surface.blit(label, label.get_rect(center=self.audit_item.center))


class Level3:
    def __init__(self):
        self.title = "Fase 3: O Buraco no Orçamento"
        self.reset()

    def reset(self):
        self.spawn_pos = (40, 480)
        self.coins_collected = 0
        self.total_coins = 5
        self.orcamento_aprovado = False
        self.trap_triggered = False
        self.death_message = ""
        self.win_message = "Orçamento completo! Os serviços públicos chegaram à população."
        self.won = False

        self.edu_card = {
            "title": "COMO FUNCIONA O ORÇAMENTO PÚBLICO?",
            "points": [
                "• Recursos Limitados: O Estado só investe o que consegue arrecadar.",
                "• Prioridades Sociais: Saúde, educação e transporte disputam verbas.",
                "• Impacto Coletivo: Sem arrecadação justa, serviços essenciais param."
            ]
        }

        self.platforms = [
            # Base inferior onde fica a Urna
            {"id": "start", "rect": pygame.Rect(0, 530, 410, 70), "solid": True, "falling": False, "color": WALL_COLOR},

            # Circuito aéreo para coletar as 5 moedas de tributo
            {"id": "step_a", "rect": pygame.Rect(80, 420, 110, 18), "solid": True, "falling": False, "color": WALL_COLOR},
            {"id": "step_b", "rect": pygame.Rect(240, 340, 110, 18), "solid": True, "falling": False, "color": WALL_COLOR},
            {"id": "step_c", "rect": pygame.Rect(70, 250, 120, 18), "solid": True, "falling": False, "color": WALL_COLOR},
            {"id": "step_d", "rect": pygame.Rect(260, 190, 120, 18), "solid": True, "falling": False, "color": WALL_COLOR},

            # Plataforma 1 do abismo (foge para a direita se pular sem depositar na urna!)
            {"id": "public_service1", "rect": pygame.Rect(450, 480, 95, 22), "solid": True, "falling": False, "color": WALL_COLOR},
            # Plataforma 2 do abismo (degrau final até a porta)
            {"id": "public_service2", "rect": pygame.Rect(580, 410, 90, 22), "solid": True, "falling": False, "color": WALL_COLOR},

            # Plataforma final
            {"id": "end", "rect": pygame.Rect(700, 350, 100, 250), "solid": True, "falling": False, "color": WALL_COLOR},
        ]

        # Espinhos no abismo
        self.spikes = [
            pygame.Rect(410, 575, 290, 25)
        ]

        # 5 Moedas de Tributo espalhadas pelo circuito
        self.coins = [
            pygame.Rect(125, 385, 22, 22),  # Moeda 1
            pygame.Rect(285, 305, 22, 22),  # Moeda 2
            pygame.Rect(115, 215, 22, 22),  # Moeda 3
            pygame.Rect(310, 155, 22, 22),  # Moeda 4 (topo)
            pygame.Rect(220, 485, 22, 22),  # Moeda 5 (chão)
        ]

        # Urna de Arrecadação na beira do abismo
        self.urn = pygame.Rect(345, 480, 44, 50)

        # Gatilho invisível no salto
        self.trigger_zone = pygame.Rect(405, 380, 55, 150)

        # Porta final
        self.goal = pygame.Rect(730, 280, 40, 70)

    def get_hud_info(self):
        if self.orcamento_aprovado:
            return f"{self.title} | Orçamento: APROVADO (100%)", REAL_WALL_COLOR
        return f"{self.title} | Tributos: {self.coins_collected}/{self.total_coins} (Deposite na Urna)", COIN_COLOR

    def update(self, player):
        if not player.alive or self.won:
            return

        for coin in self.coins[:]:
            if player.rect.colliderect(coin):
                self.coins.remove(coin)
                self.coins_collected += 1

        if not self.orcamento_aprovado and player.rect.colliderect(self.urn):
            if self.coins_collected == self.total_coins:
                self.orcamento_aprovado = True
                for plat in self.platforms:
                    if plat["id"] in ("public_service1", "public_service2"):
                        plat["color"] = REAL_WALL_COLOR

        if player.rect.colliderect(self.trigger_zone) and not self.orcamento_aprovado:
            self.trap_triggered = True

        # Se pular sem orçamento, as duas pontes recuam para dentro da parede final
        if self.trap_triggered and not self.orcamento_aprovado:
            for plat in self.platforms:
                if plat["id"] in ("public_service1", "public_service2") and plat["rect"].x < 710:
                    plat["rect"].x += 15

        for spike in self.spikes:
            if player.rect.colliderect(spike):
                player.alive = False

        if not player.alive:
            if self.coins_collected < self.total_coins:
                self.death_message = "Orçamento incompleto! Colete os 5 tributos e deposite na urna."
            elif not self.orcamento_aprovado:
                self.death_message = "Encoste na Urna azul para liberar a verba das pontes!"
            else:
                self.death_message = "Cuidado com o salto duplo sobre o abismo!"

        if player.rect.colliderect(self.goal):
            self.won = True

    def draw(self, surface, font):
        for plat in self.platforms:
            pygame.draw.rect(surface, plat["color"], plat["rect"], border_radius=3)

        for spike in self.spikes:
            for x in range(spike.left, spike.right, 20):
                points = [(x, spike.bottom), (x + 10, spike.top), (x + 20, spike.bottom)]
                pygame.draw.polygon(surface, SPIKE_COLOR, points)

        for coin in self.coins:
            pygame.draw.ellipse(surface, COIN_COLOR, coin)
            lbl = font.render("$", True, TEXT_BG)
            surface.blit(lbl, lbl.get_rect(center=coin.center))

        urn_col = REAL_WALL_COLOR if self.orcamento_aprovado else URN_COLOR
        pygame.draw.rect(surface, urn_col, self.urn, border_radius=4)
        urn_lbl = font.render("R$", True, WHITE)
        surface.blit(urn_lbl, urn_lbl.get_rect(center=self.urn.center))

        pygame.draw.rect(surface, GOAL_COLOR, self.goal, border_radius=4)