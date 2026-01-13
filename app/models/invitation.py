from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime
from sqlalchemy.sql import func
from app.database import Base
import enum


class InvitationStatus(enum.Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"


class GroupInvitation(Base):
    __tablename__ = "group_invitations"

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    invited_email = Column(String, nullable=False)
    invited_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(Enum(InvitationStatus), default=InvitationStatus.pending)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
