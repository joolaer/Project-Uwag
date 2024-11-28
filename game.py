from settings import *
from npc import NPC
from dialogue import DialogSprite
from groups import AllSprites, AbsoluteSprites
from player import Player
from sprites import Sprite, CollisionSprite, NonCollisionSprite, TeleportSprite
from hud import Hud
from pytmx.util_pygame import load_pygame
from face import Face
from button import Button

class Game:
    
    def __init__(self) -> None:
        # setup
        pygame.init()
        self.running = True
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Project Uwag')
        self.clock = pygame.time.Clock()
        self.all_sprites = AllSprites()
        self.player_sprite = pygame.sprite.GroupSingle()
        self.absolute_sprites = AbsoluteSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.character_sprites = pygame.sprite.Group()
        self.teleport_sprites = pygame.sprite.Group()
        self.npc_buttons_sprites = pygame.sprite.Group()
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
                self.player = Player((obj.x, obj.y), enums.CNST_DIRECTION_RIGHT, (self.all_sprites, self.player_sprite), self.collision_sprites, self.teleport_sprites)
        
        NPC('Mary (Mom)', 'mary', (self.all_sprites, self.character_sprites), self.absolute_sprites, self.npc_buttons_sprites)
        
    def run(self):
        
        while self.running:
            self._check_events()  
            self._set_char_collision()
            self._check_char_collision()
            self._update_events()
            
    def _set_char_collision(self):
        for sprite in self.character_sprites:
            if self.player.hitbox_rect.colliderect(sprite.hitbox_rect):
                state.set_STATE_COLLIDED_CHAR(sprite)
            else:
                state.set_STATE_COLLIDED_CHAR(None)
                
                
    def _check_char_collision(self):
        char = state.STATE_COLLIDED_CHAR
        if char:
            if not hasattr(self, 'face'):
                self.face = Face(self.absolute_sprites, char)
                if state.STATE_COLLIDED_CHAR_MODE != enums.CNST_DATA_KEY_DIALOG:
                    Button((self.npc_buttons_sprites), "Talk", enums.CNST_NPC_BUTTON_TYPE_TALK, (275, 510), char.talk)
                    Button((self.npc_buttons_sprites), "Action", enums.CNST_NPC_BUTTON_TYPE_ACTION, (375, 510), char.action)
                    Button((self.npc_buttons_sprites), "Inspect", enums.CNST_NPC_BUTTON_TYPE_INSPECT, (475, 510), char.inspect)
        else:
            if hasattr(self, 'face'):
                self.npc_buttons_sprites.empty()
                self.face.kill()
                del self.face
            
            
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        if state.STATE_COLLIDED_CHAR_MODE == enums.CNST_NPC_BUTTON_TYPE_TALK:
            self.npc_buttons_sprites.empty()
                
    
    def _update_events(self):
        self.clock.tick(60)
        self.all_sprites.update()
        self.absolute_sprites.update()
        self.npc_buttons_sprites.update()
        self.display_surface.fill('black')
        self.all_sprites.draw(self.player.rect.center)
        self.absolute_sprites.draw(self.display_surface) 
        self.npc_buttons_sprites.draw(self.display_surface)
        pygame.display.update()
    
if __name__ == '__main__':
    game = Game()
    game.run()