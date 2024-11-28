from pydantic import BaseModel

# Определяем модели данных, наследуемые от BaseModel для создания и обновления пользователей и задач
# для удобной работы с будущими объектами БД
class CreateUser(BaseModel):
    username: str
    firstname: str
    lastname: str
    age: int

class UpdateUser(BaseModel):
    firstname: str
    lastname: str
    age: int

class CreateTask(BaseModel):
    title: str
    content: str
    priority: int

class UpdateTask(BaseModel):
    title: str
    content: str
    priority: int
