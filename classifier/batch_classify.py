import csv
import json
from pathlib import Path
from core import classify_trace

LABELED_CSV = Path(__file__).parent.parent / "data" / "labeled" / "trace_labels.csv"
RAW_DIR = Path(__file__).parent.parent / "data" / "raw"
OUTPUT_CSV = Path(__file__).parent / "batch_results.csv"


def run_batch_test():
    """
    Runs the classifier on every trace in the labeled dataset,
    compares predicted vs expected failure_mode, writes results to CSV.
    """
    results = []

    with open(LABELED_CSV, "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    total = len(rows)

    for i, row in enumerate(rows):
        trace_id = row["trace_id"]
        expected = row["failure_mode"]

        raw_trace_path = RAW_DIR / f"{trace_id}.json"

        # Skip gracefully if a raw trace file is missing instead of crashing
        if not raw_trace_path.exists():
            print(f"[{i+1}/{total}] {trace_id}: SKIPPED — raw file not found")
            continue

        with open(raw_trace_path, "r") as tf:
            trace_data = json.load(tf)

        prediction = classify_trace(trace_data)
        predicted = prediction["failure_mode"]
        correct = "yes" if predicted == expected else "no"

        results.append({
            "trace_id": trace_id,
            "expected": expected,
            "predicted": predicted,
            "confidence": prediction["confidence"],
            "correct": correct,
            "reasoning": prediction["reasoning"]
        })

        print(f"[{i+1}/{total}] {trace_id}: expected={expected}, predicted={predicted}, correct={correct}")

    # Write all results to CSV for review in Excel/Sheets
    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["trace_id", "expected", "predicted", "confidence", "correct", "reasoning"]
        )
        writer.writeheader()
        writer.writerows(results)

    correct_count = sum(1 for r in results if r["correct"] == "yes")
    accuracy = (correct_count / len(results)) * 100 if results else 0

    print(f"\n{'='*50}")
    print(f"Accuracy: {correct_count}/{len(results)} ({accuracy:.1f}%)")
    print(f"Results saved to: {OUTPUT_CSV}")
    print(f"{'='*50}")


if __name__ == "__main__":
    run_batch_test()