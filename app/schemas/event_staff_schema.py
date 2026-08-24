from pydantic import BaseModel


class EventMemberResponse(BaseModel):
    user_id: int
    user_name: str
    email: str
    role: str

    class Config:
        from_attributes = True
