from fastapi import APIRouter

route = APIRouter(prefix="/auth")


@route.get("/login")
def login():
    return {"data": "ho"}


@route.get("/login")
def register():
    return {"data": "ho"}
