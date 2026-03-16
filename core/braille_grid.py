# core/braille_grid.py

braille_grid = [[None]*4 for _ in range(4)]

def update_tile(row, col, letter):
    braille_grid[row][col] = letter

def get_row_word(row_index):
    return ''.join([letter if letter else '' for letter in braille_grid[row_index]])

def get_full_word():
    return ''.join([letter if letter else '' for row in braille_grid for letter in row if letter])