from hooks.Hook import Hook


class HelloWorldHook(Hook):
    def __init__(self):
        pass

    def call(self):
        print("Hello World!")