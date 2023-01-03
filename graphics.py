SPRITE_NAME = 'sprite.rgb332'


class Graphics():
    '''
    Representa un grafico abstracto
    '''

    size = 1

    @classmethod
    def set_size(cls, size: int = 1):
        '''
        Cambia el tamaño en el que se dibujan los graficos
        '''

        cls.size = size

    @classmethod
    def load_spritesheet(cls, display, name = SPRITE_NAME):
        '''
        Carga un spritesheet en RAM
        '''

        display.load_spritesheet(name)


    def get_width(self):
        '''
        Obtiene el ancho del grafico
        '''

        pass


    def get_height(self):
        '''
        Obtiene el alto del grafico
        '''

        pass


    def draw(self, display, x: int, y: int):
        '''
        Dibuja el grafico
        '''

        pass


class Tile(Graphics):
    '''
    Representa un cuadro dentro del spritesheet
    '''

    def __init__(self, row: int, column: int, offset_x: int = 0, offset_y: int = 0, key_pen = -1):
        self.row = row
        self.col = column
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.key_pen = key_pen


    def get_width(self):
        '''
        Obtiene el ancho del cuadro
        '''

        return 8 * Graphics.size


    def get_height(self):
        '''
        Obtiene el alto del cuadro
        '''

        return 8 * Graphics.size


    def draw(self, display, x: int, y: int):
        '''
        Dibuja el cuadro
        '''

        display.sprite(self.row, self.col, x + self.offset_x * Graphics.size, y + self.offset_y * Graphics.size, Graphics.size, self.key_pen)


class Sprite(Graphics):
    '''
    Define un sprite cogiendo cuadros del spritesheet
    '''

    def __init__(self, tileset: list[Tile]):
        self.tileset = tileset


    def get_width(self):
        '''
        Obtiene el ancho del sprite
        '''

        acc = 0
        max_offset = 0

        for tile in self.tileset:
            max_offset = tile.offset_x
            if tile.offset_x >= max_offset:
                acc = tile.offset_x * Graphics.size + tile.get_width()

        return acc


    def get_height(self):
        '''
        Obtiene el alto del sprite
        '''

        acc = 0
        max_offset = 0

        for tile in self.tileset:
            if tile.offset_y >= max_offset:
                max_offset = tile.offset_y
                acc = tile.offset_y * Graphics.size + tile.get_width()

        return acc


    def draw(self, display, x: int, y: int):
        '''
        Dibuja el sprite
        '''

        for tile in self.tileset:
            tile.draw(display, x, y)


class SpriteAnim():
    '''
    Representa una animacion
    '''

    def __init__(self, sheet: list[Sprite], time = 0.1):
        self.sheet = sheet
        self.current = 0
        self.playing = True
        self.reverse = False
        self.time = time
        self.dt = 0

    def get_width(self):
        '''
        Obtiene el ancho de la animacion
        '''

        max_width = 0

        for sprite in self.sheet:
            if max_width < sprite.get_width():
                max_width = sprite.get_width()

        return max_width

    def get_height(self):
        '''
        Obtiene el alto de la animacion
        '''

        max_height = 0

        for sprite in self.sheet:
            if max_height < sprite.get_height():
                max_height = sprite.get_height()

        return max_height
    
    def update(self, dt: float):
        '''
        Actualiza la animacion usando un delta time en segundos
        '''

        if self.playing:
            if dt < 0 or self.reverse:
                self.dt = self.dt - abs(dt)

                if self.dt <= 0:
                    self.dt = self.time - self.dt
                    self.current -= 1

                    if self.current == 0:
                        self.current = len(self.sheet)
            elif dt > 0 or not self.reverse:
                self.dt = self.dt + abs(dt)

                if self.dt >= self.time:
                    self.dt = 0
                    self.current += 1

                    if self.current == len(self.sheet):
                        self.current = 0

    def play(self):
        '''
        Pone la animacion a correr
        '''

        self.playing = True

    def pause(self):
        '''
        Para de actualizar la animacion
        '''

        self.playing = False

    def set(self, sprite):
        '''
        Establece el frame actual de la animacion
        '''

        self.current = sprite % len(self.sheet)

    def reset(self):
        '''
        Reinicia la animacion (sin pausarla)
        '''

        self.set(0)

    def stop(self):
        '''
        Detiene la animacion y la reinicia
        '''

        self.pause()
        self.reset()

    def rewind(self):
        '''
        Pone la animacion a correr hacia el lado contrario
        '''

        self.reverse = not self.reverse
        return self.reverse

    def draw(self, display, x: int, y: int):
        '''
        Dibuja la animacion
        '''

        current_sprite = self.sheet[self.current]
        current_sprite.draw(display, x, y)
