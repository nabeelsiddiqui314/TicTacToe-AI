from os.path import dirname, abspath

# file paths
PARENT_DIR = resDirectory = abspath(dirname(dirname(__file__))) + "/"
RES_DIR = PARENT_DIR + "res/"

# colors
BACKGROUND_COLOR = (228, 217, 255)
TITLE_TEXT_COLOR = (39, 52, 105)
BUTTON_TEXT_COLOR = (250, 250, 255)
TEXT_COLOR = BUTTON_TEXT_COLOR
BUTTON_COLOR = (48, 52, 63)
BUTTON_HIGHLIGHT_COLOR = (149, 151, 159)

# sizes
TITLE_FONT_SIZE = 64
REGULAR_FONT_SIZE = 32

BOARD_CELL_WIDTH = 120
BOARD_SPACING = 5