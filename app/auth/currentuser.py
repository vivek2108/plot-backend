from pydantic import BaseModel

class CurrentUser(BaseModel):
    """
    Represents the authenticated user's identity and role.

    Attributes:
        user_id (int): Unique ID of the user.
        username (str): Username of the user.
        role (str): Role assigned to the user (e.g., 'admin', 'user').

    Methods:
        is_admin(): Returns True if the user's role is 'admin'.
    """

    user_id: int
    username: str
    role: str

    def is_admin(self) -> bool:
        """
        Check if the user has admin privileges.

        Returns:
            bool: True if role is 'admin', False otherwise.
        """
        return self.role == "admin"
