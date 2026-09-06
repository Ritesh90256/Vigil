import csv
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

GROUND_TRUTH_FILE = (
    Path(__file__).parent.parent / "data" / "synthetic_labels.csv"
)


def load_ground_truth():
    ground_truth = {}

    with open(GROUND_TRUTH_FILE, encoding="utf-8") as file:
        rows = csv.DictReader(file)

        for row in rows:
            ground_truth[row["trace_id"]] = row["failure_mode"]

    return ground_truth


def load_predictions():
    predictions = {}

    with engine.connect() as conn:
        query = text(
            """
            SELECT
                trace_data ->> 'trace_id' AS trace_id,
                failure_mode
            FROM traces
            WHERE trace_data ->> 'trace_id' LIKE 'synthetic_%'
            """
        )

        result = conn.execute(query)
        rows = result.fetchall()

        for row in rows:
            predictions[row._mapping["trace_id"]] = row._mapping[
                "failure_mode"
            ]

    return predictions


def calc_metrics(mode, ground_truth, predictions):
    tp = 0
    fp = 0
    fn = 0

    for trace_id in ground_truth:
        actual = ground_truth[trace_id]
        predicted = predictions.get(trace_id)

        if predicted is None:
            continue

        if actual == mode and predicted == mode:
            tp += 1
        elif actual != mode and predicted == mode:
            fp += 1
        elif actual == mode and predicted != mode:
            fn += 1

    return tp, fp, fn


ground_truth = load_ground_truth()
predictions = load_predictions()

modes = set(ground_truth.values())
modes.remove("none")

results = {}

for mode in modes:
    tp, fp, fn = calc_metrics(
        mode,
        ground_truth,
        predictions
    )
    results[mode] = (tp, fp, fn)

metrics_results = {}

for mode, metrics in results.items():
    tp, fp, fn = metrics

    if tp + fp == 0:
        precision = 0
    else:
        precision = tp / (tp + fp)

    if tp + fn == 0:
        recall = 0
    else:
        recall = tp / (tp + fn)

    if precision + recall == 0:
        f1 = 0
    else:
        f1 = 2 * precision * recall / (precision + recall)

    metrics_results[mode] = {
        "precision": precision,
        "recall": recall,
        "f1": f1
    }

print(json.dumps(metrics_results, indent=2))