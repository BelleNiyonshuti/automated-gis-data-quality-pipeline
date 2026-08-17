from pathlib import Path

import geopandas as gpd


def validate_vector_file(path: str) -> dict:
    """Run basic quality checks on a vector dataset."""
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

    geometry_nulls = int(gdf.geometry.isna().sum())
    invalid_geometries = int((~gdf.geometry.is_valid).sum())
    duplicate_rows = int(gdf.duplicated().sum())

    return {
        "file": str(file_path),
        "status": "OK",
        "features": len(gdf),
        "columns": len(gdf.columns),
        "geometry_nulls": geometry_nulls,
        "invalid_geometries": invalid_geometries,
        "duplicate_rows": duplicate_rows,
        "crs": str(gdf.crs),
    }


if __name__ == "__main__":
    print("GIS data validation module ready.")