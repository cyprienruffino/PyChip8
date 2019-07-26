class AbstractError(NotImplementedError):
    def __init__(self, *args, **kwargs):
        return super().__init__("Abstract class, cannot be instanciated")
