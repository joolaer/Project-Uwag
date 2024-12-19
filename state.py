

class State:
    
    def __init__(self) -> None:
        self.STATE_COLLIDED_CHAR_MODE = 0
        self.STATE_COLLIDED_CHAR = None
        self.buff = []
        self.buff_time_delay = []
        self.buff_date_delay = []
        self.unlocked_buff = []
        
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