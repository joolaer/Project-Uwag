from typing import Any
from settings import *

class Button(pygame.sprite.Sprite):
    
    def __init__(self, groups, text, type, pos) -> None:
        super().__init__(groups)
        self.text = text
        self.type = type
        self.font = pygame.font.Font(None, 24)
        
        self.text_surf = self.font.render(self.text, False, (50,50,50))
        self.width = max(30, self.text_surf.get_width() + 5 * 5)
        self.width = self.width if self.width > 80 else 80
        self.height = self.text_surf.get_height() + 5 * 5
        
        self.surf = pygame.Surface((self.width, self.height))
        self.image = self.surf
        self.rect = self.image.get_frect(topleft = (pos[0],pos[1]))
        
    def _if_hovered(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            print(self.text)
            self.surf.fill((255, 255 ,255))
            self.text_surf = self.font.render(self.text, False, (0,0,0))
        else:
            self.surf.fill((200,200,200))
            self.text_surf = self.font.render(self.text, False, (50,50,50))
    def update(self) -> None:
        self._if_hovered()
        self.surf.blit(self.text_surf, self.text_surf.get_frect(center = (self.width / 2, self.height / 2)))
        self.image = self.surf