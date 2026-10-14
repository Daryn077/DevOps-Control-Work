import os

from bson import ObjectId
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient

app = FastAPI()

mongo_user = os.getenv("MONGO_USER")
mongo_password = os.getenv("MONGO_PASSWORD")
mongo_db = os.getenv("MONGO_DB")
mongo_host = os.getenv("MONGO_HOST", "db")
mongo_port = int(os.getenv("MONGO_PORT", "27017"))

client = MongoClient(
    host=mongo_host,
    port=mongo_port,
    username=mongo_user,
    password=mongo_password,
    authSource="admin"
)

db = client[mongo_db]
users = db["users"]


class User(BaseModel):
    name: str
    age: int


def format_user(user):
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "age": user["age"]
    }


@app.get("/")
def home():
    return {"message": "FastAPI + MongoDB"}


@app.post("/users")
def create_user(user: User):
    result = users.insert_one(user.model_dump())

    return {
        "message": "User created",
        "id": str(result.inserted_id)
    }


@app.get("/users")
def get_users():
    return [format_user(user) for user in users.find()]


@app.get("/users/{user_id}")
def get_user(user_id: str):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid ID"
        )

    user = users.find_one({"_id": ObjectId(user_id)})

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return format_user(user)


@app.put("/users/{user_id}")
def update_user(user_id: str, user: User):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid ID"
        )

    result = users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": user.model_dump()}
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {"message": "User updated"}


@app.delete("/users/{user_id}")
def delete_user(user_id: str):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid ID"
        )

    result = users.delete_one(
        {"_id": ObjectId(user_id)}
    )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {"message": "User deleted"}
