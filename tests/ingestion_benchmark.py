import json
import time
import requests
from pathlib import Path

BACKEND_URL = "http://127.0.0.1:8000/traces"
TRACE_FILE = Path(__file__).parent.parent / "data" / "synthetic_traces.jsonl"

def load_traces():
    traces =[]

    with open(TRACE_FILE, "r", encoding = "utf-8") as file:
        for line in file:
            traces.append(json.loads(line))

    return traces

def run_benchmark():
    traces = load_traces()

    print(f"Loaded {len(traces)} traces. ")

    successful = 0
    failed = 0

    start_time = time.perf_counter()

    for i, trace in enumerate(traces, start = 1):
        try:
            response = requests.post(
                BACKEND_URL,
                json = trace
            )

            response.raise_for_status()
            successful+=1

        except requests.exceptions.RequestException as e:
            failed+=1
            print(f"Trace {i} failed : {e}")

    elapsed = time.perf_counter() - start_time

    throughput = successful/ elapsed if elapsed > 0 else 0

    print("" \
    "Benchmark Results : ")
    print(f"Total traces : {len(traces)}")
    print(f"Successful : {successful}")
    print(f"Failed : {failed}")
    print(f"Total time : {elapsed:.2f} seconds")
    print(f"throughput: {throughput:.2f} traces/sec")


if __name__ == "__main__":
    run_benchmark()