import pygame

def draw_text(screen, text, size, x, y, color=(0,0,0)):
    font = pygame.font.SysFont("Verdana", size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def button(screen, msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            return action()
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))
    draw_text(screen, msg, 20, x+(w/2), y+(h/2), (255,255,255))
    return None