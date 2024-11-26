from settings import *
from character_data import CHARACTER_DATA
import copy

class Face(pygame.sprite.Sprite):
    def __init__(self, groups, character):
        super().__init__(groups)
        self.character = character
        self.name = self.character.name
        self.file_name = self.character.file_name
        self.emotion = self.character.emotion
        
        self.face_frames = copy.deepcopy(CHARACTER_DATA[self.file_name][enums.CNST_DATA_KEY_FACE])
        self.font = pygame.font.Font(None, 30)
        self.name_text = self.font.render(self.name, False, (255,255,255))
        
        self.surf = pygame.Surface((256,300), pygame.SRCALPHA)
        self.surf.fill((0,0,0,0))
        
        self.image = self.surf
        self.rect = self.image.get_frect(bottomleft = (0, 720))
        
        self.surf.blit(self.name_text, self.name_text.get_frect(center = (128, 280)))
        
        
    def animate_face(self):
        if state.STATE_COLLIDED_CHAR_MODE == enums.CNST_NPC_BUTTON_TYPE_TALK:
            self.face_index = self.face_index + .1
            self.current_face_frame = self.face_frames[self.emotion][int(self.face_index) % len(self.face_frames[self.emotion])]
        else:
            self.current_face_frame = self.face_frames[self.emotion][0]
        self.surf.blit(self.current_face_frame, self.current_face_frame.get_frect(topleft = (0,0)))
        
    def update(self):
        self.animate_face()