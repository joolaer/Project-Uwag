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
        self.stats = deepcopy(CHARACTER_DATA[self.file_name][enums.CNST_DATA_KEY_STATS])
        self.locations_data = deepcopy(CHARACTER_DATA[self.file_name][enums.CNST_DATA_KEY_LOCATIONS])
        self.direction = enums.CNST_DIRECTION_LEFT
        self.idle_frames = deepcopy(CHARACTER_DATA[self.file_name][enums.CNST_DATA_KEY_IDLE])
        self.image = self.idle_frames[self._check_direction(self.direction)][0].convert_alpha()
        self.rect = self.image.get_frect(midbottom = (0,0))
        self.hitbox_rect = self.rect.inflate(-60, 0)
        self.update_location()
                        
    def animate(self):
        self.frame_index = self.frame_index + .1
        self.image = self.idle_frames[self._check_direction(self.direction)][int(self.frame_index) % len(self.idle_frames[self._check_direction(self.direction)])]
        
    def talk(self):
        state.set_STATE_COLLIDED_CHAR_MODE(enums.CNST_NPC_BUTTON_TYPE_TALK)
        self.current_dialog = DialogSprite(self, self.game_time, self.name, self.file_name, self.absolute_sprite, self.npc_buttons_sprites)
        
    def remove_dialog(self):
        self.current_dialog.kill()
        del self.current_dialog
    
    def action(self):
        pass
    
    def inspect(self):
        pass        
        
    def update_location(self):
        locations = deepcopy(self.locations_data)
        time = locations[state.current_time]
        tVal = time[enums.CNST_DATA_KEY_DEFAULT]['position']
        
        for item, value in time.items():
            if 'condition' in value:
                if self.check_location_condition(value['condition']):
                    tVal = value['position']
                    break
            else:
                tVal = value['position']

            # print(f'@@{tVal}')

        self.hitbox_rect.midbottom = tVal

    def check_location_condition(self, conditions):
        tVal = False
        for condition in conditions:
            type = condition[0]
            cond = condition[1]
            val = condition[2]
            # print(f'type: {type}')
            # print(f'cond: {cond}')
            # print(f'val: {val}')
            # print(f'state.current_day: {state.current_day}')
            # print('@@@@@@@@@@@@@@@@@@@@')
            if type == 'day':
                if (cond and val == state.current_day) or (not cond and val != state.current_day):
                    tVal = True
                else:
                    return False
            #elif type == 'buff':

        return tVal

    def _check_direction(self, direction):
        if int(direction) == enums.CNST_DIRECTION_RIGHT:
            return 'right'
        elif int(direction) == enums.CNST_DIRECTION_LEFT:
            return 'left'
                        
    def update(self):
        self.animate()
        self.rect.midbottom = self.hitbox_rect.midbottom
        