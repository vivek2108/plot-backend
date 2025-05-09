from pydantic import BaseModel


class CurrentUser(BaseModel):
    user_id: int
    username: str
    role: str

    # Optional: define methods for cleaner role checks
    def is_admin(self) -> bool:
        return self.role == "admin"
