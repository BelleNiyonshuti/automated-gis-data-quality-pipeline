from pathlib import Path

import pandas as pd

try:
    from .validate_data import validate_vector_file
except ImportError:
    from validate_data import validate_vector_file


SUPPORTED_EXTENSIONS = {".gpkg", ".shp", ".geojson", ".json"}


def validate_directory(input_dir="data/raw", output_file="outputs/batch_validation_report.csv"):
    input_path = Path(input_dir)
    output_path = Path(output_file)

    files = sorted(
        file
        for file in input_path.iterdir()
        if file.is_file() and file.suffix.lower() in SUPPORTED_EXTENSIONS
    )

    results = []

    for file in files:
        try:
            result = validate_vector_file(str(file))
        except Exception as error:
            result = {
                "file": str(file),
                "status": "ERROR",
                "error": str(error),
            }

        results.append(result)

    output_path.parent.mkdir(exist_ok=True)

    pd.DataFrame(results).to_csv(output_path, index=False)

    print(f"Validated {len(files)} file(s).")
    print(f"Batch report: {output_path}")

    return results


if __name__ == "__main__":
    validate_directory()