from pathlib import Path

from src.run_validation import main


def test_validation_outputs(monkeypatch):
    monkeypatch.setattr(
        "sys.argv",
        [
            "run_validation.py",
            "data/raw/sample_points.gpkg",
        ],
    )

    main()

    assert Path("outputs/validation_report.json").exists()
    assert Path("outputs/validation_report.csv").exists()