import os

from dotenv import load_dotenv
from fastapi import FastAPI
from sqlalchemy import create_engine, text

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

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

@app.get("/traces")
def get_all_traces():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM traces"))
        traces = result.fetchall()

    return [dict(row._mapping) for row in traces]

@app.get("/traces/{trace_id}")
def get_trace_by_id(trace_id: int):
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM traces WHERE id = :id"),
            {"id": trace_id}
        )
        trace = result.fetchone()

    if trace is None:
        return {"error": "Trace not found"}

    return dict(trace._mapping)