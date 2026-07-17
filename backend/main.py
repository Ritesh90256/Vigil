import os
import json
from dotenv import load_dotenv
from fastapi import FastAPI, logger
from sqlalchemy import create_engine, text
from classifier.core import classify_trace

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
app = FastAPI()

@app.get("/")
def home():
    return {"message": "Vigil backend running"}

@app.post("/traces")
def create_trace(trace: dict):
    # insert the trace
    with engine.connect() as conn:
        query = text("""
                     INSERT INTO traces (trace_data, failure_mode, confidence, reasoning)
                        VALUES (:trace_data, :failure_mode, :confidence, :reasoning)
                     RETURNING id
                        """)
        result = conn.execute(query, {
            "trace_data": json.dumps(trace),
            "failure_mode": trace.get("failure_mode"),
            "confidence": trace.get("confidence"),
            "reasoning": trace.get("reasoning")
        })

        #get inserted row's id
        new_id = result.scalar()
        conn.commit()

    try:    

        # call classify_trace
        classification = classify_trace(trace)

        # update the row with failure_mode, confidence, reasoning
        with engine.connect() as conn:
            update_query = text("""
                                UPDATE traces
                                SET failure_mode = :failure_mode,
                                    confidence = :confidence,
                                    reasoning = :reasoning
                                WHERE id = :new_id
                                """)
            conn.execute(update_query, {
                "failure_mode": classification.get("failure_mode"),
                "confidence": classification.get("confidence"),
                "reasoning": classification.get("reasoning"),
                "new_id": new_id
            })
            conn.commit()

        return {"status": "success", "trace_id": new_id}
    
    except Exception:
        logger.exception(f"failed to classify trace: {new_id}")

        return {"status": "partial_success",
                "trace_id": new_id,
                "message": "trace stored successfully, but classification failed"
                }
    

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
