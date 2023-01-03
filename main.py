import utime
from pimoroni import Button
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_RGB332
from graphics import Graphics, Tile, Sprite, SpriteAnim

# set up the hardware
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, pen_type=PEN_RGB332, rotate=128)
display.set_backlight(1)

button_b = Button(13)
button_y = Button(15)

# load colors
BLACK = display.create_pen(0, 0, 0)

# load sprite
Graphics.load_spritesheet(display, "sprite.rgb332")
Graphics.set_size(3)

def comeuvas_sheet():
    spritesheet = []
    for i in range(4):
        spritesheet.append(Sprite([
            Tile(i * 2, 0, key_pen=BLACK),
            Tile(i * 2 + 1, 0, offset_x=8, key_pen=BLACK),
            Tile(i * 2, 1, offset_y=8, key_pen=BLACK),
            Tile(i * 2 + 1, 1, offset_x=8, offset_y=8, key_pen=BLACK)
        ]))
    spritesheet.append(spritesheet[2])
    spritesheet.append(spritesheet[1])

    return spritesheet

def campana_sheet():
    spritesheet = []
    for i in range(2):
        spritesheet.append(Sprite([
            Tile(12 + i * 2, 0, key_pen=BLACK),
            Tile(12 + i * 2 + 1, 0, offset_x=8, key_pen=BLACK),
            Tile(12 + i * 2, 1, offset_y=8, key_pen=BLACK),
            Tile(12 + i * 2 + 1, 1, offset_x=8, offset_y=8, key_pen=BLACK)
        ]))

    return spritesheet

def uva_verde_sheet():
    spritesheet = []
    for i in range(3):
        spritesheet.append(Sprite([
            Tile(8 + i * 2, 0)
        ]))
    
    return spritesheet

def uva_morada_sheet():
    spritesheet = []
    for i in range(3):
        spritesheet.append(Sprite([
            Tile(8 + i * 2, 1)
        ]))
    
    return spritesheet

last_ticks = utime.ticks_ms()
def screen_get_delta_time():
    global last_ticks

    current_ticks = utime.ticks_ms()
    delta_time = utime.ticks_diff(current_ticks, last_ticks) / 1000
    last_ticks = current_ticks

    return delta_time

def screen_clear():
    ''' Clears the screen with black color'''
    display.set_pen(BLACK)
    display.clear()
    
def screen_flip(wait: float = 1):
    ''' Updates display buffer and waits 1s'''
    display.update()
    utime.sleep(wait)

# get display size
w, h = display.get_bounds()

# player
comeuvas = SpriteAnim(comeuvas_sheet())
# bell
campana = SpriteAnim(campana_sheet(), time=1)


class Uva():
    def __init__(self):
        self.x = 0
        self.v = 176
        self.anim = SpriteAnim(uva_verde_sheet())
        self.anim.stop()

    def update(self, dt):
        self.x = self.x - self.v * dt
        if int(self.x) <= 37:
            self.x = 176 - (self.x - 37)
            return True
        
        return False

    def draw(self, display):
        global h
        self.anim.draw(display, int(self.x), int(h / 2 - self.anim.get_height() / 2))

uva = Uva()


while True:
    # get time since last screen update
    delta_time = screen_get_delta_time()

    # update sprites
    comeuvas.update(delta_time)
    if uva.update(delta_time):
        campana.set(campana.current + 1)

    # draw sprites
    screen_clear()

    uva.draw(display)
    comeuvas.draw(display, 16, int(h / 2 - comeuvas.get_height() / 2))
    campana.draw(display, w - campana.get_width() - 16, int(h / 2 - campana.get_height() / 2))

    screen_flip(1 / 10)
