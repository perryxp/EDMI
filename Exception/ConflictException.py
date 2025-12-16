class ConflictException(Exception):
    def __init__(self, message="Conflict with related resources"):
        super().__init__(message)
