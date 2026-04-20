import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    
    radius = 15
    drawing_mode = 'line' # Modes: 'line', 'rect', 'circle', 'eraser'
    color = (0, 0, 0) # Default color black
    
    # Simple list to store drawings to keep them on screen
    # In a real app, you'd draw to a persistent surface
    points = [] 

    while True:
        pressed_keys = pygame.key.get_pressed()
        alt_held = pressed_keys[pygame.K_LALT] or pressed_keys[pygame.K_RALT]
        ctrl_held = pressed_keys[pygame.K_LCTRL] or pressed_keys[pygame.K_RCTRL]
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held: return
                if event.key == pygame.K_F4 and alt_held: return
                
                # Mode selection
                if event.key == pygame.K_r: drawing_mode = 'rect'
                if event.key == pygame.K_c: drawing_mode = 'circle'
                if event.key == pygame.K_l: drawing_mode = 'line'
                if event.key == pygame.K_e: drawing_mode = 'eraser'
                
                # Color selection
                if event.key == pygame.K_1: color = (255, 0, 0) # Red
                if event.key == pygame.K_2: color = (0, 255, 0) # Green
                if event.key == pygame.K_3: color = (0, 0, 255) # Blue
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left click
                    start_pos = event.pos
                    if drawing_mode == 'circle':
                        pygame.draw.circle(screen, color, event.pos, radius)
                    elif drawing_mode == 'rect':
                        pygame.draw.rect(screen, color, (event.pos[0], event.pos[1], 50, 50))
            
            if event.type == pygame.MOUSEMOTION:
                position = event.pos
                if pygame.mouse.get_pressed()[0]: # If left button held
                    if drawing_mode == 'line':
                        pygame.draw.circle(screen, color, position, 2)
                    elif drawing_mode == 'eraser':
                        pygame.draw.circle(screen, (255, 255, 255), position, 20)

        pygame.display.flip()
        clock.tick(60)

main()