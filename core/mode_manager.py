class ModeManager:

    LETTER_MODE = 1
    PHONICS_MODE = 2
    WORD_MODE = 3

    def __init__(self):

        self.current_mode = self.LETTER_MODE

    def set_mode(self, mode):

        self.current_mode = mode

    def get_mode(self):

        return self.current_mode