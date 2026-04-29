import pygame
import datetime
import math

# 1. Setup
pygame.init()
WIDTH, HEIGHT = 1000, 750  # Added 50px for a bottom UI/Status bar
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS 2: Advanced Paint")

# The Canvas holds the permanent drawing (white background)
canvas = pygame.Surface((WIDTH, HEIGHT - 50))
canvas.fill((255, 255, 255))

# 2. Tools & State
color = (0, 0, 0)
brush_sizes = [2, 5, 10]
thickness = 5
mode = 'pencil' 

# Text Tool Variables
font = pygame.font.SysFont("Arial", 24)
ui_font = pygame.font.SysFont("Arial", 18)
text_buffer = ""
text_pos = None
is_typing = False

def flood_fill(surface, x, y, new_color):
    """Fills a closed area using a stack-based algorithm to avoid recursion limits."""
    try:
        target_color = surface.get_at((x, y))
    except IndexError: return
    if target_color == new_color: return
    
    stack = [(x, y)]
    while stack:
        curr_x, curr_y = stack.pop()
        if surface.get_at((curr_x, curr_y)) != target_color: continue #get_at getting a color of a position
        
        surface.set_at((curr_x, curr_y), new_color)#opposite of get_at
        
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = curr_x + dx, curr_y + dy
            if 0 <= nx < WIDTH and 0 <= ny < (HEIGHT - 50):
                if surface.get_at((nx, ny)) == target_color:
                    stack.append((nx, ny))

def draw_shape(surf, shape_mode, start, end, thick, current_color):
    """Handles logic for drawing shapes on preview or canvas."""
    x1, y1 = start
    x2, y2 = end
    w, h = x2 - x1, y2 - y1

    if shape_mode == 'line':
        pygame.draw.line(surf, current_color, start, end, thick)
    elif shape_mode == 'rect':
        pygame.draw.rect(surf, current_color, (min(x1, x2), min(y1, y2), abs(w), abs(h)), thick)
    elif shape_mode == 'square':
        side = max(abs(w), abs(h))
        s_x = x1 if x2 > x1 else x1 - side
        s_y = y1 if y2 > y1 else y1 - side
        pygame.draw.rect(surf, current_color, (s_x, s_y, side, side), thick)
    elif shape_mode == 'circle':
        rad = int(math.hypot(w, h))
        pygame.draw.circle(surf, current_color, start, rad, thick)
    elif shape_mode == 'right_tri':
        pygame.draw.polygon(surf, current_color, [(x1, y1), (x1, y2), (x2, y2)], thick)
    elif shape_mode == 'equi_tri':
        # Draws triangle based on width, height adjusts to keep it equilateral
        tri_h = int(math.sqrt(3) / 2 * w)
        pygame.draw.polygon(surf, current_color, [(x1, y1), (x2, y1), (x1 + w // 2, y1 - tri_h)], thick)
    elif shape_mode == 'rhombus':
        points = [(x1 + w // 2, y1), (x1 + w, y1 + h // 2), (x1 + w // 2, y1 + h), (x1, y1 + h // 2)]
        pygame.draw.polygon(surf, current_color, points, thick)

# 3. Main Loop
running, drawing = True, False
start_pos = (0, 0)
last_pos = (0, 0)

while running:
    # Draw background and then the drawing canvas
    screen.fill((200, 200, 200)) # UI background
    screen.blit(canvas, (0, 0)) 
    
    mouse_pos = pygame.mouse.get_pos()
    # Adjust mouse_pos for canvas boundary if necessary (only draw if inside)
    on_canvas = mouse_pos[1] < (HEIGHT - 50)
    
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
            if event.key == pygame.K_x: mode = 'eraser'
            
            # --- SHAPES ---
            if event.key == pygame.K_r: mode = 'rect'
            if event.key == pygame.K_c: mode = 'circle'
            if event.key == pygame.K_s: mode = 'square'
            if event.key == pygame.K_i: mode = 'right_tri'
            if event.key == pygame.K_e: mode = 'equi_tri'
            if event.key == pygame.K_h: mode = 'rhombus'

            # --- COLOR PICKER (Quick select) ---
            if event.key == pygame.K_g: color = (0, 255, 0) # Green
            if event.key == pygame.K_b: color = (0, 0, 255) # Blue
            if event.key == pygame.K_k: color = (0, 0, 0)   # Black
            
            # --- SAVE (Ctrl + S) ---
            if event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                filename = datetime.datetime.now().strftime("paint_%Y%m%d_%H%M%S.png")
                pygame.image.save(canvas, filename)
                print(f"Saved to {filename}")

            # --- TEXT TYPING ---
            if is_typing:
                if event.key == pygame.K_RETURN:
                    txt_surf = font.render(text_buffer, True, color)#creates a surface(text image)
                    canvas.blit(txt_surf, text_pos)
                    is_typing, text_buffer = False, ""
                elif event.key == pygame.K_ESCAPE:
                    is_typing, text_buffer = False, ""
                elif event.key == pygame.K_BACKSPACE:
                    text_buffer = text_buffer[:-1]
                else:
                    text_buffer += event.unicode#gives actual character

        if event.type == pygame.MOUSEBUTTONDOWN and on_canvas:
            if mode == 'fill':
                flood_fill(canvas, *event.pos, color)
            elif mode == 'text':
                text_pos, is_typing, text_buffer = event.pos, True, ""
            else:
                drawing, start_pos = True, event.pos
                last_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                if mode == 'eraser':
                    pass # Handled in MOUSEMOTION
                elif mode != 'pencil':
                    draw_shape(canvas, mode, start_pos, mouse_pos, thickness, color)
                drawing = False

        if event.type == pygame.MOUSEMOTION and drawing and on_canvas:
            if mode == 'pencil':
                pygame.draw.line(canvas, color, last_pos, mouse_pos, thickness * 2)
                last_pos = mouse_pos
            elif mode == 'eraser':
                pygame.draw.circle(canvas, (255, 255, 255), mouse_pos, thickness * 2)

    # 4. Previews & UI
    if drawing and mode not in ['pencil', 'eraser', 'fill', 'text']:
        draw_shape(screen, mode, start_pos, mouse_pos, thickness, color)

    if is_typing:
        screen.blit(font.render(text_buffer + "|", True, color), text_pos)

    # --- STATUS BAR (Bottom UI) ---
    pygame.draw.rect(screen, (50, 50, 50), (0, HEIGHT - 50, WIDTH, 50))
    status_text = f"Mode: {mode.upper()} | Size: {thickness} | Color: {color} | Ctrl+S to Save"
    info_surf = ui_font.render(status_text, True, (255, 255, 255))
    screen.blit(info_surf, (10, HEIGHT - 35))

    pygame.display.flip()

pygame.quit()
#P, L, R, C, S, I, E, H: Pencil, Line, Rect, Circle, Square, Right Tri, Equi Tri, Rhombus.

#F: Flood Fill.

#T: Text Tool (Click → Type → Enter).

#X: Eraser.

#1, 2, 3: Thickness levels.

#K, G, B: Black, Green, Blue colors.

#Ctrl+S: Save to PNG.