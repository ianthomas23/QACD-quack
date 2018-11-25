# Collection of zoom rectangles to support undo/redo functionality.
class ZoomHistory:
    def __init__(self):
        self._stack = []
        self._index = 0   # Index at which new commands are added.

    def append(self, from_, to):
        if self.has_redo():
            del self._stack[self._index+1:]
            self._stack[self._index] = (from_, to)
        else:
            self._stack.append((from_, to))

        self._index += 1

    def clear(self):
        self._stack.clear()
        self._index = 0

    def current(self):
        if self.has_any():
            return self._stack[self._index-1]
        else:
            return None

    def has_any(self):
        return len(self._stack) > 0

    def redo(self):
        zoom = self._stack[self._index]
        self._index += 1
        return zoom

    def undo(self):
        zoom = self._stack[self._index-1]
        self._index -= 1
        return zoom

    def has_undo(self):
        return self._index > 0

    def has_redo(self):
        return self._index < len(self._stack)

