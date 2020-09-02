

class CustomError():
    def __init__(self, message, errorCode):
        self.message = message
        self.errorCode = errorCode

    def to_json(self):
        return {"message": self.message, "code": self.errorCode}



class NotFoundError(CustomError):

    def __init__(self, message):
        super().__init__(message, 404)

    
