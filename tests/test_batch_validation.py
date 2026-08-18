from pathlib import Path

from src.batch_validate import validate_directory


def test_validate_directory():
    output_file = "outputs/test_batch_validation_report.csv"

    results = validate_directory(
        input_dir="data/raw",
        output_file=output_file,
    )

    assert len(results) >= 1
    assert Path(output_file).exists()
    assert results[0]["status"] in {"PASS", "WARNING", "ERROR"}