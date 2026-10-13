import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from XiaoLiuRen import XiaoLiuRen, MeiHuaYiShu_number, MeiHuaYiShu_time

app = FastAPI()

@app.get("/api/xiaoliuren")
def get_xiaoliuren():
    return XiaoLiuRen()

@app.get("/api/meihua/number")
def get_meihua_number(num1: int, num2: int):
    return MeiHuaYiShu_number(num1, num2)

@app.get("/api/meihua/time")
def get_meihua_time():
    return MeiHuaYiShu_time()

app.mount("/", StaticFiles(directory="static", html=True), name="static")
