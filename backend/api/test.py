from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World", "status": "working"}

@app.get("/api/health")
def health():
    return {"status": "healthy"}

handler = app
