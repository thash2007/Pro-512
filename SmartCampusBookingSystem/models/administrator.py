from models.user import User

class Administrator(User):

    def __init__(self, username, password):
        super().__init__(
            username,
            password,
            "Administrator"
        )