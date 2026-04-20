import pygame
import datetime
import math

# 1. Setup
pygame.init()
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS 2: Advanced Paint")

# The Canvas holds the permanent drawing
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill((255, 255, 255))

# 2. Tools & State
color = (0, 0, 0)
brush_sizes = [2, 5, 10]
thickness = 5
mode = 'pencil' # Options: pencil, line, rect, circle, square, right_tri, equi_tri, rhombus, fill, text

# Text Tool Variables
font = pygame.font.SysFont("Arial", 24)
text_buffer = ""
text_pos = None
is_typing = False

def flood_fill(surface, x, y, new_color):
    """Fills a closed area using a stack-based algorithm."""
    target_color = surface.get_at((x, y))
    if target_color == new_color: return
    stack = [(x, y)]
    while stack:
        curr_x, curr_y = stack.pop()
        if surface.get_at((curr_x, curr_y)) != target_color: continue
        surface.set_at((curr_x, curr_y), new_color)
        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            nx, ny = curr_x + dx, curr_y + dy
            if 0 <= nx < WIDTH and 0 <= ny < HEIGHT:
                if surface.get_at((nx, ny)) == target_color:
                    stack.append((nx, ny))

# 3. Main Loop
running, drawing = True, False
start_pos = (0, 0)

while running:
    screen.blit(canvas, (0, 0)) # Draw the permanent canvas first
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            # --- BRUSH SIZE ---
            if event.key == pygame.K_1: thickness = brush_sizes[0]
            if event.key == pygame.K_2: thickness = brush_sizes[1]
            if event.key == pygame.K_3: thickness = brush_sizes[2]
            
            # --- TOOLS ---
            if event.key == pygame.K_p: mode = 'pencil'
            if event.key == pygame.K_l: mode = 'line'
            if event.key == pygame.K_f: mode = 'fill'
            if event.key == pygame.K_t: mode = 'text'
            
            # --- SHAPES (Practice 10-11) ---
            if event.key == pygame.K_r: mode = 'rect'
            if event.key == pygame.K_c: mode = 'circle'
            if event.key == pygame.K_s: mode = 'square'
            
            # --- SAVE (Ctrl + S) ---
            if event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                filename = datetime.datetime.now().strftime("paint_%Y%m%d_%H%M%S.png")
                pygame.image.save(canvas, filename)
                print(f"Saved to {filename}")

            # --- TEXT TYPING ---
            if is_typing:
                if event.key == pygame.K_RETURN:
                    txt_surf = font.render(text_buffer, True, color)
                    canvas.blit(txt_surf, text_pos)
                    is_typing, text_buffer = False, ""
                elif event.key == pygame.K_BACKSPACE:
                    text_buffer = text_buffer[:-1]
                else:
                    text_buffer += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:
            if mode == 'fill':
                flood_fill(canvas, *event.pos, color)
            elif mode == 'text':
                text_pos, is_typing, text_buffer = event.pos, True, ""
            else:
                drawing, start_pos = True, event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                # Finalize drawing onto the permanent canvas
                if mode == 'line':
                    pygame.draw.line(canvas, color, start_pos, mouse_pos, thickness)
                elif mode == 'rect':
                    w, h = mouse_pos[0]-start_pos[0], mouse_pos[1]-start_pos[1]
                    pygame.draw.rect(canvas, color, (start_pos[0], start_pos[1], w, h), thickness)
                elif mode == 'circle':
                    rad = int(math.hypot(mouse_pos[0]-start_pos[0], mouse_pos[1]-start_pos[1]))
                    pygame.draw.circle(canvas, color, start_pos, rad, thickness)
                drawing = False

        if event.type == pygame.MOUSEMOTION and drawing and mode == 'pencil':
            # Pencil draws directly to the canvas for smooth freehand
            pygame.draw.circle(canvas, color, mouse_pos, thickness)

    # 4. Previews (Visible only while dragging)
    if drawing:
        if mode == 'line':
            pygame.draw.line(screen, color, start_pos, mouse_pos, thickness)
        elif mode == 'rect':
            w, h = mouse_pos[0]-start_pos[0], mouse_pos[1]-start_pos[1]
            pygame.draw.rect(screen, color, (start_pos[0], start_pos[1], w, h), thickness)

    # Show typing text preview
    if is_typing:
        screen.blit(font.render(text_buffer + "|", True, color), text_pos)

    pygame.display.flip()

pygame.quit()