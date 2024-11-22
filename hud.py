from settings import *

class Hud(pygame.sprite.Sprite):
    
    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.image.load(join('media', 'items', 'hud.png')).convert_alpha()
        self.rect = self.image.get_rect(topleft = (0,0))
        