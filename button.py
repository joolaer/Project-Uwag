from settings import *

class Button(pygame.sprite.Sprite):
    
    def __init__(self, groups, text, type, pos, function) -> None:
        super().__init__(groups)
        self.text = text
        self.type = type
        self.function = function
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
            self.surf.fill((255, 255 ,255))
            self.text_surf = self.font.render(self.text, False, (0,0,0))
            
            if pygame.mouse.get_just_pressed()[0]:
                self.function()
        else:
            self.surf.fill((200,200,200))
            self.text_surf = self.font.render(self.text, False, (50,50,50))
        
        
            
    def update(self) -> None:
        self._if_hovered()
        self.surf.blit(self.text_surf, self.text_surf.get_frect(center = (self.width / 2, self.height / 2)))
        self.image = self.surf
        
class ChoicesButton(pygame.sprite.Sprite):
    
    def __init__(self, groups, text, pos, dialog) -> None:
        super().__init__(groups)
        self.text = text
        self.pos = pos
        self.dialog = dialog
        self.font = pygame.font.Font(None, 24)
        
        self.text_surf = self.font.render(self.text, False, 'red')
        self.width = 700
        self.height = 40
        
        self.surf = pygame.Surface((self.width, self.height))
        self.image = self.surf
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2,self.pos))
        
    def _if_hovered(self):
        click_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(click_pos):
            self.surf.fill('red')
            self.text_surf = self.font.render(self.text, False, 'green')
            
            if pygame.mouse.get_just_pressed()[0]:
                self.dialog._chosen_effect(self.text)
        else:
            self.surf.fill('blue')
            self.text_surf = self.font.render(self.text, False, 'red')
        
        
            
    def update(self) -> None:
        self._if_hovered()
        self.surf.blit(self.text_surf, self.text_surf.get_frect(center = (self.width / 2, self.height / 2)))
        

class BorderedButton(pygame.sprite.Sprite):

    def __init__(self, groups, text:str, position:tuple, func, color_main: tuple, color_hovered: tuple, size:tuple):
        super().__init__(groups)
        self.text = text
        self.position_x = position[0]
        self.position_y = position[1]
        self.width = size[0]
        self.height = size[1]
        self.func = func
        self.color_border = color_main[1]
        self.color_main = color_main[0]
        self.color_text = color_main[2]

        self.hovered_color_border = color_hovered[1]
        self.hovered_color_main =  color_hovered[0]
        self.hovered_color_text = color_hovered[1]

        self.surf = pygame.Surface((self.width, self.height))
        self.image = self.surf
        self.rect = self.image.get_frect(topleft = (self.position_x, self.position_y))
        self.child_surf = pygame.Surface((self.width - 10, self.height - 10))
        self.font = pygame.font.Font(None, 24)
        
    def set_unhovered_button(self):
        self.text_surf = self.font.render(self.text, False, self.color_text)
        self.surf.fill(self.color_border)
        self.child_surf.fill(self.color_main)

    def set_hovered_button(self):
        self.text_surf = self.font.render(self.text, False, self.hovered_color_text)
        self.surf.fill(self.hovered_color_border)
        self.child_surf.fill(self.hovered_color_main)

    def check_if_hovered(self):
        click_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(click_pos):
            self.set_hovered_button()
            
            if pygame.mouse.get_just_pressed()[0]:
                self.func()
        else:
            self.set_unhovered_button()

    def update(self) -> None:
        self.check_if_hovered()
        self.surf.blit(self.child_surf, self.child_surf.get_frect(center = (self.width / 2, self.height / 2)))
        self.surf.blit(self.text_surf, self.text_surf.get_frect(center = (self.width / 2, self.height / 2)))
        self.image = self.surf
        
    