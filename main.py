# main.py
import pygame
import sys
from settings import *
from player import Player
from level import Level1, Level2, Level3

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("EducaJogo Fiscal - Protótipo NP2")
    clock = pygame.time.Clock()

    font_hud = pygame.font.SysFont("arial", 20, bold=True)
    font_card = pygame.font.SysFont("arial", 17, bold=False)

    levels = [Level1(), Level2(), Level3()]
    current_idx = 0
    level = levels[current_idx]
    player = Player(*level.spawn_pos)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # Reinício rápido da fase atual
                if event.key == pygame.K_r:
                    level.reset()
                    player = Player(*level.spawn_pos)

                # Avançar para a próxima fase ao vencer
                if level.won and event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    current_idx = (current_idx + 1) % len(levels)
                    level = levels[current_idx]
                    level.reset()
                    player = Player(*level.spawn_pos)

        # Atualização
        player.update(level.platforms)
        level.update(player)

        # Renderização
        screen.fill(BG_COLOR)
        level.draw(screen, font_hud)
        player.draw(screen)

        # HUD Superior dinâmico
        status_text, status_color = level.get_hud_info()
        hud_surf = font_hud.render(status_text, True, status_color)
        screen.blit(hud_surf, (20, 20))

        # Banner de Morte
        if not player.alive:
            overlay = pygame.Surface((WIDTH, 90))
            overlay.fill(TEXT_BG)
            screen.blit(overlay, (0, HEIGHT // 2 - 45))

            msg_surf = font_hud.render(level.death_message, True, WHITE)
            screen.blit(msg_surf, msg_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 12)))

            sub_surf = font_hud.render("Pressione R para tentar novamente", True, SPIKE_COLOR)
            screen.blit(sub_surf, sub_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 18)))

        # Banner de Vitória
        # Card Educativo de Vitória
        # Card Educativo de Vitória (com ajuste automático de largura)
        if level.won:
            dim_bg = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            dim_bg.fill((0, 0, 0, 160))
            screen.blit(dim_bg, (0, 0))

            card_rect = pygame.Rect(0, 0, 720, 260)
            card_rect.center = (WIDTH // 2, HEIGHT // 2)
            pygame.draw.rect(screen, BG_COLOR, card_rect, border_radius=12)
            pygame.draw.rect(screen, GOAL_COLOR, card_rect, width=4, border_radius=12)

            # Cabeçalho verde
            header_rect = pygame.Rect(card_rect.x, card_rect.y, card_rect.width, 48)
            pygame.draw.rect(screen, GOAL_COLOR, header_rect, border_top_left_radius=10, border_top_right_radius=10)
            title_surf = font_hud.render(level.edu_card["title"], True, WHITE)
            screen.blit(title_surf, title_surf.get_rect(center=header_rect.center))

            # Largura máxima permitida dentro do cartão (com 30px de margem de cada lado)
            max_text_width = card_rect.width - 60

            # Tópicos educativos com ajuste automático se passar da borda
            for i, point in enumerate(level.edu_card["points"]):
                font_size = 18
                temp_font = pygame.font.SysFont("arial", font_size, bold=False)
                pt_surf = temp_font.render(point, True, TEXT_BG)

                # Reduz a fonte 1px por vez até caber com folga dentro do card
                while pt_surf.get_width() > max_text_width and font_size > 12:
                    font_size -= 1
                    temp_font = pygame.font.SysFont("arial", font_size, bold=False)
                    pt_surf = temp_font.render(point, True, TEXT_BG)

                screen.blit(pt_surf, (card_rect.x + 30, card_rect.y + 74 + i * 38))

            # Rodapé
            next_label = "Pressione ESPAÇO ou ENTER para a próxima fase" if current_idx < len(levels) - 1 else "Protótipo Concluído! Pressione ESPAÇO para reiniciar"
            sub_surf = font_hud.render(next_label, True, GOAL_COLOR)
            screen.blit(sub_surf, sub_surf.get_rect(center=(WIDTH // 2, card_rect.bottom - 26)))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()