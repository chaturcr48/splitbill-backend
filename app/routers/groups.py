from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.group import Group
from app.models.group_member import GroupMember
from app.models.invitation import GroupInvitation
from app.schemas.group import GroupCreate, GroupResponse
from app.utils.dependencies import get_current_user
from app.services.email_service import send_invitation_email
from app.schemas.invitation import InviteUserRequest

router = APIRouter(prefix="/groups", tags=["Groups"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("", response_model=GroupResponse)
def create_group(
    group: GroupCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_group = Group(name=group.name, created_by=current_user.id)
    db.add(new_group)
    db.commit()
    db.refresh(new_group)

    member = GroupMember(group_id=new_group.id, user_id=current_user.id)
    db.add(member)
    db.commit()

    return new_group

# @router.get("")
# def my_groups(
#     current_user = Depends(get_current_user),
#     db: Session = Depends(get_db)
# ):
#     groups = (
#         db.query(Group)
#         .join(GroupMember)
#         .filter(GroupMember.user_id == current_user.id)
#         .all()
#     )
#     return groups

@router.get("")
def my_groups(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    member_counts_subquery = (
        db.query(
            GroupMember.group_id, 
            func.count(GroupMember.user_id).label("total_members")
        )
        .group_by(GroupMember.group_id)
        .subquery()
    )

    results = (
        db.query(Group, member_counts_subquery.c.total_members)
        .join(GroupMember, Group.id == GroupMember.group_id)
        .outerjoin(member_counts_subquery, Group.id == member_counts_subquery.c.group_id)
        .filter(GroupMember.user_id == current_user.id)
        .all()
    )

    return [
        {
            "id": group.id,
            "name": group.name,
            "created_by": group.created_by,
            "created_at": group.created_at,
            "total_members": total_members or 0 
        } 
        for group, total_members in results
    ]


@router.post("/{group_id}/invite")
def invite_user(
    group_id: int,
    payload: InviteUserRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    invitation = GroupInvitation(
        group_id=group_id,
        invited_email=payload.email,
        invited_by=current_user.id,
    )

    db.add(invitation)
    db.commit()

    send_invitation_email(payload.email, group.name)

    return {"message": "Invitation sent"}