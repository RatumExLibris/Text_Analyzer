from app.src.preprocessing import Pipeline
from fastapi import FastAPI, Depends

app = FastAPI()
pipeline = Pipeline()

@app.get("/")
def index():
    return "Анализ текста"

@app.post("/post_text")
async def analyze(text: str):
    pipeline.set_text(text)
    pipeline.process()

@app.get("/get_tags")
async def get_tags() -> dict:
    return pipeline.get_tags()
