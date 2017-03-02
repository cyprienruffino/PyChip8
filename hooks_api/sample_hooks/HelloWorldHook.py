from IHook import IHook


class HelloWorldHook(IHook):
    def __init__(self):
        pass

    def call(self):
        print("Hello World!")