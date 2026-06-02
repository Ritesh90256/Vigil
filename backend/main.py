from fastapi import FastAPI
from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/Vigil"

engine = create_engine(DATABASE_URL)
app = FastAPI()

@app.get("/")
def home():
    return {"message": "Vigil backend running"}

@app.post("/traces")
def create_trace(trace: dict):
    with engine.connect() as conn:
        query = text("""
            INSERT INTO traces (input, output, latency)
            VALUES (:input, :output, :latency)
        """)
        conn.execute(query, {
            "input": trace.get("input"),
            "output": trace.get("output"),
            "latency": trace.get("latency")
        })
        conn.commit()

    return {"status": "stored"}