from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from app.models import Task, User
from app.schemas import CreateTask, UpdateTask
from sqlalchemy import insert, select, update, delete
from slugify import slugify

# Создаем маршруты для управления задачами с использованием APIRouter
router = APIRouter(prefix="/task", tags=["task"])

@router.get("/")
async def all_tasks(db: Session = Depends(get_db)):
    # Получаем все задачи из базы данных
    stmt = select(Task)
    tasks = db.execute(stmt).scalars().all()
    return tasks


@router.get("/{task_id}")
async def task_by_id(task_id: int, db: Session = Depends(get_db)):
    # Извлечение задачи по ID
    stmt = select(Task).where(Task.id == task_id)
    task = db.execute(stmt).scalars().first()

    if task is None:
        raise HTTPException(status_code=404, detail="Task was not found")

    return task


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_task(task: CreateTask, user_id: int, db: Session = Depends(get_db)):
    # Проверка на существование пользователя
    existing_user = db.execute(select(User).where(User.id == user_id)).scalars().first()

    if existing_user is None:
        raise HTTPException(status_code=404, detail="User was not found")

    # Вставка новой задачи в базу данных с привязкой к пользователю
    stmt = insert(Task).values(
        title=task.title,
        content=task.content,
        priority=task.priority,
        completed=False,
        user_id=user_id,
        slug=slugify(task.title)
    )

    db.execute(stmt)
    db.commit()

    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


@router.put("/update/{task_id}", status_code=status.HTTP_200_OK)
async def update_task(task_id: int, task: UpdateTask, db: Session = Depends(get_db)):
    # Поиск задачи по ID
    stmt = select(Task).where(Task.id == task_id)
    existing_task = db.execute(stmt).scalars().first()

    if existing_task is None:
        raise HTTPException(status_code=404, detail="Task was not found")

    # Обновление данных задачи
    stmt = update(Task).where(Task.id == task_id).values(
        title=task.title,
        content=task.content,
        priority=task.priority,
        completed=task.completed,
    )

    db.execute(stmt)
    db.commit()

    return {'status_code': status.HTTP_200_OK, 'transaction': 'Task update is successful!'}


@router.delete("/delete/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    # Поиск задачи по ID
    stmt = select(Task).where(Task.id == task_id)
    existing_task = db.execute(stmt).scalars().first()

    if existing_task is None:
        raise HTTPException(status_code=404, detail="Task was not found")

    # Удаление задачи из базы данных
    stmt = delete(Task).where(Task.id == task_id)

    db.execute(stmt)
    db.commit()

    return {'status_code': status.HTTP_204_NO_CONTENT}
