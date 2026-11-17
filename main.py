# main.py
import pygame
import sys
from settings import *
from player import Player
from level import Level1

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("EducaJogo Fiscal - Protótipo NP2")
    clock = pygame.time.Clock()

    font_hud = pygame.font.SysFont("arial", 20, bold=True)
    font_msg = pygame.font.SysFont("arial", 22, bold=True)

    level = Level1()
    player = Player(*level.spawn_pos)

    while True:
        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # Reinício rápido (essencial no estilo Level Devil)
                if event.key == pygame.K_r:
                    level.reset()
                    player = Player(*level.spawn_pos)

        # Atualização de Lógica
        player.update(level.platforms)
        level.update(player)

        # Renderização
        screen.fill(BG_COLOR)
        level.draw(screen, font_hud)
        player.draw(screen)

        # HUD Superior
        status_text = "Nota Fiscal: EMITIDA (Infraestrutura Segura)" if level.nota_fiscal_emitida else "Nota Fiscal: NÃO EMITIDA (Cuidado!)"
        status_color = GOAL_COLOR if level.nota_fiscal_emitida else SPIKE_COLOR
        hud_surf = font_hud.render(f"Fase 1: O Desconto sem Nota | {status_text}", True, status_color)
        screen.blit(hud_surf, (20, 20))

        # Banner de Feedback na Morte
        if not player.alive:
            overlay = pygame.Surface((WIDTH, 90))
            overlay.fill(TEXT_BG)
            screen.blit(overlay, (0, HEIGHT // 2 - 45))

            msg_surf = font_hud.render(level.death_message, True, WHITE)
            msg_rect = msg_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 12))
            screen.blit(msg_surf, msg_rect)

            sub_surf = font_hud.render("Pressione R para tentar novamente", True, SPIKE_COLOR)
            sub_rect = sub_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 18))
            screen.blit(sub_surf, sub_rect)

        # Banner de Vitória
        if level.won:
            overlay = pygame.Surface((WIDTH, 90))
            overlay.fill(GOAL_COLOR)
            screen.blit(overlay, (0, HEIGHT // 2 - 45))

            win_surf = font_hud.render("Fase Concluída! O tributo virou infraestrutura pública.", True, WHITE)
            win_rect = win_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 12))
            screen.blit(win_surf, win_rect)

            sub_surf = font_hud.render("Pressione R para jogar novamente", True, WHITE)
            sub_rect = sub_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 18))
            screen.blit(sub_surf, sub_rect)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()