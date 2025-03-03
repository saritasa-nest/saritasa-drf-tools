import pathlib

import pytest
from django.core.management import call_command
from drf_spectacular.management.commands import spectacular


def test_open_api(tmp_path: pathlib.Path) -> None:
    """Validate that schema is properly generated."""
    try:
        call_command(
            "spectacular",
            file=tmp_path / "schema.yaml",
            validate=True,
            fail_on_warn=True,
        )
    except spectacular.SchemaGenerationError:
        pytest.fail(
            reason=(
                "Schema generation failed, check logs or run: "
                "inv open-api.validate-swagger"
            ),
            pytrace=False,
        )
