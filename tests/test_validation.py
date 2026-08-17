import geopandas as gpd
from shapely.geometry import Point, Polygon

from src.validate_data import validate_vector_file


def test_sample_dataset_passes():
    result = validate_vector_file("data/raw/sample_points.gpkg")

    assert result["status"] == "PASS"
    assert result["features"] == 3
    assert result["geometry_nulls"] == 0
    assert result["invalid_geometries"] == 0
    assert result["duplicate_rows"] == 0
    assert result["duplicate_ids"] == 0
    assert result["null_attributes"] == 0
    assert result["crs"] == "EPSG:4326"
    assert result["crs_valid"] is True
    assert result["geometry_types"] == ["Point"]
    assert result["geometry_types_valid"] is True
    assert result["quality_score"] == 100.0


def test_bad_dataset_is_detected(tmp_path):
    bad_file = tmp_path / "bad_sample.gpkg"

    gdf = gpd.GeoDataFrame(
        {
            "id": [1, 1, 2],
            "name": ["A", "B", "C"],
            "geometry": [
                Point(30.06, -1.95),
                None,
                Point(30.08, -1.96),
            ],
        },
        crs="EPSG:4326",
    )

    gdf.to_file(bad_file, driver="GPKG")

    result = validate_vector_file(str(bad_file))

    assert result["status"] == "WARNING"
    assert result["geometry_nulls"] == 1
    assert result["duplicate_ids"] == 1
    assert result["crs_valid"] is True
    assert result["quality_score"] < 100.0