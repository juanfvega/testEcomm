from sqlalchemy.orm import Session
from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(is_active=True, email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
        db_user = db.query(models.User).filter(models.User.id == user_id)
        return db_user

def update_user(user_id: int, user:schemas.UserCreate, db: Session):
    db_user = db.query(models.User).filter(models.User.id == user_id)
    user_data_update = user.model_dump(exclude_unset=True)
    db_user.update(user_data_update)    
    db.commit()
    return db_user.first()
