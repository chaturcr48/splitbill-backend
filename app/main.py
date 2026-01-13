from fastapi import FastAPI
from app.database import engine
from app.models import User, Group
from app.routers.auth import router as auth_router
from app.routers.groups import router as group_router
from app.routers.expenses import router as expense_router
from app.routers.balances import router as balance_router
from app.routers.invitations import router as invitation_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Splitwise Clone API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3001", "http://127.0.0.1:3001", "http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

User.metadata.create_all(bind=engine)
Group.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(group_router)
app.include_router(expense_router)
app.include_router(balance_router)
app.include_router(invitation_router)

@app.get("/")
def health_check():
    return {"status": "running"}
