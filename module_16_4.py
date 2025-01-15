from fastapi import FastAPI, Path, status, Body, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

users = []


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get("/")
async def welcome() -> dict:
    return {"message": "Главная страница"}


@app.get('/users', response_model=List[User])
async def get_all_users() -> List[User]:
    return users


@app.post("/user", response_model=User)
async def create_user(username: str, age: int) -> User:
    user_id = len(users) + 1  # Используем текущее количество пользователей для ID
    new_user = User(id=user_id, username=username, age=age)
    users.append(new_user)
    return new_user


@app.put("/user/{user_id}", response_model=User)
async def update_user(user_id: int, username: str, age: int) -> User:
    if user_id <= 0 or user_id > len(users):
        raise HTTPException(status_code=404, detail="User not found")

    users[user_id - 1].username = username
    users[user_id - 1].age = age
    return users[user_id - 1]


@app.delete("/user/{user_id}")
async def delete_user(user_id: int) -> str:
    if user_id <= 0 or user_id > len(users):
        raise HTTPException(status_code=404, detail="User not found")

    users.pop(user_id - 1)
    return f"User with ID {user_id} was deleted."

