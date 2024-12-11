import copy

from settings import *
from dialogue import DialogSprite
from dialog_data import DIALOG_DATA
from character_data import CHARACTER_DATA

class NPC(pygame.sprite.Sprite):
    
    def __init__(self, name, file_name, groups, game_time, absolute_sprite, npc_buttons_sprites):
        super().__init__(groups)
        self.name = name
        self.talking = False
        self.dialog_type = enums.CNST_NPC_BUTTON_TYPE_NONE
        self.emotion = enums.CNST_EMOTION_NORMAL
        self.file_name = file_name
        self.game_time = game_time
        self.absolute_sprite = absolute_sprite
        self.npc_buttons_sprites = npc_buttons_sprites
        self.frame_index = 0
        self.stats = copy.deepcopy(CHARACTER_DATA[self.file_name][enums.CNST_DATA_KEY_STATS])
        self.direction = enums.CNST_DIRECTION_LEFT
        self.idle_frames = copy.deepcopy(CHARACTER_DATA[self.file_name][enums.CNST_DATA_KEY_IDLE])
        self.image = self.idle_frames[self._check_direction(self.direction)][0].convert_alpha()
        self.rect = self.image.get_frect(midbottom = (300, 450))
        self.hitbox_rect = self.rect.inflate(-60, 0)
                        
    def animate(self):
        self.frame_index = self.frame_index + .1
        self.image = self.idle_frames[self._check_direction(self.direction)][int(self.frame_index) % len(self.idle_frames[self._check_direction(self.direction)])]
        
    def talk(self):
        print(f'{self.name} is talking')
        state.set_STATE_COLLIDED_CHAR_MODE(enums.CNST_NPC_BUTTON_TYPE_TALK)
        self.current_dialog = DialogSprite(self, self.game_time, self.name, self.file_name, self.absolute_sprite, self.npc_buttons_sprites)
        
    def remove_dialog(self):
        self.current_dialog.kill()
        del self.current_dialog
    
    def action(self):
        print(f'{self.name} is actioning')
    
    def inspect(self):
        print(f'{self.name} is inspecting')           
        
    def _check_direction(self, direction):
        if int(direction) == enums.CNST_DIRECTION_RIGHT:
            return 'right'
        elif int(direction) == enums.CNST_DIRECTION_LEFT:
            return 'left'
                        
    def update(self):
        self.animate()
        self.rect.midbottom = self.hitbox_rect.midbottom
        