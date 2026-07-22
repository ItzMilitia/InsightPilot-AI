from __future__ import annotations

import pandas as pd
import json
import pandas as pd
import pytest
from backend.services.report_pipeline import ReportPipeline
from pathlib import Path
from backend.services.report_storage_service import ReportStorageService

def create_sample_dataframe() -> pd.DataFrame:
    """
    Create a small banking dataset for integration testing.
    """

    return pd.DataFrame(
        {
            "CustomerID": [1, 2, 3, 4, 5],
            "Age": [22, 45, 31, 27, 39],
            "Balance": [2500, 12000, 5100, 8000, 9500],
            "CreditScore": [720, 680, 790, 650, 700],
        }
    )


def test_pipeline_generates_html_report():

    pipeline = ReportPipeline()

    context, html_report, pdf_path = pipeline.run(
        dataframe=create_sample_dataframe(),
        file_name="bank_customers.csv",
        generate_pdf=False,
        generate_json=False,
        return_package=False,
    )

    assert context is not None

    assert html_report is not None

    assert html_report.html

    assert pdf_path is None

def test_pipeline_returns_report_package():

    pipeline = ReportPipeline()

    package = pipeline.run(
        dataframe=create_sample_dataframe(),
        file_name="bank_customers.csv",
        generate_pdf=False,
        generate_json=False,
        return_package=True,
    )

    assert package is not None

    assert package.metadata is not None

    assert package.html_report is not None

    assert package.html_report.html

    assert package.pdf_report is None

    assert package.json_report_path is None

    assert package.metadata.report_id

    assert package.metadata.title

def test_pipeline_generates_json_report(tmp_path):

    pipeline = ReportPipeline()

    json_output = tmp_path / "report.json"

    package = pipeline.run(
        dataframe=create_sample_dataframe(),
        file_name="bank_customers.csv",
        generate_pdf=False,
        generate_json=True,
        json_output_path=str(json_output),
        return_package=True,
    )

    assert package is not None

    assert package.json_report_path is not None

    assert Path(package.json_report_path).exists()

    assert Path(package.json_report_path).suffix == ".json"

def test_pipeline_generates_pdf_report(tmp_path):

    pipeline = ReportPipeline()

    pdf_output = tmp_path / "report.pdf"

    package = pipeline.run(
        dataframe=create_sample_dataframe(),
        file_name="bank_customers.csv",
        generate_pdf=True,
        pdf_output_path=str(pdf_output),
        generate_json=False,
        return_package=True,
    )

    assert package is not None

    assert package.pdf_report is not None

    assert package.pdf_report.file_path is not None

    pdf_path = Path(package.pdf_report.file_path)

    assert pdf_path.exists()

    assert pdf_path.suffix == ".pdf"

def test_report_storage_service(tmp_path):

    pipeline = ReportPipeline()

    package = pipeline.run(
        dataframe=create_sample_dataframe(),
        file_name="bank_customers.csv",
        generate_pdf=True,
        pdf_output_path=str(tmp_path / "report.pdf"),
        generate_json=True,
        json_output_path=str(tmp_path / "report.json"),
        return_package=True,
    )

    storage = ReportStorageService()

    output_dir = tmp_path / "stored_reports"

    storage.save(
        package=package,
        output_directory=output_dir,
    )

    assert (output_dir / "report.html").exists()

    assert (output_dir / "report.pdf").exists()

    assert (output_dir / "report.json").exists()

    assert (output_dir / "manifest.json").exists()

    assert "html" in package.artifacts

    assert "pdf" in package.artifacts

    assert "json" in package.artifacts

def test_manifest_contents(tmp_path):

    pipeline = ReportPipeline()

    package = pipeline.run(
        dataframe=create_sample_dataframe(),
        file_name="bank_customers.csv",
        generate_pdf=True,
        pdf_output_path=str(tmp_path / "report.pdf"),
        generate_json=True,
        json_output_path=str(tmp_path / "report.json"),
        return_package=True,
    )

    storage = ReportStorageService()

    output_dir = tmp_path / "manifest_test"

    storage.save(
        package=package,
        output_directory=output_dir,
    )

    manifest_path = output_dir / "manifest.json"

    assert manifest_path.exists()

    with manifest_path.open(
        "r",
        encoding="utf-8",
    ) as file:

        manifest = json.load(file)

    assert "metadata" in manifest

    assert "formats" in manifest

    assert "artifacts" in manifest

    assert manifest["metadata"]["report_id"] == package.metadata.report_id

    assert "HTML" in manifest["formats"]

    assert "PDF" in manifest["formats"]

    assert "JSON" in manifest["formats"]

def test_package_artifacts_exist(tmp_path):

    pipeline = ReportPipeline()

    package = pipeline.run(
        dataframe=create_sample_dataframe(),
        file_name="bank_customers.csv",
        generate_pdf=True,
        pdf_output_path=str(tmp_path / "report.pdf"),
        generate_json=True,
        json_output_path=str(tmp_path / "report.json"),
        return_package=True,
    )

    storage = ReportStorageService()

    output_dir = tmp_path / "artifact_test"

    storage.save(
        package=package,
        output_directory=output_dir,
    )

    assert package.artifacts

    for name, path in package.artifacts.items():

        assert Path(path).exists(), f"{name} artifact does not exist: {path}"

def test_pipeline_empty_dataframe():

    pipeline = ReportPipeline()

    empty_df = pd.DataFrame()

    with pytest.raises(ValueError):
        pipeline.run(
            dataframe=empty_df,
            file_name="empty.csv",
            return_package=True,
        )

def test_legacy_api_backward_compatibility():

    pipeline = ReportPipeline()

    result = pipeline.run(
        dataframe=create_sample_dataframe(),
        file_name="bank_customers.csv",
        generate_pdf=False,
        generate_json=False,
        return_package=False,
    )

    assert isinstance(result, tuple)

    assert len(result) == 3

    context, html_report, pdf_path = result

    assert context is not None

    assert html_report is not None

    assert html_report.html

    assert pdf_path is None

def test_pipeline_multiple_runs_are_isolated():

    pipeline = ReportPipeline()

    package1 = pipeline.run(
        dataframe=create_sample_dataframe(),
        file_name="bank_customers_1.csv",
        generate_pdf=False,
        generate_json=False,
        return_package=True,
    )

    package2 = pipeline.run(
        dataframe=create_sample_dataframe(),
        file_name="bank_customers_2.csv",
        generate_pdf=False,
        generate_json=False,
        return_package=True,
    )

    assert package1 is not package2

    assert package1.metadata is not package2.metadata

    assert package1.metadata.report_id != package2.metadata.report_id

    assert package1.html_report is not package2.html_report

    assert package1.artifacts == {}

    assert package2.artifacts == {}

def test_report_metadata_is_unique():

    pipeline = ReportPipeline()

    package1 = pipeline.run(
        dataframe=create_sample_dataframe(),
        file_name="bank_customers.csv",
        generate_pdf=False,
        generate_json=False,
        return_package=True,
    )

    package2 = pipeline.run(
        dataframe=create_sample_dataframe(),
        file_name="bank_customers.csv",
        generate_pdf=False,
        generate_json=False,
        return_package=True,
    )

    metadata1 = package1.metadata
    metadata2 = package2.metadata

    assert metadata1.report_id != metadata2.report_id

    assert metadata1.generated_at != metadata2.generated_at

    assert metadata1.title == metadata2.title

    assert metadata1.version == metadata2.version