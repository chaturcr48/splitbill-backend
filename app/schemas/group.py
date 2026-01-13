from pydantic import BaseModel, field_validator, ConfigDict
from typing import List
from datetime import datetime

class GroupCreate(BaseModel):
    name: str

# 1. Create a schema for the individual member objects
class GroupMemberSchema(BaseModel):
    user_id: int
    user_name: str

    class Config:
        from_attributes = True


# 2. Update your GroupResponse to expect a LIST of members
class GroupResponse(BaseModel):
    id: int
    name: str
    created_by: int
    created_at: datetime
    members: List[GroupMemberSchema] 

    class Config:
        from_attributes = True

