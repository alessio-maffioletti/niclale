#the gunman and the samurai
import random
import pygame
from constants import *
import game as g
import power_up

game = g.Game()


def create_power_up():
    if len(game.power_up_list) < 2 and game.tick % 100 == 0:
        random_x, random_y = random.choice(game.available_coordinates)
        
        random_num = random.randint(0, 100)

        if random_num < 10:
            type = 1
            path = IMG_POWER1
        elif random_num >= 10 and random_num < 20:
            type = 2
            path = IMG_POWER2
        else:
            type = 3
            path = IMG_POWER3


        game.power_up_list.append(power_up.PowerUP(random_x * GRID_WIDTH + 15, random_y * GRID_WIDTH + 5, type, game.tick, game, path))

while True:
    if game.in_menu:
        game.screen.fill((255, 255, 255))

        # Blit image
        image_rect = game.screen.get_rect()
        image = pygame.image.load(IMG_FRONTSCREEN)
        scaled_image = pygame.transform.scale(image, (WIDTH, HEIGHT))
        game.screen.blit(scaled_image, image_rect)

        title_font = pygame.font.Font(None, TITLE_FONT_SIZE)
        title_surf = title_font.render("Gunman and Samurai", True, FONT_COLOR)
        title_rect = title_surf.get_rect(center=(WIDTH // 2, 100))
        pygame.draw.rect(game.screen, GRAY, title_rect)
        game.screen.blit(title_surf, title_rect)    

        # Draw buttons
        for button in game.buttons:
            button.draw(game.screen)

            # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            for button in game.buttons:
                button.handle_event(event)

        pygame.display.flip()

    if game.in_map_select:
        game.screen.fill(MAP_SELECT_COLOR)

        # Draw buttons
        for button in game.picture_buttons:
            button.draw(game.screen)

            # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            for button in game.picture_buttons:
                button.handle_event(event)

        pygame.display.flip()

    if game.game_over:
        game.screen.fill(GAME_OVER_COLOR)

        # Draw title
        title_font = pygame.font.Font(None, GAME_OVER_FONT_SIZE)
        title_surf = title_font.render("GAME OVER", True, GAME_OVER_FONT_COLOR)
        title_rect = title_surf.get_rect(center=(WIDTH // 2, 100))
        game.screen.blit(title_surf, title_rect)  

        # Draw buttons
        for button in game.game_over_buttons:
            button.draw(game.screen)

            # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            for button in game.game_over_buttons:
                button.handle_event(event)

        pygame.display.flip()


    if game.in_game:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()


        keys = pygame.key.get_pressed()

        # draw / render
        game.screen.fill(BACKGROUND_COLOR)

        game.draw_floor()

        create_power_up()


        # update
        
        # draw / render1
        for p in game.power_up_list:
            p.draw(game.screen)
            p.update(game.tick)
        
        for wall in game.wall_list:
            wall.draw(game.screen)

        for bullet in game.bullet_list:
            bullet.draw(game.screen)
            bullet.update(game.collision_rectangles)

            if bullet.health <= 0:
                game.bullet_list.remove(bullet)



        game.player1.update(game.collision_rectangles, keys, game.tick)
        game.player2.update(game.collision_rectangles, keys, game.tick)

        game.player1.draw(game.screen, game.tick)
        game.player2.draw(game.screen, game.tick)

        game.clock.tick(FPS)

        #check for game over
        if game.player1.health <= 0 or game.player2.health <= 0:
            game.in_game = False
            game.game_over = True
                    
        pygame.display.update()
        game.tick += 1
