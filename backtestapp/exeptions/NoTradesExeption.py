class NoTradesException(Exception):

    def __init__(self, message="Error"):
        self.message = message
        super().__init__(self.message)
