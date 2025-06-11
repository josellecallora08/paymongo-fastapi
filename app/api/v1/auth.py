from fastapi import APIRouter, Depends, HTTPException, status
from app.core.security import create_access_token, verify_password
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import User
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.core.security import hash_password
router = APIRouter()

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(
        User.email == form_data.username
    ).first()
    if not user or not verify_password(form_data.password,user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    token = create_access_token(
        data={"sub": user.email}
    )
    return  {
        "access_token": token,
        "token_type": "bearer"
    }

@router.post("/register")
def register(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        User.email == form_data.username
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    new_user = User(
        email=form_data.username,
        password=hash_password(form_data.password)  # Ensure password is hashed in the User model
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    token = create_access_token(
        data={"sub": new_user.email}
    )

    return {
        "message": "User registered successfully",
        "user": new_user,
        "token": token,
    }