from settings import *
from character_data import CHARACTER_DATA
from dialog_data import DIALOG_DATA
from helpers import *
import time

class DialogSprite(pygame.sprite.Sprite):
    def __init__(self, character, name, filename, groups):
        super().__init__(groups)
        self.character = character
        self.name = name
        self.filename = filename
        
        self.character_data = CHARACTER_DATA[self.filename]
        self.face_frames = self.character_data[enums.CNST_DATA_KEY_FACE]
        self.dialog_data = DIALOG_DATA[self.filename]
        self.whole_message = self._get_dialog()
        self.first_message = self.whole_message[0]
        
        self.message_split = self.first_message.split('<>')    
        self.emotion = self.message_split[0]
        self.choices = self.message_split[1]
        self.message = self.message_split[2]
        
        self.face_index = 0
        self.message_index = 0
        self.letters_rendered = 0
        
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
        print(self.face_index)
        self.current_face_frame = self.face_frames[self.emotion][int(self.face_index) % len(self.face_frames[self.emotion])]
        self.surf.blit(self.current_face_frame, self.current_face_frame.get_frect(topleft = (0,0)))
        self.surf.blit(self.text_surf_name, self.text_surf_name.get_frect(center = (130, 280)))
        
    def blit_dialog(self):
        self.text_surf_dialog = self.font.render(self.current_text if not self.skip_animation else self.message, False, (255, 255 ,255))
        self.surf.blit(self.text_surf_dialog, self.text_surf_dialog.get_frect(topleft = (280, 100)))
        self.image = self.surf
        
    def _check_space_key(self):
        key = pygame.key.get_just_pressed()
        self.elapsed_time = time.time() - self.start_time
        self.letters_rendered = int(self.elapsed_time * TEXT_SPEED)
        
        if key[pygame.K_SPACE] and helper_dialog.get_dialogue_mode():
            
            if self.letters_rendered < len(self.message):
                self.skip_animation = True
            else:
                self.skip_animation = False
                self.message_index += 1
                self.elapsed_time = 0
            
        
    def update(self):
        self.animate_face()
        self._check_space_key()
        self.blit_dialog()
        if not self.skip_animation:            
            if self.letters_rendered > len(self.message):
                self.skip_animation = False
        else:
            self.blit_dialog()
            self.animating = False
        
        