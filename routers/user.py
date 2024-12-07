from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from app.models import *
from app.schemas import CreateUser, UpdateUser
from sqlalchemy import insert, select, update, delete
from typing import Annotated
from slugify import slugify

# Создаем маршруты для управления пользователями с использованием APIRouter
router = APIRouter(prefix="/user", tags=["user"])

@router.get("/")
async def all_users(db: Session = Depends(get_db)):
    # Получаем всех пользователей из базы данных
    stmt = select(User)
    users = db.execute(stmt).scalars().all()
    return users


@router.get("/{user_id}")
async def user_by_id(user_id: int, db: Session = Depends(get_db)):
    # Извлечение пользователя по ID
    stmt = select(User).where(User.id == user_id)
    user = db.execute(stmt).scalars().first()

    if user is None:
        raise HTTPException(status_code=404, detail="User was not found")

    return user


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user(user: CreateUser, db: Annotated[Session, Depends(get_db)]):

    # Проверка на существование пользователя с таким же username
    existing_user = db.execute(select(User).where(User.username == user.username)).scalars().first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")


    # Вставка нового пользователя в базу данных
    stmt = insert(User).values(
        username=user.username,
        firstname=user.firstname,
        lastname=user.lastname,
        age=user.age,
        slug=slugify(user.username),
    )

    db.execute(stmt)
    db.commit()

    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


@router.put("/update/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(user_id: int, user: UpdateUser, db: Session = Depends(get_db)):
    # Поиск пользователя по ID
    stmt = select(User).where(User.id == user_id)
    existing_user = db.execute(stmt).scalars().first()

    if existing_user is None:
        raise HTTPException(status_code=404, detail="User was not found")

    # Обновление данных пользователя
    stmt = update(User).where(User.id == user_id).values(
        firstname=user.firstname,
        lastname=user.lastname,
        age=user.age,
    )

    db.execute(stmt)
    db.commit()

    return {'status_code': status.HTTP_200_OK, 'transaction': 'User update is successful!'}


@router.delete("/delete/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    # Поиск пользователя по ID
    stmt = select(User).where(User.id == user_id)
    existing_user = db.execute(stmt).scalars().first()

    if existing_user is None:
        raise HTTPException(status_code=404, detail="User was not found")

    # Удаление пользователя из базы данных
    stmt = delete(User).where(User.id == user_id)

    db.execute(stmt)
    db.commit()

    return {'status_code': status.HTTP_204_NO_CONTENT}
