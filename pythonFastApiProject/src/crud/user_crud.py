from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.auth.auth import get_password_hash
from src.schemas.user_schema import UserInDB
from src import models


def get_user(db: Session, user_id: int):
    return db.query(models.UserModel).filter(models.UserModel.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.UserModel).filter(models.UserModel.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.UserModel).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserInDB):
    hashed_password = get_password_hash(user.hashed_password)
    db_user = models.UserModel(username=user.username, full_name=user.full_name, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def check_if_username_taken(db: Session,  username: str):
    user = db.query(models.UserModel).filter(models.UserModel.username == username).first()
    if user:
        raise HTTPException(status_code=204)
    else:
        return False


def update_user(db: Session, new_user: UserInDB):
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
