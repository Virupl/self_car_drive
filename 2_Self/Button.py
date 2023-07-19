import pygame


class Button:
    def __init__(self, rect, icon, callback):
        self.rect = pygame.Rect(rect)
        self.icon = pygame.image.load(icon)
        self.callback = callback

    def draw(self, surface):
        # pygame.draw.rect(surface, (200, 200, 200), self.rect)
        # font = pygame.font.Font(None, 24)
        # text = font.render(self.text, True, (0, 0, 0))
        # text_rect = text.get_rect(center=self.rect.center)
        # surface.blit(text, text_rect)
        surface.blit(self.icon, self.rect.topleft)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()
