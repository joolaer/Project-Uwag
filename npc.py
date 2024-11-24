from settings import *
from dialog_data import DIALOG_DATA
from character_data import CHARACTER_DATA
from groups import AbsoluteSprites
from dialogue import DialogSprite
import player

class NPC(pygame.sprite.Sprite):
    
    def __init__(self, name, file_name, groups, character_sprites, absolute_sprites):
        super().__init__(groups)
        self.name = name
        self.file_name = file_name
        self.character_sprites = character_sprites
        self.absolute_sprites = absolute_sprites
        self.dialogue_index = 0
        self.display_surface = pygame.display.get_surface()
        self.frame_index = 0
        # self.dialogue = dialogue
        self.stats = CHARACTER_DATA[self.file_name][enums.CNST_DATA_KEY_STATS]
        self.direction = enums.CNST_DIRECTION_LEFT
        self.idle_frames = CHARACTER_DATA[self.file_name][enums.CNST_DATA_KEY_IDLE]
        self.image = self.idle_frames[self._check_direction(self.direction)][0].convert_alpha()
        self.rect = self.image.get_frect(midbottom = (300, 450))
        self.hitbox_rect = self.rect.inflate(-60, 0)
                        
    def animate(self):
        self.frame_index = self.frame_index + .1
        self.image = self.idle_frames[self._check_direction(self.direction)][int(self.frame_index) % len(self.idle_frames[self._check_direction(self.direction)])]
    
    def collision(self):
        for sprite in self.character_sprites:
            if isinstance(sprite, player.Player) and sprite.hitbox_rect.colliderect(self.hitbox_rect):
                key_pressed = pygame.key.get_just_pressed()
                if key_pressed[pygame.K_w] and helper_dialog.get_dialogue_mode() == False:
                    helper_dialog.set_dialogue_mode(True)
                    self.current_dialog = DialogSprite(self, self.name, self.file_name, self.absolute_sprites)
                        
        
    def _check_direction(self, direction):
        if int(direction) == enums.CNST_DIRECTION_RIGHT:
            return 'right'
        elif int(direction) == enums.CNST_DIRECTION_LEFT:
            return 'left'
                        
    def update(self):
        self.collision()
        self.animate()
        self.rect.midbottom = self.hitbox_rect.midbottom
        