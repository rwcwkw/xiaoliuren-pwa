import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from XiaoLiuRen import XiaoLiuRen

app = FastAPI()

@app.get("/api/xiaoliuren")
def get_xiaoliuren():
    return XiaoLiuRen()

app.mount("/", StaticFiles(directory="static", html=True), name="static")

