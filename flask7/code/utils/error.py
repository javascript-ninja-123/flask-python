


class CustomError():
    def __init__(self, message, errorCode):
        self.message = message
        self.errorCode = errorCode
    
    def json(self):
        return {
            "message":self.message,
            "code": self.errorCode
        }, self.errorCode

    
    @classmethod
    def is_custom_error(cls, instance):
        return isinstance(instance, CustomError)
  

class NotFoundError(CustomError):

    errorCode = 400

    def __init__(self,message):
        super().__init__(message, NotFoundError.errorCode)


class InternalError(CustomError):

    errorCode = 500

    def __init__(self, message):
        super().__init__(message, InternalError.errorCode)




    
