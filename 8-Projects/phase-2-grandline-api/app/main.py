from fastapi import FastAPI 

app = FastAPI()

maps = [
    {"id": "1", "crew": "Straw Hat", "island": "Elbaf"},
]


@app.get("/")
def root():
    return {"test": "Welcome to Grandline API"}