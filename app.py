import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from XiaoLiuRen import XiaoLiuRen, MeiHuaYiShu

app = FastAPI()

@app.get("/api/xiaoliuren")
def get_xiaoliuren():
    return XiaoLiuRen()

@app.get("/api/meihua")
def get_meihua(num1: int, num2: int):
    return MeiHuaYiShu(num1, num2)

app.mount("/", StaticFiles(directory="static", html=True), name="static")
