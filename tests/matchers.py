class InstanceOf:
    """Custom matcher to check if a mock argument is an instance of a given class."""

    def __init__(self, cls):
        self.cls = cls

    def __eq__(self, other):
        return isinstance(other, self.cls)
