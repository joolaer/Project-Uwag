from settings import *
from groups import AllSprites
from player import Player

class Game:
    
    def __init__(self) -> None:
        # setup
        pygame.init()
        self.running = True
        
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Project Uwag')
        self.clock = pygame.time.Clock()
        self.all_sprites = AllSprites()
        self.player = Player((self.all_sprites),enums. CNST_DIRECTION_RIGHT)
        
    def run(self):
        
        while self.running:
            
            self.clock.tick(60)
            
            self._check_events()
            self._update_events()
            
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    
    def _update_events(self):
        self.all_sprites.update()
        self.display_surface.fill('Grey')
        self.all_sprites.draw(self.display_surface)
        pygame.display.update()
    
if __name__ == '__main__':
    game = Game()
    game.run()