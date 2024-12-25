from settings import *

class State:
    
    def __init__(self) -> None:
        self.STATE_COLLIDED_CHAR_MODE = 0
        self.STATE_COLLIDED_CHAR = None
        self.current_location = enums.CNST_GAME_LOCATION_STREET_GHETTO
        self.current_location_max_border = -1020
        self.current_location_min_border = 0

        #Buff
        self.buff = []
        self.buff_time_delay = []
        self.buff_date_delay = []
        self.unlocked_buff = []

        #Game Time
        self.available_action = 3
        self.action_cap = 3
        self.current_time = enums.CNST_GAME_TIME_MORNING
        self.current_day = enums.CNST_GAME_DAY_SUNDAY
        
    def set_available_action(self, value):
        self.available_action = value

    def set_action_cap(self, value):
        self.action_cap = value

    def set_current_time(self, value):
        self.current_time = value

    def set_current_day(self, value):
        self.current_day = value

    def set_current_location(self, value):
        self.current_location = value

    def set_current_location_border(self, max, min):
        self.current_location_max_border = max
        self.current_location_min_border = min

    def set_STATE_COLLIDED_CHAR_MODE(self, value):
        self.STATE_COLLIDED_CHAR_MODE = value
    
    def reset_STATE_COLLIDED_CHAR_MODE(self):
        self.STATE_COLLIDED_CHAR_MODE = 0
        
    def set_STATE_COLLIDED_CHAR(self, value):
        self.STATE_COLLIDED_CHAR = value

    def apply_buff_time_delay(self):
        for buff in self.buff_time_delay:
            if buff not in self.buff:
                self.buff.append(buff)
        self.buff_time_delay = []
    
    def apply_buff_date_delay(self):
        for buff in self.buff_date_delay:
            if buff not in self.buff:
                self.buff.append(buff)
        self.buff_date_delay = []
    
    def add_buff_time_delay(self, value):
        self.buff_time_delay.append(value)

    def add_buff_date_delay(self, value):
        self.buff_date_delay.append(value)

    def immediate_buff(self, value):
        self.buff.append(value)

    def get_buffs(self):
        return self.buff[:]
    
    def remove_buff(self, value):
        if value in self.buff:
            self.buff.remove(value)
            self.remove_buff.append(value)