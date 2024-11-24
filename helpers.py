class Helper_Dialog:
    def __init__(self):
        self.dialogue_mode = False
        self.person_1 = None
        self.person_2 = None
        
    def get_dialogue_mode(self):
        return self.dialogue_mode
    
    def set_dialogue_mode(self, value):
        self.dialogue_mode = value
        #self.person_1 = 'Johan'
        #self.person_2 = person_2
        
    def set_dialogue_mode_diff_person(self, person_1, person_2):
        self.dialogue_mode = True
        self.person_1 = person_1
        self.person_2 = person_2
        
    def reset_dialogue_mode(self):
        self.dialogue_mode = False
        self.person_1 = None
        self.person_2 = None