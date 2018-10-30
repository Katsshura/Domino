class Peca_Domino:
    def __init__(self, top, bottom):
        self._next = None
        self._previous = None
        self._value = [top, bottom]
        self._sprite = None

    def get_next(self):
        return self._next

    def get_previous(self):
        return self._previous

    def get_value(self):
        return self._value

    def set_next(self, next):
        self._next = next

    def set_previous(self, prev):
        self._previous = prev

    def set_sprite(self, sprite):
        self._sprite = sprite

    def sprite(self):
        return self._sprite

    def __str__(self):
        return str(self._value)
