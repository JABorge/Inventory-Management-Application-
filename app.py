from fastapi import FastAPI

app = FastAPI()

app.get('/')
def index():
    return {"Msg": "Hello World"}