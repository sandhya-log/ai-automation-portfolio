from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse
from app.models.user import User
from app.db.database import get_db
from app.utils.hashing import hash_password, verify_password
from app.utils.jwt_handler import create_access_token
from app.schemas.user import UserLogin, UserUpdate
from app.core.security import get_current_user

router = APIRouter()

@router.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail="Email alreay exist"
        )
    
    hashed_pw = hash_password(user.password)

    new_user = User(
        email = user.email,
        hashed_password = hashed_pw 
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email or password"
        )
    
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid email or password"
        )
    
    access_token = create_access_token({"sub": db_user.email})

    return {"access_token"  : access_token, "token_type": "bearer"}


@router.put("/profile", response_model=UserResponse)
def update_profile(
    update_data : UserUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    if update_data.email:
        current_user.email = update_data.email

    if update_data.password:
        current_user.hashed_password = hash_password(update_data.password)

    db.commit()
    db.refresh(current_user)

    return current_user



@router.get("/ping")
def ping():
    return {"ping" : "pong"}