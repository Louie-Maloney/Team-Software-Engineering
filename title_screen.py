import pygame

def run_title_screen(screen, clock):

    ##create fonts
    title_font = pygame.font.SysFont("Courier New", 64, bold = True)
    enter_font = pygame.font.SysFont("Courier New", 64,)

    ##controls the visible state of the text (visible is true)
    blink_visible = True
    ##counts how many seconds since last blink
    blink_timer = 0.0
    
    ##game loop
    running = True
    while running:

        ##add the frames time to the blink counter
        dt = clock.tick(60) / 1000.0

        
        for event in pygame.event.get():
            ##detects if window was closed
            if event.type == pygame.QUIT:
                running = False
            ##detects if enter was pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False

        ##add the frames time to the counter, if a second has passed swap the value of blink_visible
        blink_timer += dt
        if blink_timer >= 1:
            blink_timer = 0.0
            blink_visible = not blink_visible

        ##draw the frame in the window
        screen.fill((0,0,0))

        ##render title text
        title = title_font.render("Computer Science Escape Room", True, (80, 255, 80))
        title_rect = title.get_rect(center = (640, 200))
        screen.blit(title, title_rect)

        ##render enter text
        if blink_visible:
            enter = enter_font.render("Press Enter To Begin", True, (30, 100, 30))
            enter_rect = enter.get_rect(center =(640, 400))
            screen.blit(enter, enter_rect)

        pygame.display.flip()

