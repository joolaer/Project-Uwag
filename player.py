from settings import *

class Player(pygame.sprite.Sprite):
    
    def __init__(self, pos, direction, groups, collision_sprites, teleport_sprites):
        super().__init__(groups)
        self.init_direction = direction
        self.frame_index = 0
        self.load_images()
        self.image = pygame.image.load(join('media', 'animation', 'run', self._check_direction(self.init_direction), '0.png')).convert_alpha()
        self.rect = self.image.get_rect(midbottom = pos)
        self.hitbox_rect = self.rect.inflate(-40, 0)
        self.direction = pygame.Vector2()
        self.state = enums.CNST_STATE_IDLE
        self.collision_sprites = collision_sprites
        self.teleport_sprites = teleport_sprites
        
    def load_images(self):
        self.idle_frames = {'left': [], 'right': []}
        self.run_frames = {'left': [], 'right': []}
        
        for state in self.idle_frames.keys():
            for folder_path, sub_folders, file_names in walk (join('media', 'animation', 'idle', state)):
                if file_names:
                    for file_name in sorted(file_names, key= lambda name: int(name.split('.')[0])):
                        full_path = join(folder_path, file_name)
                        surf = pygame.image.load(full_path).convert_alpha()
                        self.idle_frames[state].append(surf)
            
        for state in self.run_frames.keys():
            for folder_path, sub_folders, file_names in walk (join('media', 'animation', 'run', state)):
                if file_names:
                    for file_name in sorted(file_names, key= lambda name: int(name.split('.')[0])):
                        full_path = join(folder_path, file_name)
                        surf = pygame.image.load(full_path).convert_alpha()
                        self.run_frames[state].append(surf)          
        
    def collision(self):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if self.direction.x > 0: self.hitbox_rect.right = sprite.rect.left
                if self.direction.x < 0: self.hitbox_rect.left = sprite.rect.right
                
    def teleport(self):
        for teleporter in self.teleport_sprites:
            if teleporter.rect.colliderect(self.hitbox_rect):
                self.hitbox_rect.x = teleporter.object['teleport_x']
    
    def input(self):
        key_pressed = pygame.key.get_pressed()
        
        if key_pressed[pygame.K_d] or key_pressed[pygame.K_a]:
            self.state = enums.CNST_STATE_RUN
            self.direction.x = int(key_pressed[pygame.K_d] - key_pressed[pygame.K_a])
            self.direction = self.direction.normalize() if self.direction else self.direction
            
            if int(self.direction.x) == enums.CNST_DIRECTION_LEFT:
                self.init_direction = enums.CNST_DIRECTION_LEFT
            elif int(self.direction.x) == enums.CNST_DIRECTION_RIGHT:
                self.init_direction = enums.CNST_DIRECTION_RIGHT
        else:
            self.state = enums.CNST_STATE_IDLE
            self.direction.x = 0
        
        self.hitbox_rect.x += self.direction.x * PLAYER_RUN_SPEED
        #self.teleport()
        self.collision()
        self.rect.center = self.hitbox_rect.center
                
    def _check_direction(self, direction):
        if int(direction) == enums.CNST_DIRECTION_RIGHT:
            return 'right'
        elif int(direction) == enums.CNST_DIRECTION_LEFT:
            return 'left'
            
    def animate(self):
        
        self.frame_index = self.frame_index + .3 if self.direction else self.frame_index + .1
        
        if self.state == enums.CNST_STATE_IDLE:
            self.image = self.idle_frames[self._check_direction(self.init_direction)][int(self.frame_index) % len(self.idle_frames[self._check_direction(self.init_direction)])]
        elif self.state == enums.CNST_STATE_RUN:
            self.image = self.run_frames[self._check_direction(self.init_direction)][int(self.frame_index) % len(self.run_frames[self._check_direction(self.init_direction)])]
            
    def update(self):
        self.input()
        self.animate()