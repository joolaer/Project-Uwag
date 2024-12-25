from settings import *
from character_data import TIME_DATA, DAY_DATA
from button import BorderedButton

class GameTime:
    
    def __init__(self, game, groups) -> None:
        self.game = game
        self.groups = groups
        
        #Time
        self.current_time = DisplayTime(self.groups, state.current_time)
        
        #Day
        self.day = enums.CNST_GAME_DAY_SUNDAY
        self.current_day = DisplayDate(self.groups, state.current_day)

        print(f"{state.STATE_COLLIDED_CHAR}")
    
    def _transition_time(self):
        state.available_action = state.action_cap

        if state.current_time == enums.CNST_GAME_TIME_NIGHT:
            self._sleep()
            return
        
        if state.current_time == enums.CNST_GAME_TIME_MORNING:
            state.set_current_time(enums.CNST_GAME_TIME_NOON)
        elif state.current_time == enums.CNST_GAME_TIME_NOON:
            state.set_current_time(enums.CNST_GAME_TIME_AFTERNOON)
        elif state.current_time == enums.CNST_GAME_TIME_AFTERNOON:
            state.set_current_time(enums.CNST_GAME_TIME_EVENING)
        elif state.current_time == enums.CNST_GAME_TIME_EVENING:
            state.set_current_time(enums.CNST_GAME_TIME_NIGHT)
        
        self.game.update_character_location()
        state.apply_buff_time_delay()
        self.current_time.kill()
        self.current_time = DisplayTime(self.groups, state.current_time)
        
    def decrement_available_action(self, amount):
        state.set_available_action(state.available_action - amount)
            
        if state.available_action < 1:
            self._transition_time()
            
    def increment_available_action(self, amount):
        if (state.available_action + amount ) > state.action_cap:
            state.set_available_action(state.action_cap)
        else:
            state.set_available_action(state.available_action + amount)
            
    def _sleep(self):
        state.set_current_time(enums.CNST_GAME_TIME_MORNING)

        if state.current_day == 6:
            state.set_current_day(0)
        else: 
            state.set_current_day(state.current_day + 1)
        self.game.update_character_location()
        state.apply_buff_date_delay()
        state.apply_buff_time_delay()
        self.current_day.kill()
        self.current_time.kill()
        self.current_time = DisplayTime(self.groups, state.current_time)
        self.current_day = DisplayDate(self.groups, state.current_day)
            
        
    def check_available_action(self):
        if state.available_action < 1:
            self._transition_time()

    def check_time_buttons(self):
        if not state.STATE_COLLIDED_CHAR:
            if not hasattr(self, 'rest_button') and not hasattr(self, 'sleep_button'):
                self.rest_button = BorderedButton(self.groups, 'Rest', (100,600), self._transition_time, 
                                        ('grey', 'white', 'black'), ('black', 'grey', 'white'), (100,50))
                self.sleep_button = BorderedButton(self.groups, 'Sleep', (100,660), self._sleep, 
                                        ('grey', 'white', 'black'), ('black', 'grey', 'white'), (100,50))
        else:
            if hasattr(self, 'rest_button') and hasattr(self, 'sleep_button'):
                self.rest_button.kill()
                self.sleep_button.kill()
                del self.rest_button
                del self.sleep_button

    def update(self):
        self.check_time_buttons()
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

