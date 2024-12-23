from settings import *
from character_data import TIME_DATA, DAY_DATA
from button import BorderedButton

class GameTime:
    
    def __init__(self, groups) -> None:
        self.groups = groups
        self.available_action = 3
        self.action_cap = 3
        
        #Time
        self.point_of_time = enums.CNST_GAME_TIME_MORNING
        self.current_time = DisplayTime(self.groups, self.point_of_time)
        
        #Day
        self.day = enums.CNST_GAME_DAY_SUNDAY
        self.current_day = DisplayDate(self.groups, self.day)

        self.button = BorderedButton(self.groups, 'Rest', (100,100), self._transition_time, 
                                     ('grey', 'white', 'black'), ('black', 'grey', 'white'), (100,50))
        self.button = BorderedButton(self.groups, 'Sleep', (100,160), self._sleep, 
                                     ('grey', 'white', 'black'), ('black', 'grey', 'white'), (100,50))
    
    def _transition_time(self):
        self.available_action = self.action_cap

        if self.point_of_time == enums.CNST_GAME_TIME_NIGHT:
            self._sleep()
            return
        
        if self.point_of_time == enums.CNST_GAME_TIME_MORNING:
            self.point_of_time = enums.CNST_GAME_TIME_NOON
        elif self.point_of_time == enums.CNST_GAME_TIME_NOON:
            self.point_of_time = enums.CNST_GAME_TIME_AFTERNOON
        elif self.point_of_time == enums.CNST_GAME_TIME_AFTERNOON:
            self.point_of_time = enums.CNST_GAME_TIME_EVENING
        elif self.point_of_time == enums.CNST_GAME_TIME_EVENING:
            self.point_of_time = enums.CNST_GAME_TIME_NIGHT
        
        state.apply_buff_time_delay()
        self.current_time.kill()
        self.current_time = DisplayTime(self.groups, self.point_of_time)
        
    def decrement_available_action(self, amount):
        self.available_action -= amount
            
        if self.available_action < 1:
            self._transition_time()
            
    def increment_available_action(self, amount):
        if (self.available_action + amount ) > self.action_cap:
            self.available_action = self.action_cap
        else:
            self.available_action += amount
            
    def _sleep(self):
        self.point_of_time = enums.CNST_GAME_TIME_MORNING

        if self.day == 6:
            self.day = 0
        else: 
            self.day += 1
        state.apply_buff_date_delay()
        state.apply_buff_time_delay()
        self.current_day.kill()
        self.current_time.kill()
        self.current_time = DisplayTime(self.groups, self.point_of_time)
        self.current_day = DisplayDate(self.groups, self.day)
            
        
    def check_available_action(self):
        if self.available_action < 1:
            self._transition_time()
    
    def update(self):
        self.check_available_action()
        
class DisplayTime(pygame.sprite.Sprite):
    def __init__(self, groups, point_of_time) -> None:
        super().__init__(groups)
        
        self.point_of_time = point_of_time
        
        self.time_data = deepcopy(TIME_DATA['text'])
        self.font = pygame.font.Font(None, 24)
        self.time_text = self.font.render(self.time_data[self.point_of_time], False, (255,255,255))
        
        self.surf = pygame.Surface((110,32), pygame.SRCALPHA)
        self.surf.fill((0,0,0,0))
        self.surf.blit(self.time_text, self.time_text.get_frect(center = (50,16)))
        
        self.image = self.surf
        self.rect = self.image.get_frect(topright = (WINDOW_WIDTH, 0))

class DisplayDate(pygame.sprite.Sprite):
    def __init__(self, groups, date) -> None:
        super().__init__(groups)
        
        self.date = date
        
        self.date_data = deepcopy(DAY_DATA['text'])
        self.font = pygame.font.Font(None, 24)
        self.date_text = self.font.render(self.date_data[self.date], False, (255,255,255))
        
        self.surf = pygame.Surface((110,32), pygame.SRCALPHA)
        self.surf.fill((0,0,0,0))
        self.surf.blit(self.date_text, self.date_text.get_frect(center = (50,16)))
        
        self.image = self.surf
        self.rect = self.image.get_frect(topright = (WINDOW_WIDTH - 70, 0))

