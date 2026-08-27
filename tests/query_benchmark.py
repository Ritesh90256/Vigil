import time
import requests
import statistics

BACKEND_URL = "http://127.0.0.1:8000"

QUERY_CASES = [
    {
        "name": "all_traces",
        "path": "/traces?limit=50"
    },
    {
        "name": "failure_filter",
        "path": "/traces?failure_mode=retry_storm&limit=50"
    },
    {
        "name": "confidence_filter",
        "path": "/traces?confidence=high&limit=50"
    }
]


def benchmark_query(path, iterations=100):
    latencies = []

    for _ in range(iterations):
        try:
            start = time.perf_counter()

            response = requests.get(
                BACKEND_URL + path
            )

            response.raise_for_status()

            elapsed = (time.perf_counter() - start) * 1000
            latencies.append(elapsed)

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")

    return latencies


def calculate_percentiles(latencies):
    if not latencies:
        return None, None

    p50 = statistics.median(latencies)

    if len(latencies) == 1:
        p95 = latencies[0]
    else:
        p95 = statistics.quantiles(
            latencies,
            n=100
        )[94]

    return p50, p95


def run_benchmark():
    for query in QUERY_CASES:
        print(f"\nBenchmarking: {query['name']}")

        latencies = benchmark_query(query["path"])

        p50, p95 = calculate_percentiles(latencies)

        print(f"Successful requests: {len(latencies)}")

        if p50 is None:
            print("No successful requests.")
        else:
            print(f"p50 latency: {p50:.2f} ms")
            print(f"p95 latency: {p95:.2f} ms")


if __name__ == "__main__":
    run_benchmark()