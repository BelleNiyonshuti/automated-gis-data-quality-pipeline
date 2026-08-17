from pathlib import Path

import geopandas as gpd


EXPECTED_CRS = "EPSG:4326"
ALLOWED_GEOMETRY_TYPES = {"Point", "MultiPoint", "LineString", "MultiLineString", "Polygon", "MultiPolygon"}


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

    non_geometry = gdf.drop(columns="geometry")
    null_attributes = int(non_geometry.isna().sum().sum())

    id_columns = [
        column
        for column in gdf.columns
        if column.lower() in {"id", "fid", "objectid"}
    ]

    duplicate_ids = 0

    if id_columns:
        id_column = id_columns[0]
        duplicate_ids = int(gdf[id_column].duplicated().sum())

    actual_crs = str(gdf.crs)
    crs_valid = actual_crs == EXPECTED_CRS

    geometry_types = set(
        gdf.geometry.dropna().geom_type.unique()
    )

    unexpected_geometry_types = sorted(
        geometry_types - ALLOWED_GEOMETRY_TYPES
    )

    geometry_types_valid = len(unexpected_geometry_types) == 0

    checks = [
        geometry_nulls == 0,
        invalid_geometries == 0,
        duplicate_rows == 0,
        duplicate_ids == 0,
        crs_valid,
        geometry_types_valid,
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
        "duplicate_ids": duplicate_ids,
        "null_attributes": null_attributes,
        "crs": actual_crs,
        "crs_valid": crs_valid,
        "geometry_types": sorted(geometry_types),
        "unexpected_geometry_types": unexpected_geometry_types,
        "geometry_types_valid": geometry_types_valid,
        "quality_score": quality_score,
    }


if __name__ == "__main__":
    print("GIS data validation module ready.")