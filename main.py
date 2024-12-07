# Подключаем необходимые библиотеки
from fastapi import FastAPI
from app.routers.task import router as task_router
from app.routers.user import router as user_router

# Создаем экземпляр FastAPI и определяем маршрут - '/', по которому функция welcome()
# возвращает словарь - {"message": "Welcome to Taskmanager"}
app = FastAPI()

@app.get("/")
async def welcome():
    return {"message": "Welcome to Taskmanager"}

#  Подключаем маршруты из модулей task и user
app.include_router(task_router)
app.include_router(user_router)
