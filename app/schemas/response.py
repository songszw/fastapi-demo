class ResponseModel:
    def __init__(self, code: int, message: str, data: any = None):
        self.code = code
        self.message = message
        self.data = data
