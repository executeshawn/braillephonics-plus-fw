# core/mode_manager.py

from core.braille_grid import update_tile, get_full_word
from core.word_checker import WordChecker

class ModeManager:

    LETTER_MODE = 1
    PHONICS_MODE = 2
    WORD_MODE = 3

    def __init__(self, feedback_manager):
        self.current_mode = self.LETTER_MODE
        self.feedback_manager = feedback_manager
        self.word_checker = WordChecker(feedback_manager)

    def set_mode(self, mode):
        self.current_mode = mode

    def get_mode(self):
        return self.current_mode

    def handle_tile_placement(self, row, col, letter):
        """
        Call this whenever a tile is placed.
        Handles feedback depending on current mode.
        """
        mode = self.current_mode

        if mode == self.LETTER_MODE:
            self.feedback_manager.letter_mode(letter)
        elif mode == self.PHONICS_MODE:
            self.feedback_manager.phonics_mode(letter)
        elif mode == self.WORD_MODE:
            word, valid = self.word_checker.place_tile(row, col, letter)
            # word_checker already triggers feedback
            return word, valid