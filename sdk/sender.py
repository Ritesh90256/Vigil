import requests

# FastAPI endpoint that receives completed traces
BACKEND_URL = "http://127.0.0.1:8000/traces"


def send_trace_to_backend(trace):
    """
    Sends a completed Trace object to the Vigil backend.

    The sender is responsible only for networking.
    It does not modify or inspect the trace.
    """

    try:
        response = requests.post(
            BACKEND_URL,
            json=trace.to_dict()
        )

        # Raise an exception if the backend returns 4xx or 5xx
        response.raise_for_status()

        print("Trace successfully sent to backend.")
        print("Backend Response:", response.json())

    except requests.exceptions.RequestException as e:
        print(f"Failed to send trace: {e}")