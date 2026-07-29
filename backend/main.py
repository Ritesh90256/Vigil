import os
import json
from dotenv import load_dotenv
from fastapi import FastAPI, logger, HTTPException, Query
from sqlalchemy import create_engine, text
from classifier.core import classify_trace
from .models import FailureMode

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
                     INSERT INTO traces (trace_data, failure_mode, confidence, reasoning, agent_goal)
                        VALUES (:trace_data, :failure_mode, :confidence, :reasoning, :agent_goal)
                     RETURNING id
                        """)
        result = conn.execute(query, {
            "trace_data": json.dumps(trace),
            "failure_mode": trace.get("failure_mode"),
            "confidence": trace.get("confidence"),
            "reasoning": trace.get("reasoning"),
            "agent_goal": trace.get("agent_goal")
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
def get_all_traces(
    failure_mode: FailureMode | None = None,
    confidence: str | None = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100)
    ):

    offset = (page - 1) * limit
    traces = []

    query = """
            SELECT 
            id, 
            agent_goal,
            failure_mode,
            confidence,
            reasoning,
            trace_data
            FROM 
            traces
            """

    conditions = []
    params = {}
    if failure_mode:
        conditions.append("failure_mode = :failure_mode")
        params["failure_mode"] = failure_mode
    
    if confidence:
        conditions.append("confidence = :confidence")
        params["confidence"] = confidence
    
    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    #pagination
    query += " LIMIT :limit OFFSET :offset"
    params["limit"] = limit
    params["offset"] = offset

    with engine.connect() as conn:
        result = conn.execute(text(query), params)
        rows = result.fetchall()
        for row in rows:
            traces.append(dict(row._mapping))
    
    return traces




@app.get("/traces/{trace_id}")
def get_trace_by_id(trace_id: int
):
    with engine.connect() as conn:
        result = conn.execute(text("""
                                   SELECT
                                    id,
                                    agent_goal,
                                    failure_mode,
                                    confidence,
                                    reasoning,
                                    trace_data
                                   FROM
                                    traces
                                   WHERE 
                                    id = :trace_id
                                   """
                                   ), {"trace_id": trace_id})
        row = result.fetchone()

    if row is None:
            raise HTTPException(status_code=404, detail="Trace not found")
        
    return dict(row._mapping)



@app.get("/stats")
def get_stats():
    with engine.connect() as conn:
        result = conn.execute(text("""
                                   SELECT COUNT(*) FROM traces
                                   """))
        total_traces = result.scalar()
    
        failure_count = {}

        for mode in FailureMode:
            failure_count[mode.value] = 0

        failure_count["unclassified"] = 0

        result = conn.execute(text("""
                                   SELECT failure_mode, COUNT(*) as count
                                   FROM traces
                                   GROUP BY failure_mode
                                   """))
        rows = result.fetchall()
        for row in rows:
            failure_mode = row._mapping["failure_mode"]
            count = row._mapping["count"]
            if failure_mode is None:
                failure_count["unclassified"] += count
            else:
                failure_count[failure_mode]+=count

    return{
        "total_traces": total_traces,
        "failure_count": failure_count
    }

