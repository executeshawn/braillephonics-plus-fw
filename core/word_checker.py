# core/word_checker.py

from core.braille_grid import update_tile, get_full_word
from core.word_validator import is_valid

class WordChecker:

    def __init__(self, feedback_manager):
        """
        feedback_manager: instance of FeedbackManager
        """
        self.feedback = feedback_manager

    def place_tile(self, row, col, letter):
        """
        Call this when a tile is placed on the board.
        Updates grid, forms current word, checks validity, triggers feedback.
        """
        # Update the 4x4 grid
        update_tile(row, col, letter)

        # Form current word from grid (left-to-right)
        word = get_full_word()

        # Check validity
        valid = is_valid(word)

        # Trigger feedback
        self.feedback.word_mode(word, valid)

        return word, valid

    def reset(self):
        """Optional: clear the letters/grid if needed"""
        from core.braille_grid import braille_grid
        for r in range(4):
            for c in range(4):
                braille_grid[r][c] = None