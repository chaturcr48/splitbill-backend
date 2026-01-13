from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from app.database import Base
from sqlalchemy.orm import relationship

class GroupMember(Base):
    __tablename__ = "group_members"

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    group = relationship("Group", back_populates="members")
    user = relationship("User") 

    @property
    def user_name(self) -> str:
        if self.user:
            return getattr(self.user, 'name', None)
        return "Unknown User"


    __table_args__ = (
        UniqueConstraint("group_id", "user_id", name="uq_group_user"),
    )
