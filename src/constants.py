from os.path import dirname, abspath

# file paths
PARENT_DIR = resDirectory = abspath(dirname(dirname(__file__))) + "/"
RES_DIR = PARENT_DIR + "res/"

# colors
BACKGROUND_COLOR = (228, 217, 255)
TEXT_COLOR = (48, 52, 63)

# sizes
BOARD_CELL_WIDTH = 120
BOARD_SPACING = 5