from settings import *
from character_data import CHARACTER_DATA, CHARACTER_DIALOG_COLOR
from dialog_data import DIALOG_DATA
from button import Button, ChoicesButton

import time
import copy

class DialogSprite(pygame.sprite.Sprite):
    def __init__(self, character, game_time, name, filename, all_group, npc_buttons_sprites):
        super().__init__(all_group)
        self.character = character
        self.game_time = game_time
        self.name = name
        self.filename = filename
        self.all_group = all_group
        self.screen = pygame.display.get_surface()
        self.choices_group = pygame.sprite.Group()
        self.npc_buttons_sprites = npc_buttons_sprites
        
        self.character_data = copy.deepcopy(CHARACTER_DATA[self.filename])
        self.face_frames = self.character_data[enums.CNST_DATA_KEY_FACE]
        self.dialog_data = copy.deepcopy(DIALOG_DATA[self.filename])
        
        self.face_index = 0
        self.message_index = 0
        self.letters_rendered = 0
        self.dialog_space_key = False
        self.has_choices = False
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

        
        self.dialog_blit = DialogSpriteBlit(self.dialog_message, self.dialog_name, self.all_group)

        self.effect_types = {
            'stats': self.effect_type_stats,
            'action': self.effect_type_actions,
            'buff-add': self.effect_type_buff_add,
            'buff-remove': self.effect_type_buff_remove
        }
        
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
                            stat_amount = int(stats[1])
                            if stat_condition == '>' and self.character.stats[condition_value] > stat_amount:
                                oRet = value[enums.CNST_DATA_KEY_DIALOG]
                                
        return oRet      
        
    def _chosen_effect(self, chosen_key):
        chosen = self.choices[chosen_key]
        index = self.message_index + 1
        
        if chosen:
            
            for dialog in chosen['dialog']:
                self.whole_message.insert(index, dialog)
                index += 1
        
            for effect in chosen['effect']:
                type = effect[0]

                self.effect_types.get(type, self.effect_type_default)(effect)
                
            self.dialog_type = enums.CNST_DATA_KEY_DIALOG
            self.character.dialog_type = enums.CNST_DATA_KEY_DIALOG
            self.reset_choices()
            self.render_dialog()

    def effect_type_stats(self, effect):
        stat = effect[1]
        value_temp = effect[2]
        self.character.stats[stat] = self.character.stats[stat] + value_temp

    def effect_type_actions(self, effect):
        self.action_effect = effect
        
    def activate_action_effect(self):
        action = self.action_effect[1]
        value = self.action_effect[2]
        if action == "decrease":
            self.game_time.decrement_available_action(value)
        elif action == "increase":
            self.game_time.increment_available_action(value)

    def effect_type_buff_add(self, effect):
        action = effect[1]
        value = effect[2]

        if action == 'date':
            state.add_buff_date_delay(value)
        elif action == 'time':
            state.add_buff_time_delay(value)
        else:
            state.immediate_buff(value
                                 )
    def effect_type_buff_remove(self, effect):
        state.remove_buff(effect[2])
    def effect_type_default(self, effect):
        pass
            
    def render_choices(self):
        y_pos = 100
        self.has_choices = True
        choices = self.current_message[3].keys()
        for choice in choices: 
            ChoicesButton((self.all_group, self.choices_group), choice, y_pos, self)
            y_pos += 60
        
    def reset_choices(self):
        self.has_choices = False
        self.choices = None
        for sprite in self.choices_group:
            sprite.kill()
        
        
    def _check_space_key(self):
        key = pygame.key.get_just_pressed()
        self.choice_transition = False
        if self.dialog_type == 'choices' and self.has_choices == False:
            self.render_choices()
            
        if key[pygame.K_SPACE] and state.STATE_COLLIDED_CHAR_MODE == enums.CNST_NPC_BUTTON_TYPE_TALK and self.dialog_type == enums.CNST_DATA_KEY_DIALOG:
            self.render_dialog()
            
    def render_dialog(self):
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
                self.dialog_blit = DialogSpriteBlit(self.dialog_message, self.dialog_name, self.all_group)
            
        else:
            if hasattr(self, 'action_effect'):
                self.activate_action_effect()
            state.set_STATE_COLLIDED_CHAR_MODE(enums.CNST_NPC_BUTTON_TYPE_NONE)
            self._reset_message_choice_dialog()
            Button((self.npc_buttons_sprites), "Talk", enums.CNST_NPC_BUTTON_TYPE_TALK, (275, 510), self.character.talk)
            Button((self.npc_buttons_sprites), "Action", enums.CNST_NPC_BUTTON_TYPE_ACTION, (375, 510), self.character.action)
            Button((self.npc_buttons_sprites), "Inspect", enums.CNST_NPC_BUTTON_TYPE_INSPECT, (475, 510), self.character.inspect)
            self.kill()
            self.character.remove_dialog()
                
    def _check_if_talking(self):
        if self.dialog_name:
            if self.dialog_name.lower() == self.filename:
                self.character.talking = True
            else: 
                self.character.talking = False

    def update(self):
        self._check_space_key()
        self._check_if_talking()
        
            
            

class DialogSpriteBlit(pygame.sprite.Sprite):
    def __init__(self, message, name ,groups):
        super().__init__(groups)
        self.message = message
        self.name = name
        
        self.font_color = self.get_font_color()
        self.font = pygame.font.Font(None, 30)
        self.get_font()
        
        self.surf = pygame.Surface((1070,300), pygame.SRCALPHA)
        self.surf.fill((0,0,0,0))
        self.image = self.surf
        self.rect = self.image.get_frect(bottomleft = (0, 720))
        
        self.start_time = time.time()
        self.letters_rendered = 0
        
        self.skip_animation = False
        self.animating = True
        
    def get_font_color(self):
        return deepcopy(CHARACTER_DIALOG_COLOR[self.name])
        
    def blit_dialog(self):
        self.text_surf_dialog = self.font.render(self.current_text if not self.skip_animation else self.message, False, self.font_color)
        self.surf.blit(self.text_surf_dialog, self.text_surf_dialog.get_frect(topleft = (280, 100)))
        self.image = self.surf
        
    def update(self):
        if not self.skip_animation:
            self.elapsed_time = time.time() - self.start_time
            self.letters_rendered = int(self.elapsed_time * TEXT_SPEED)
            self.current_text = self.message[:self.letters_rendered+1]
            self.blit_dialog()
            
            if self.letters_rendered > len(self.message):
                self.animating = False
                
        else:
            self.blit_dialog()
            self.animating = False
    
    def get_font(self):
        first_letter = self.message[0]
        if first_letter == '/':
            self.font.italic = True
            self.message = self.message[1:]
        elif first_letter == '*':
            self.font.bold = True
            self.message = self.message[1:]