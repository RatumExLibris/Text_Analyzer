from src.preprocessing import Pipeline
from fastapi import FastAPI, Depends

app = FastAPI()
tags = ''
pipeline = Pipeline()

@app.get("/")
def index():
    return "Анализ текста"

@app.get("/get_tags_from_text")
async def single_student(text: str) -> dict:
    pipeline.set_text(text)
    pipeline.process()
    return pipeline.get_tags()
