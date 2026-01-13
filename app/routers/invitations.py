from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.invitation import GroupInvitation, InvitationStatus
from app.models.group_member import GroupMember
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/invitations", tags=["Invitations"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("")
def get_my_invitations(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return (
        db.query(GroupInvitation)
        .filter(
            GroupInvitation.invited_email == current_user.email,
            GroupInvitation.status == InvitationStatus.pending,
        )
        .all()
    )

@router.post("/{invitation_id}/accept")
def accept_invitation(
    invitation_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    invitation = db.query(GroupInvitation).filter_by(id=invitation_id).first()
    if not invitation:
        raise HTTPException(status_code=404, detail="Invitation not found")

    invitation.status = InvitationStatus.accepted

    member = GroupMember(
        group_id=invitation.group_id,
        user_id=current_user.id,
    )

    db.add(member)
    db.commit()

    return {"message": "Joined group successfully"}

@router.post("/{invitation_id}/reject")
def reject_invitation(
    invitation_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    invitation = db.query(GroupInvitation).filter_by(id=invitation_id).first()
    if not invitation:
        raise HTTPException(status_code=404, detail="Invitation not found")

    invitation.status = InvitationStatus.rejected
    db.commit()

    return {"message": "Invitation rejected"}

