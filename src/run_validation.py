import argparse
import json
from pathlib import Path

import pandas as pd

try:
    from .validate_data import validate_vector_file
except ImportError:
    from validate_data import validate_vector_file


def main():
    parser = argparse.ArgumentParser(
        description="Run GIS data-quality validation."
    )
    parser.add_argument(
        "input_file",
        help="Path to the vector dataset to validate.",
    )

    args = parser.parse_args()

    result = validate_vector_file(args.input_file)

    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    json_path = output_dir / "validation_report.json"
    csv_path = output_dir / "validation_report.csv"

    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(result, file, indent=4)

    pd.DataFrame([result]).to_csv(csv_path, index=False)

    print(f"Validation completed: {result['status']}")
    print(f"Quality score: {result.get('quality_score', 'N/A')}")
    print(f"JSON report: {json_path}")
    print(f"CSV report: {csv_path}")


if __name__ == "__main__":
    main()