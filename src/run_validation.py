import json
from pathlib import Path

import pandas as pd

from validate_data import validate_vector_file


DATASET = "data/raw/sample_points.gpkg"
OUTPUT_DIR = Path("outputs")


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    result = validate_vector_file(DATASET)

    # JSON report
    json_path = OUTPUT_DIR / "validation_report.json"
    with json_path.open("w", encoding="utf-8") as file:
        json.dump(result, file, indent=4)

    # CSV report
    csv_path = OUTPUT_DIR / "validation_report.csv"
    pd.DataFrame([result]).to_csv(csv_path, index=False)

    print(f"Validation completed: {result['status']}")
    print(f"Quality score: {result.get('quality_score', 'N/A')}")
    print(f"JSON report: {json_path}")
    print(f"CSV report: {csv_path}")


if __name__ == "__main__":
    main()