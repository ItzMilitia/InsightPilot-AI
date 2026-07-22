import pytest

from backend.services.report_pipeline import ReportPipeline

from tests.test_report_pipeline_integration import (
    create_sample_dataframe,
)


def test_pipeline_registers_report():

    pipeline = ReportPipeline()

    package = pipeline.run(
        dataframe=create_sample_dataframe(),
        file_name="bank_customers.csv",
        generate_pdf=False,
        generate_json=False,
        return_package=True,
    )

    assert pipeline.registry.count() == 1

    assert pipeline.registry.exists(
        package.metadata.report_id
    )


def test_pipeline_registry_get():

    pipeline = ReportPipeline()

    package = pipeline.run(
        dataframe=create_sample_dataframe(),
        file_name="bank_customers.csv",
        generate_pdf=False,
        generate_json=False,
        return_package=True,
    )

    retrieved = pipeline.registry.get(
        package.metadata.report_id
    )

    assert retrieved is package


def test_pipeline_registry_multiple_reports():

    pipeline = ReportPipeline()

    package1 = pipeline.run(
        dataframe=create_sample_dataframe(),
        file_name="customers1.csv",
        generate_pdf=False,
        generate_json=False,
        return_package=True,
    )

    package2 = pipeline.run(
        dataframe=create_sample_dataframe(),
        file_name="customers2.csv",
        generate_pdf=False,
        generate_json=False,
        return_package=True,
    )

    assert pipeline.registry.count() == 2

    assert pipeline.registry.exists(
        package1.metadata.report_id
    )

    assert pipeline.registry.exists(
        package2.metadata.report_id
    )


def test_pipeline_registry_delete():

    pipeline = ReportPipeline()

    package = pipeline.run(
        dataframe=create_sample_dataframe(),
        file_name="customers.csv",
        generate_pdf=False,
        generate_json=False,
        return_package=True,
    )

    assert pipeline.registry.delete(
        package.metadata.report_id
    )

    assert pipeline.registry.count() == 0


def test_pipeline_registry_clear():

    pipeline = ReportPipeline()

    pipeline.run(
        dataframe=create_sample_dataframe(),
        file_name="customers1.csv",
        generate_pdf=False,
        generate_json=False,
        return_package=True,
    )

    pipeline.run(
        dataframe=create_sample_dataframe(),
        file_name="customers2.csv",
        generate_pdf=False,
        generate_json=False,
        return_package=True,
    )

    assert pipeline.registry.count() == 2

    pipeline.registry.clear()

    assert pipeline.registry.count() == 0