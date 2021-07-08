class Error:
    def __init__(self, error_message):
        self.error_message = error_message
    def toDict(self):
        return {"error":self.error_message}


class ErrUserWithEmailAlreadyRegistered(Error):
    def __init__(self, email):
        self.error_message = f"User with email {email} already registred"
        Error.__init__(self, self.error_message)



