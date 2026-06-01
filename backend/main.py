from fastapi import FastAPI

app = FastAPI(title="Vigil API", version="0.1.0")

@app.get("/")
def root():
    return {"message": "Vigil API is running"}