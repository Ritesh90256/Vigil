import sys
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)


def show_traces():
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM traces ORDER BY id DESC LIMIT 10")
        )
        traces = result.fetchall()

    print("\n📊 Vigil CLI Dashboard\n")
    print("=" * 60)

    if not traces:
        print("No traces found.")
        return

    for trace in traces:
        t = trace._mapping

        print(f"Trace ID: {t['id']}")
        print(f"Input: {t['input']}")
        print(f"Output: {t['output']}")
        print(f"Latency: {t['latency']} ms")
        print(f"Created At: {t['created_at']}")
        print("-" * 60)


if __name__ == "__main__":
    show_traces()