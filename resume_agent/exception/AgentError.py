from .AgentErrorCode import AgentErrorCode

class AgentError(Exception):

    def __init__(self, code:AgentErrorCode, message:str, details:str = ""):
        self.code = code
        self.message = message
        self.details = details
        super().__init__(f"{code.name}: {message} - {details}")
