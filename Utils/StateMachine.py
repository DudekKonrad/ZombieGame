class State:
    def enter(self):
        pass

    def execute(self):
        pass

    def exit(self):
        pass


class StateMachine:
    def __init__(self):
        self.states = {}
        self.active_state = None

    def add_state(self, state_name, state):
        self.states[state_name] = state

    def set_state(self, state_name):
        if self.active_state:
            self.active_state.exit()
        self.active_state = self.states[state_name]
        self.active_state.enter()

    def update(self):
        self.active_state.execute()
