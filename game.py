from settings import *
from npc import NPC
from dialogue import DialogSprite
from groups import AllSprites, AbsoluteSprites
from player import Player
from sprites import Sprite, CollisionSprite, NonCollisionSprite, TeleportSprite
from hud import Hud
from pytmx.util_pygame import load_pygame

class Game:
    
    def __init__(self) -> None:
        # setup
        pygame.init()
        self.running = True
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Project Uwag')
        self.clock = pygame.time.Clock()
        self.all_sprites = AllSprites()
        self.absolute_sprites = AbsoluteSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.character_sprites = pygame.sprite.Group()
        self.teleport_sprites = pygame.sprite.Group()
        self.setup()
        
    def setup(self):
        map = load_pygame(join('media', 'map', 'map_1.tmx'))
        
        for x, y, image in map.get_layer_by_name('Grounds').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)
            
        for obj in map.get_layer_by_name('Objects'):
            CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))
            
        for obj in map.get_layer_by_name('Collisions'):
            CollisionSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)
            
        for obj in map.get_layer_by_name('Teleporters'):
            TeleportSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.teleport_sprites, obj.properties)
        
        self.hud = Hud(self.absolute_sprites)
            
        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'map_1_spawn':
                self.player = Player((obj.x, obj.y), enums.CNST_DIRECTION_RIGHT, (self.all_sprites, self.character_sprites), self.collision_sprites, self.teleport_sprites)
        
        NPC('Mary (Mom)', 'mary', self.all_sprites, self.character_sprites, self.absolute_sprites)
                
        #DialogSprite(self.absolute_sprites, self.display_surface)
        
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
        self.absolute_sprites.update()
        self.display_surface.fill('black')
        self.all_sprites.draw(self.player.rect.center)
        self.absolute_sprites.draw(self.display_surface) 
        pygame.display.update()
    
if __name__ == '__main__':
    game = Game()
    game.run()