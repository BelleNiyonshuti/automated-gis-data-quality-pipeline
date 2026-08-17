from pathlib import Path

import geopandas as gpd


def validate_vector_file(path: str) -> dict:
    """Run GIS data-quality checks on a vector dataset."""
    file_path = Path(path)

    if not file_path.exists():
        return {
            "file": str(file_path),
            "status": "ERROR",
            "message": "File does not exist.",
        }

    try:
        gdf = gpd.read_file(file_path)
    except Exception as exc:
        return {
            "file": str(file_path),
            "status": "ERROR",
            "message": f"Could not read file: {exc}",
        }

    feature_count = len(gdf)
    geometry_nulls = int(gdf.geometry.isna().sum())
    invalid_geometries = int((~gdf.geometry.is_valid).sum())
    duplicate_rows = int(gdf.duplicated().sum())

    null_attributes = int(
        gdf.drop(columns="geometry").isna().sum().sum()
    )

    checks = [
        geometry_nulls == 0,
        invalid_geometries == 0,
        duplicate_rows == 0,
    ]

    passed_checks = sum(checks)
    total_checks = len(checks)
    quality_score = round((passed_checks / total_checks) * 100, 2)

    status = "PASS" if quality_score == 100 else "WARNING"

    return {
        "file": str(file_path),
        "status": status,
        "features": feature_count,
        "columns": len(gdf.columns),
        "geometry_nulls": geometry_nulls,
        "invalid_geometries": invalid_geometries,
        "duplicate_rows": duplicate_rows,
        "null_attributes": null_attributes,
        "crs": str(gdf.crs),
        "quality_score": quality_score,
    }


if __name__ == "__main__":
    print("GIS data validation module ready.")