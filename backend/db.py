from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Создание движка базы данных
engine = create_engine('sqlite:///taskmanager.db', echo=True)

# Создание локальной сессии
SessionLocal = sessionmaker(bind=engine)

# Создание базового класса для моделей
class Base(DeclarativeBase): pass

# Создание всех таблиц в базе данных
# def init_db():
# from app.models import User, Task  # Импортируем модели
Base.metadata.create_all(bind=engine)
    # print("Созданы таблицы:")
    # print(Base.metadata.tables)  # Печать SQL-запросов для создания таблиц

# Вызов функции init_db() для создания таблиц при запуске приложения
#  if __name__ == "__main__":
# init_db()


