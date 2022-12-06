# game setup
WIDTH = 1080
HEIGTH = 680
FPS = 60
TILESIZE = 64

# camera and player speed
SMOOTH_SPEED = 0.07
PLAYER_SPEED = 5
PLAYER_ANIMATION_SPEED = 0.15

# UI
BAR_HEIGHT = 26
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = "../graphics/font/joystix.ttf"
UI_FONT_SIZE = 18

# general colours
WATER_COLOUR = '#71DDEE'
UI_BG_COLOUR = '#222222'
UI_BORDER_COLOUR = '#111111'
TEXT_COLOUR = '#EEEEEE'

# UI colours
HEALTH_COLOUR = 'red'
ENERGY_COLOUR = 'chartreuse3'
UI_BORDER_COLOUR_ACTIVE = 'gold'

WEAPON_DATA = {
    'sword': {
        'cooldown': 100,
        'damage': 15,
        'graphic': '../graphics/weapons/sword/full.png'},
    'lance': {
        'cooldown': 400,
        'damage': 30,
        'graphic': '../graphics/weapons/lance/full.png'},
    'axe': {
        'cooldown': 300,
        'damage': 20,
        'graphic': '../graphics/weapons/axe/full.png'},
    'rapier': {
        'cooldown': 50,
        'damage': 8,
        'graphic': '../graphics/weapons/rapier/full.png'},
    'sai': {
        'cooldown': 80,
        'damage': 10,
        'graphic': '../graphics/weapons/sai/full.png'}}
