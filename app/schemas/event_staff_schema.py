from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class AddMemberSchema(BaseModel):
    user_id: int 
    role: Optional[str] = Field("MEMBER")

class EventMemberResponse(BaseModel):
    user_id: int
    user_name: str
    email: str
    role: str

    class Config:
        from_attributes = True
