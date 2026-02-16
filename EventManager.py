class Events:
    COMPANION_WINDOW_CONSTRUCT = 'base-cwc'
    COMPANION_TRAY_INIT = 'base-cti'
    CONFIG_LOAD = 'base-cl'
    RESTART = 'base-rst'
    PLUGINS_INIT = 'base-pi'
    COMPANION_WINDOW_MOVED = 'base-cwm'
    COMPANION_WINDOW_MOUSE_DOWN = 'base-cwmd'
    COMPANION_WINDOW_MOUSE_UP = 'base-cwmu'
    COMPANION_WINDOW_MOUSE_DOUBLE_CLICK = 'base-cwmdc'
    COMPANION_WINDOW_RENDER_PRE = 'base-cwrpr'
    COMPANION_WINDOW_RENDER_POST = 'base-cwrps'
    COMPANION_WINDOW_TICK = 'base-cwtk'


class EventManager:
    def __init__(self):
        self.listeners: dict[str, list] = {}

    def fire(self, event: str, sender, *args):
        if event in self.listeners:
            for listener in self.listeners[event]:
                listener(sender, *args)

    def register_listener(self, event: str, listener):
        if event not in self.listeners:
            self.listeners[event] = []
        self.listeners[event].append(listener)

    def unregister_listener(self, event: str, listener):
        if event not in self.listeners or listener not in self.listeners[event]:
            return
        self.listeners[event].remove(listener)


INSTANCE = EventManager()
