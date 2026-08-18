Automated GIS Data Quality Pipeline
A reproducible GIS data quality and validation pipeline using Python, GeoPandas, QGIS, and spatial data.
Project Status
🚧 Active development
The pipeline currently supports automated validation of individual GIS datasets and batch validation of multiple datasets.
Objectives
Validate and clean spatial datasets
Detect common GIS data quality issues
Automate repetitive data-quality checks
Produce clear validation reports
Support batch validation of multiple datasets
Integrate Python workflows with QGIS
Build a reproducible and documented GIS workflow
Technologies
Python
GeoPandas
Pandas
QGIS
Git
GitHub
Project Structure
data/
├── raw/
└── processed/
docs/
src/
├── validate_data.py
├── run_validation.py
└── batch_validate.py
tests/
├── test_validation.py
├── test_run_validation.py
└── test_batch_validation.py
outputs/
Setup
The project uses a Python virtual environment and a requirements.txt file to manage dependencies.
Activate the virtual environment:
.venv\Scripts\activate
Install dependencies:
pip install -r requirements.txt
Usage
Validate a single dataset
python src\run_validation.py data\raw\sample_points.gpkg
The pipeline generates:
outputs/validation_report.json
outputs/validation_report.csv
Validate multiple datasets
python src\batch_validate.py
The batch validator scans data/raw/ and validates supported vector datasets.
Supported formats:
GeoPackage (.gpkg)
Shapefile (.shp)
GeoJSON (.geojson)
JSON (.json)
The consolidated results are written to:
outputs/batch_validation_report.csv
Validation Checks
The pipeline currently checks:
Null geometries
Invalid geometries
Duplicate rows
Duplicate IDs
Null attributes
CRS validity
Geometry types
Unexpected geometry types
Overall quality score
Quality Scoring
Each dataset receives an overall quality score based on detected data-quality issues.
A clean dataset can return:
Validation completed: PASS
Quality score: 100.0
Datasets containing quality issues may return:
Validation completed: WARNING
along with the detected issues and calculated quality score.
Testing
Run the automated test suite with:
python -m pytest
The test suite covers:
Dataset validation
Detection of invalid GIS data
Command-line validation
Batch validation
Validation report generation
Reports
The pipeline produces machine-readable reports in CSV and JSON formats.
Single-dataset reports:
outputs/
├── validation_report.json
└── validation_report.csv
Batch validation report:
outputs/
└── batch_validation_report.csv
Generated reports can be used for quality-control workflows, documentation, and further GIS analysis.
License
To be determined.