# main.py
import pygame
import sys
import random
import math
from settings import *
from player import Player
from level import Level1, Level2, Level3

def draw_menu(surface, font_huge, font_title, font_body, font_badge):
    surface.fill(BG_COLOR)

    # 1. Selo Institucional do Projeto de Extensão
    badge_rect = pygame.Rect(0, 0, 480, 28)
    badge_rect.center = (WIDTH // 2, 70)
    pygame.draw.rect(surface, (215, 200, 175), badge_rect, border_radius=14)
    badge_txt = font_badge.render("PROJETO DE EXTENSÃO — NAF UNICHRISTUS & RECEITA FEDERAL", True, WALL_COLOR)
    surface.blit(badge_txt, badge_txt.get_rect(center=badge_rect.center))

    # 2. Título Principal
    title_surf = font_huge.render("O CAMINHO DO TRIBUTO", True, WALL_COLOR)
    surface.blit(title_surf, title_surf.get_rect(center=(WIDTH // 2, 135)))

    sub_surf = font_body.render("Um jogo sobre cidadania fiscal, transparência e retorno social", True, (90, 75, 65))
    surface.blit(sub_surf, sub_surf.get_rect(center=(WIDTH // 2, 175)))

    # 3. Ícone Ilustrativo do Personagem (Centralizado no Menu)
    icon_rect = pygame.Rect(0, 0, 50, 50)
    icon_rect.center = (WIDTH // 2, 235)
    pygame.draw.rect(surface, PLAYER_COLOR, icon_rect, border_radius=10)
    # Olhinhos do boneco
    pygame.draw.rect(surface, WHITE, (icon_rect.x + 10, icon_rect.y + 12, 10, 12), border_radius=3)
    pygame.draw.rect(surface, WHITE, (icon_rect.x + 30, icon_rect.y + 12, 10, 12), border_radius=3)
    pygame.draw.rect(surface, PLAYER_COLOR, (icon_rect.x + 13, icon_rect.y + 15, 5, 6))
    pygame.draw.rect(surface, PLAYER_COLOR, (icon_rect.x + 33, icon_rect.y + 15, 5, 6))

    # 4. Botão Principal com Efeito Pulsante
    pulse = (math.sin(pygame.time.get_ticks() * 0.005) + 1) / 2
    btn_w = int(460 + pulse * 10)  # Aumentado de 360 para 460px
    btn_h = int(50 + pulse * 4)
    btn_rect = pygame.Rect(0, 0, btn_w, btn_h)
    btn_rect.center = (WIDTH // 2, 330)
    btn_color = GOAL_COLOR if pulse > 0.3 else (35, 140, 65)
    pygame.draw.rect(surface, btn_color, btn_rect, border_radius=12)
    
    font_btn = pygame.font.SysFont("arial", 18, bold=True)
    start_txt = font_btn.render("PRESSIONE [ESPAÇO] PARA JOGAR", True, WHITE)
    surface.blit(start_txt, start_txt.get_rect(center=btn_rect.center))

    btn_color = GOAL_COLOR if pulse > 0.3 else (35, 140, 65)
    pygame.draw.rect(surface, btn_color, btn_rect, border_radius=12)
    start_txt = font_title.render("PRESSIONE [ESPAÇO] PARA JOGAR", True, WHITE)
    surface.blit(start_txt, start_txt.get_rect(center=btn_rect.center))

    # 5. Painel de Instruções / Controles
    info_box = pygame.Rect(0, 0, 540, 150)
    info_box.center = (WIDTH // 2, 470)
    pygame.draw.rect(surface, (225, 212, 185), info_box, border_radius=10)
    pygame.draw.rect(surface, WALL_COLOR, info_box, width=2, border_radius=10)

    ctrl_title = font_title.render("COMO JOGAR:", True, WALL_COLOR)
    surface.blit(ctrl_title, (info_box.x + 25, info_box.y + 18))

    instrucoes = [
        "• [A] e [D] ou Setas: Movimentação lateral",
        "• [ESPAÇO] ou [W]: Pular obstáculos",
        "• [R]: Reiniciar a fase instantaneamente ao cair em armadilhas",
        "• [ESC]: Retornar ao Menu Principal a qualquer momento"
    ]
    for i, inst in enumerate(instrucoes):
        t = font_body.render(inst, True, TEXT_BG)
        surface.blit(t, (info_box.x + 25, info_box.y + 52 + i * 22))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("O Caminho do Tributo - Conscientização Fiscal")
    clock = pygame.time.Clock()

    # Fontes pré-carregadas
    font_huge = pygame.font.SysFont("arial", 36, bold=True)
    font_hud = pygame.font.SysFont("arial", 16, bold=True)
    font_title = pygame.font.SysFont("arial", 22, bold=True)
    font_body = pygame.font.SysFont("arial", 15, bold=False)
    font_badge = pygame.font.SysFont("arial", 12, bold=True)

    # Estado de jogo: "MENU" ou "PLAYING"
    game_state = "MENU"

    levels = [Level1(), Level2(), Level3()]
    current_idx = 0
    level = levels[current_idx]
    player = Player(*level.spawn_pos)

    render_surface = pygame.Surface((WIDTH, HEIGHT))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # Se estiver no menu, Espaço ou Enter inicia a partida
                if game_state == "MENU":
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        game_state = "PLAYING"
                        current_idx = 0
                        level = levels[current_idx]
                        level.reset()
                        player = Player(*level.spawn_pos)

                # Se estiver jogando
                elif game_state == "PLAYING":
                    # Tecla ESC volta ao menu
                    if event.key == pygame.K_ESCAPE:
                        game_state = "MENU"

                    # Tecla R reinicia a fase atual
                    if event.key == pygame.K_r:
                        level.reset()
                        player = Player(*level.spawn_pos)

                    # Avançar de fase ao vencer
                    if level.won and event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        if current_idx < len(levels) - 1:
                            current_idx += 1
                            level = levels[current_idx]
                            level.reset()
                            player = Player(*level.spawn_pos)
                        else:
                            # Terminou todas as fases: retorna ao menu
                            game_state = "MENU"

        # RENDERIZAÇÃO CONFORME O ESTADO
        if game_state == "MENU":
            draw_menu(screen, font_huge, font_title, font_body, font_badge)

        elif game_state == "PLAYING":
            # 1. Atualizações lógicas
            player.update(level.platforms)
            level.update(player)

            # 2. Desenho do jogo na superfície temporária
            render_surface.fill(BG_COLOR)
            level.draw(render_surface, font_hud)
            player.draw(render_surface)

            # 3. HUD Superior Dinâmico
            status_text, status_color = level.get_hud_info()
            hud_surf = font_hud.render(status_text, True, status_color)
            render_surface.blit(hud_surf, (20, 20))

            # Instrução sutil do ESC
            esc_box = pygame.Rect(WIDTH - 110, HEIGHT - 32, 95, 22)
            pygame.draw.rect(render_surface, (215, 205, 185), esc_box, border_radius=4)
            esc_txt = font_badge.render("[ESC] MENU", True, WALL_COLOR)
            render_surface.blit(esc_txt, esc_txt.get_rect(center=esc_box.center))

            # 4. Banner de Morte
            if not player.alive:
                overlay = pygame.Surface((WIDTH, 90), pygame.SRCALPHA)
                overlay.fill((20, 20, 20, 210))
                render_surface.blit(overlay, (0, HEIGHT // 2 - 45))

                msg_surf = font_hud.render(level.death_message, True, WHITE)
                render_surface.blit(msg_surf, msg_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 12)))

                sub_surf = font_body.render("Pressione [R] para reiniciar a fase", True, (255, 120, 120))
                render_surface.blit(sub_surf, sub_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 18)))

            # 5. Card Educativo de Vitória
            if level.won:
                dim = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                dim.fill((0, 0, 0, 150))
                render_surface.blit(dim, (0, 0))

                card = pygame.Rect(0, 0, 700, 270)
                card.center = (WIDTH // 2, HEIGHT // 2)
                pygame.draw.rect(render_surface, BG_COLOR, card, border_radius=12)
                pygame.draw.rect(render_surface, GOAL_COLOR, card, width=4, border_radius=12)

                header = pygame.Rect(card.x, card.y, card.width, 50)
                pygame.draw.rect(render_surface, GOAL_COLOR, header, border_top_left_radius=8, border_top_right_radius=8)
                t_surf = font_title.render(level.edu_card["title"], True, WHITE)
                render_surface.blit(t_surf, t_surf.get_rect(center=header.center))

                for i, pt in enumerate(level.edu_card["points"]):
                    p_surf = font_body.render(pt, True, TEXT_BG)
                    render_surface.blit(p_surf, (card.x + 35, card.y + 75 + i * 40))

                footer_msg = "Pressione [ESPAÇO] ou [ENTER] para a próxima fase" if current_idx < len(levels) - 1 else "Parabéns! Jornada concluída! Pressione [ESPAÇO] para o Menu"
                f_surf = font_hud.render(footer_msg, True, GOAL_COLOR)
                render_surface.blit(f_surf, f_surf.get_rect(center=(WIDTH // 2, card.bottom - 28)))

            # 6. Efeito Screen Shake
            offset_x = 0
            offset_y = 0
            if level.shake_intensity > 0:
                offset_x = random.randint(-level.shake_intensity, level.shake_intensity)
                offset_y = random.randint(-level.shake_intensity, level.shake_intensity)
                level.shake_intensity = max(0, level.shake_intensity - 1)

            screen.fill(BG_COLOR)
            screen.blit(render_surface, (offset_x, offset_y))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()