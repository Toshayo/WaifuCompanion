import enum


class Events(enum.Enum):
    COMPANION_WINDOW_CONSTRUCT = 0
    COMPANION_TRAY_INIT = 1
    RESTART = 2
    PLUGINS_INIT = 3


class EventManager:
    def __init__(self):
        self.listeners: dict[Events, list] = {}

    def fire(self, sender, event: Events):
        if event in self.listeners:
            for listener in self.listeners[event]:
                listener(sender)

    def register_listener(self, event: Events, listener):
        if event not in self.listeners:
            self.listeners[event] = []
        self.listeners[event].append(listener)

    def unregister_listener(self, event: Events, listener):
        if event not in self.listeners or listener not in self.listeners[event]:
            return
        self.listeners[event].remove(listener)


INSTANCE = EventManager()
