

class State:
    
    def __init__(self) -> None:
        self.STATE_COLLIDED_CHAR_MODE = 0
        self.STATE_COLLIDED_CHAR = None
        
    def set_STATE_COLLIDED_CHAR_MODE(self, value):
        self.STATE_COLLIDED_CHAR_MODE = value
    
    def reset_STATE_COLLIDED_CHAR_MODE(self):
        self.STATE_COLLIDED_CHAR_MODE = 0
        
    def set_STATE_COLLIDED_CHAR(self, value):
        self.STATE_COLLIDED_CHAR = value