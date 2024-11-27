from settings import *
from character_data import CHARACTER_DATA
from dialog_data import DIALOG_DATA
from helpers import *
from button import Button

import time
import copy

class DialogSprite(pygame.sprite.Sprite):
    def __init__(self, character, name, filename, all_group, npc_buttons_sprites):
        super().__init__(all_group)
        self.character = character
        self.name = name
        self.filename = filename
        self.all_group = all_group
        self.npc_buttons_sprites = npc_buttons_sprites
        
        self.character_data = copy.deepcopy(CHARACTER_DATA[self.filename])
        self.face_frames = self.character_data[enums.CNST_DATA_KEY_FACE]
        self.dialog_data = copy.deepcopy(DIALOG_DATA[self.filename])
        
        self.face_index = 0
        self.message_index = 0
        self.letters_rendered = 0
        self.dialog_space_key = False
        self.whole_message = self._get_dialog()
        self._set_message_choice_dialog()
        
        self.font = pygame.font.Font(None, 30)
        self.start_time = time.time()
        
        self.text_surf_name = self.font.render(self.name, False, (255, 15 ,15))
        self.surf = pygame.Surface((1070,300), pygame.SRCALPHA)
        self.surf.fill((0,0,0,0))
        
        
        self.image = self.surf
        self.rect = self.image.get_frect(bottomleft = (0, 720))
        
        self.skip_animation = False
        self.animating = True

        
        self.dialog_blit = DialogSpriteBlit(self.dialog_message, self.all_group)
        
    def _set_message_choice_dialog(self):
        self.current_message = self.whole_message[self.message_index]
        self.dialog_name = self.current_message[0]
        self.dialog_emotion = self.current_message[1]
        self.character.emotion = self.dialog_emotion
        self.dialog_type = self.current_message[2]
        self.character.dialog_type = self.current_message[2]
        if self.dialog_type == 'choices':
            self.choices = self.current_message[3]
            self.dialog_message = None
        elif self.dialog_type == 'dialog':
            self.dialog_message = self.current_message[3]
            self.choices = None
        
    def _reset_message_choice_dialog(self):
        self.whole_message.clear()
        self.current_message = None
        
        self.dialog_name = None
        self.dialog_emotion = None
        self.dialog_type = None
        self.character.dialog_type = None
        self.dialog_message = None
        self.message_index = 0
        
    def _get_advance_type(self):
        
        whole_message = self._get_dialog()
        if self.message_index + 1 < len(whole_message):
            current_message = whole_message[self.message_index + 1]
            type = current_message[1]
            
            return type
        else:
            return None
        
    def _get_dialog(self):
        oRet = self.dialog_data[enums.CNST_DATA_KEY_DEFAULT][enums.CNST_DATA_KEY_DIALOG]
        for key, value in self.dialog_data.items():
            if key == enums.CNST_DATA_KEY_DEFAULT:
                continue
            else:
                if value['condition']:
                    for condition in value['condition']:
                        condition_type = condition[0]
                        condition_value = condition[1]
                        if condition_type == 'stats':
                            stats = condition[2].split(' ')
                            stat_condition = stats[0]
                            stat_amount = stats[1]
                            
                            if stat_condition == '>' and self.character_data['stats'][condition_value] > int(stat_amount):
                                oRet = value[enums.CNST_DATA_KEY_DIALOG]
                                
        return oRet      
        
    def _chosen_effect(self, chosen):
        keylist = list(self.choices.keys())
        chosen = self.choices[keylist[chosen]]
        index = self.message_index + 1
        
        if chosen:
            
            for dialog in chosen['dialog']:
                self.whole_message.insert(index, dialog)
                index += 1
        
            for effect in chosen['effect']:
                type = effect[0]
                if type == 'stats':
                    stat = effect[1]
                    value_temp = effect[2]
                    
                    self.character.stats[stat] = self.character.stats[stat] + value_temp
                    
            self.dialog_type = enums.CNST_DATA_KEY_DIALOG
            self.character.dialog_type = enums.CNST_DATA_KEY_DIALOG
            self.choice_transition = True
        
        
    def _check_space_key(self):
        key = pygame.key.get_just_pressed()
        self.choice_transition = False
        if self.dialog_type == 'choices':
            if key[pygame.K_1]:
                self._chosen_effect(0)
            elif key[pygame.K_2]:
                self._chosen_effect(1)
                
            
        if key[pygame.K_SPACE] and state.STATE_COLLIDED_CHAR_MODE == enums.CNST_NPC_BUTTON_TYPE_TALK and self.dialog_type != 'choices' or self.choice_transition == True:
            self.choice_transition = False
            if hasattr(self, 'dialog_blit') and self.dialog_blit.animating == False:
                if self._get_advance_type() != 'choices' or self._get_advance_type() == None:
                    self.dialog_blit.kill()
                    del self.dialog_blit
                
            if hasattr(self, 'dialog_blit') and self.dialog_blit.animating:
                self.dialog_blit.skip_animation = True
            elif self.message_index < len(self.whole_message) - 1:
                self.message_index += 1
                self._set_message_choice_dialog()
                if self.dialog_type == 'dialog':
                    self.dialog_blit = DialogSpriteBlit(self.dialog_message, self.all_group)
                
            else:
                state.set_STATE_COLLIDED_CHAR_MODE(enums.CNST_NPC_BUTTON_TYPE_NONE)
                self._reset_message_choice_dialog()
                Button((self.npc_buttons_sprites), "Talk", enums.CNST_NPC_BUTTON_TYPE_TALK, (275, 510), self.character.talk)
                Button((self.npc_buttons_sprites), "Action", enums.CNST_NPC_BUTTON_TYPE_ACTION, (375, 510), self.character.action)
                Button((self.npc_buttons_sprites), "Inspect", enums.CNST_NPC_BUTTON_TYPE_INSPECT, (475, 510), self.character.inspect)
                self.kill()
                

    def update(self):
        self._check_space_key()
            

class DialogSpriteBlit(pygame.sprite.Sprite):
    def __init__(self, message, groups):
        super().__init__(groups)
        self.message = message
        
        self.font = pygame.font.Font(None, 30)
        self.surf = pygame.Surface((1070,300), pygame.SRCALPHA)
        self.surf.fill((0,0,0,0))
        
        self.image = self.surf
        self.rect = self.image.get_frect(bottomleft = (0, 720))
        
        self.start_time = time.time()
        self.letters_rendered = 0
        
        self.skip_animation = False
        self.animating = True
        
    def blit_dialog(self):
        self.text_surf_dialog = self.font.render(self.current_text if not self.skip_animation else self.message, False, (255, 255 ,255))
        self.surf.blit(self.text_surf_dialog, self.text_surf_dialog.get_frect(topleft = (280, 100)))
        self.image = self.surf
        
    def update(self):
        if not self.skip_animation:
            self.elapsed_time = time.time() - self.start_time
            self.letters_rendered = int(self.elapsed_time * TEXT_SPEED)
            self.current_text = self.message[:self.letters_rendered+1]
            self.blit_dialog()
            self.image = self.surf
            
            if self.letters_rendered > len(self.message):
                self.animating = False
                
        else:
            self.blit_dialog()
            self.image = self.surf
            self.animating = False