from settings import *
from character_data import CHARACTER_DATA
from dialog_data import DIALOG_DATA
from helpers import *
import time
import copy

class DialogSprite(pygame.sprite.Sprite):
    def __init__(self, character, name, filename, all_group):
        super().__init__(all_group)
        print(f'DIALOG_DATA {DIALOG_DATA}')
        self.character = character
        self.name = name
        self.filename = filename
        self.all_group = all_group
        
        self.character_data = CHARACTER_DATA[self.filename]
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
        
        
        self.current_face_frame = self.face_frames[self.emotion][0].convert_alpha()
        self.text_surf_name = self.font.render(self.name, False, (255, 15 ,15))
        self.surf = pygame.Surface((1070,300), pygame.SRCALPHA)
        self.surf.fill((0,0,0,0))
        
        
        self.image = self.surf
        self.rect = self.image.get_frect(bottomleft = (0, 720))
        
        self.skip_animation = False
        self.animating = True
        
        self.surf.blit(self.current_face_frame, self.current_face_frame.get_frect(topleft = (0,0)))
        self.surf.blit(self.text_surf_name, self.text_surf_name.get_frect(center = (130, 280)))
        
        self.dialog_blit = DialogSpriteBlit(self.message, self.all_group)
        
    def _set_message_choice_dialog(self):
        print(self.whole_message)
        print(self.message_index)
        self.current_message = self.whole_message[self.message_index]
        split = self.current_message.split('<>')
        
        self.emotion = split[0]
        self.type = split[1]
        self.message = split[2]
        
    def _reset_message_choice_dialog(self):
        self.whole_message.clear()
        self.current_message = None
        
        self.emotion = None
        self.type = None
        self.message = None
        self.message_index = 0
        
    def _get_advance_type(self):
        
        whole_message = self._get_dialog()
        if self.message_index + 1 < len(whole_message):
            current_message = whole_message[self.message_index + 1]
            split = current_message.split('<>')
            
            return split[1]
        else:
            return None
        
    def _get_dialog(self):
        oRet = self.dialog_data[enums.CNST_DATA_KEY_DEFAULT][enums.CNST_DATA_KEY_DIALOG]
        for key, value in self.dialog_data.items():
            if key == enums.CNST_DATA_KEY_DEFAULT:
                continue
            else:
                if value['condition']:
                    for child_key, child_value in value['condition'].items():
                        condition = child_key.split('<>')
                        condition_type = condition[0]
                        condition_value = condition[1]
                        if condition_type == 'stats':
                            stats = child_value.split(' ')
                            stat_condition = stats[0]
                            stat_amount = stats[1]
                            
                            if stat_condition == '>' and self.character_data['stats'][condition_value] > int(stat_amount):
                                oRet = value[enums.CNST_DATA_KEY_DIALOG]
                                
        return oRet      
        
    def animate_face(self):
        self.face_index = self.face_index + .1
        self.current_face_frame = self.face_frames[self.emotion][int(self.face_index) % len(self.face_frames[self.emotion])]
        self.surf.blit(self.current_face_frame, self.current_face_frame.get_frect(topleft = (0,0)))
        self.surf.blit(self.text_surf_name, self.text_surf_name.get_frect(center = (130, 280)))
        
    def _set_choices(self):
        choices = []
        split = self.current_message.split('<>')
        for choice in split[2].split('()'):
            choices.append(choice.split('[]'))
            
        self.choices = choices
        
    def _chosen_effect(self, chosen):
        chosen = self.choices[chosen]
        dialogs = RESPONSE_DATA[chosen[1]][enums.CNST_DATA_KEY_DIALOG]
        effect = RESPONSE_DATA[chosen[1]][enums.CNST_DATA_KEY_EFFECT]
        for dialog in dialogs:
            self.whole_message.append(dialog)
        
        for key, value in effect.items():
            split_key = key.split('<>')
            split_value = value.split(' ')
            type = split_key[0]
            if type == 'stats':
                stat = split_key[1]
                value_temp = int(split_value[1])
                operrand = split_value[0]
                
                if operrand == '-':
                    self.character.stats[stat] = self.character.stats[stat] - value_temp
                elif operrand == '+':
                    self.character.stats[stat] = self.character.stats[stat] + value_temp
                    
        self.type = enums.CNST_DATA_KEY_DIALOG
        self.choice_transition = True
        
        
    def _check_space_key(self):
        key = pygame.key.get_just_pressed()
        self.choice_transition = False
        if self.type == 'choices':
            self._set_choices()
            if key[pygame.K_1]:
                self._chosen_effect(0)
            elif key[pygame.K_2]:
                self._chosen_effect(1)
                
            
        if key[pygame.K_SPACE] and helper_dialog.get_dialogue_mode() and self.type != 'choices' or self.choice_transition == True:
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
                if self.type == 'dialog':
                    self.dialog_blit = DialogSpriteBlit(self.message, self.all_group)
                
            else:
                helper_dialog.set_dialogue_mode(False)
                self._reset_message_choice_dialog()
                self.kill()
                

    def update(self):
        self.animate_face()
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