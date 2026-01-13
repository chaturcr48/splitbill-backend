from pydantic import BaseModel
from typing import List
from datetime import datetime

# class GroupCreate(BaseModel):
#     name: str

# class GroupResponse(BaseModel):
#     id: int
#     name: str
#     created_by: int

#     class Config:
#         from_attributes = True


# 1. Create a schema for the individual member objects
class GroupMemberSchema(BaseModel):
    user_id: int
    # You can add fields like user_name here later if you join the user table

    class Config:
        from_attributes = True

# 2. Update your GroupResponse to expect a LIST of members
class GroupResponse(BaseModel):
    id: int
    name: str
    created_by: int
    created_at: datetime
    # This change allows group.members.map() to work in your frontend
    members: List[GroupMemberSchema] 

    class Config:
        from_attributes = True

class GroupCreate(BaseModel):
    name: str

