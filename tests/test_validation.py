from src.validate_data import validate_vector_file


def test_sample_dataset_passes():
    result = validate_vector_file("data/raw/sample_points.gpkg")

    assert result["status"] == "PASS"
    assert result["features"] == 3
    assert result["geometry_nulls"] == 0
    assert result["invalid_geometries"] == 0
    assert result["duplicate_rows"] == 0
    assert result["quality_score"] == 100.0