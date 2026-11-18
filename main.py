# main.py
import pygame
import sys
import random
from settings import *
from player import Player
from level import Level1, Level2, Level3

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("O Caminho do Tributo - Conscientização Fiscal")
    clock = pygame.time.Clock()

    # Fontes pré-carregadas (boa prática, não recria no loop)
    font_hud = pygame.font.SysFont("arial", 20, bold=True)
    font_title = pygame.font.SysFont("arial", 22, bold=True)
    font_body = pygame.font.SysFont("arial", 16, bold=False)

    levels = [Level1(), Level2(), Level3()]
    current_idx = 0
    level = levels[current_idx]
    player = Player(*level.spawn_pos)

    # Superfície para Screen Shake
    render_surface = pygame.Surface((WIDTH, HEIGHT))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    level.reset()
                    player = Player(*level.spawn_pos)

                if level.won and event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    current_idx = (current_idx + 1) % len(levels)
                    level = levels[current_idx]
                    level.reset()
                    player = Player(*level.spawn_pos)

        # Lógica de atualização
        player.update(level.platforms)
        level.update(player)

        # Desenho no buffer
        render_surface.fill(BG_COLOR)
        level.draw(render_surface, font_hud)
        player.draw(render_surface)

        # HUD do topo
        status_text, status_color = level.get_hud_info()
        hud_surf = font_hud.render(status_text, True, status_color)
        render_surface.blit(hud_surf, (20, 20))

        # Tela de Morte
        if not player.alive:
            overlay = pygame.Surface((WIDTH, 90), pygame.SRCALPHA)
            overlay.fill((20, 20, 20, 210))
            render_surface.blit(overlay, (0, HEIGHT // 2 - 45))

            msg_surf = font_hud.render(level.death_message, True, WHITE)
            render_surface.blit(msg_surf, msg_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 12)))

            sub_surf = font_body.render("Pressione [R] para reiniciar a fase", True, (255, 120, 120))
            render_surface.blit(sub_surf, sub_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 18)))

        # Card de Conclusão / Aprendizado Fiscal
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

            footer_msg = "Pressione [ESPAÇO] ou [ENTER] para a próxima fase" if current_idx < len(levels) - 1 else "Parabéns! Você completou a jornada fiscal! [ESPAÇO] para recomeçar"
            f_surf = font_hud.render(footer_msg, True, GOAL_COLOR)
            render_surface.blit(f_surf, f_surf.get_rect(center=(WIDTH // 2, card.bottom - 28)))

        # Aplicação de Screen Shake no display principal
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