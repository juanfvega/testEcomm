from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from . import crud , models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

# Dependency

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db=db, skip=skip, limit=limit)
    return users



@app.post("/users/", response_model=schemas.UserCreate)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    return crud.create_user(db=db, user=user)

@app.delete("/users/{user_id}", response_model = int)
def delete_user(user_id: int , db: Session = Depends(get_db)):
    db_user = crud.delete_user(db = db, user_id = user_id)
    if db_user:
        user_deleted = db_user.first().id
        db_user.delete()
        db.commit()
        return user_deleted
    else: 
        raise HTTPException(status_code=400, detail="user not exists")
    

@app.patch("/users/{user_id}")
def update_user(user_id: int , user: schemas.UserCreate, db: Session=Depends(get_db)):
    user_data = crud.update_user(user_id=user_id, user=user, db=db)
    if user_data:
        return user_data
    else:
        HTTPException(status_code=400, detail="error update user")

