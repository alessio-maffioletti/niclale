from constants import *
import pygame

class Button:
    def __init__(self, x, y, width, height, text, game, callback):
        self.game = game
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.gray = GRAY
        self.hover_color = HOVER_COLOR
        self.callback = callback
        self.font = pygame.font.Font(None, BUTTON_FONT_SIZE)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            color = self.hover_color
        else:
            color = GRAY

        pygame.draw.rect(screen, color, self.rect)
        
        # Draw text
        text_surf = self.font.render(self.text, True, FONT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                self.callback()


class PictureButton(Button):
    def __init__(self, x, y, width, height, image_path, game, callback, map_index):
        
        super().__init__(x, y, width, height, "", game, callback)
        self.image = pygame.image.load(image_path)  
        self.map_index = map_index

        # Scale the image to fit the button
        self.image = pygame.transform.scale(self.image, (width, height))

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            color = self.hover_color
        else:
            color = self.gray

        pygame.draw.rect(screen, color, self.rect) 
        screen.blit(self.image, self.rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                self.callback(self.map_index)
